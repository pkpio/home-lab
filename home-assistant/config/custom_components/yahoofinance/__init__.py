"""
The Yahoo finance component.

https://github.com/iprak/yahoofinance
"""

from datetime import timedelta
import logging
from typing import Union

import async_timeout
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import callback
from homeassistant.helpers import discovery, event
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import async_track_point_in_utc_time
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util.dt import utcnow
import voluptuous as vol

from .const import (
    BASE,
    CONF_DECIMAL_PLACES,
    CONF_INCLUDE_FIFTY_DAY_VALUES,
    CONF_INCLUDE_POST_VALUES,
    CONF_INCLUDE_PRE_VALUES,
    CONF_INCLUDE_TWO_HUNDRED_DAY_VALUES,
    CONF_SHOW_TRENDING_ICON,
    CONF_SYMBOLS,
    CONF_TARGET_CURRENCY,
    DATA_REGULAR_MARKET_PRICE,
    DEFAULT_CONF_DECIMAL_PLACES,
    DEFAULT_CONF_INCLUDE_FIFTY_DAY_VALUES,
    DEFAULT_CONF_INCLUDE_POST_VALUES,
    DEFAULT_CONF_INCLUDE_PRE_VALUES,
    DEFAULT_CONF_INCLUDE_TWO_HUNDRED_DAY_VALUES,
    DEFAULT_CONF_SHOW_TRENDING_ICON,
    DOMAIN,
    HASS_DATA_CONFIG,
    HASS_DATA_COORDINATOR,
    NUMERIC_DATA_GROUPS,
    SERVICE_REFRESH,
    STRING_DATA_KEYS,
)

_LOGGER = logging.getLogger(__name__)
DEFAULT_SCAN_INTERVAL = timedelta(hours=6)
MINIMUM_SCAN_INTERVAL = timedelta(seconds=30)
WEBSESSION_TIMEOUT = 15
DELAY_ASYNC_REQUEST_REFRESH = 5
FAILURE_ASYNC_REQUEST_REFRESH = 20

BASIC_SYMBOL_SCHEMA = vol.All(cv.string, vol.Upper)

COMPLEX_SYMBOL_SCHEMA = vol.All(
    dict,
    vol.Schema(
        {
            vol.Required("symbol"): BASIC_SYMBOL_SCHEMA,
            vol.Optional(CONF_TARGET_CURRENCY): BASIC_SYMBOL_SCHEMA,
        }
    ),
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_SYMBOLS): vol.All(
                    cv.ensure_list,
                    [vol.Any(BASIC_SYMBOL_SCHEMA, COMPLEX_SYMBOL_SCHEMA)],
                ),
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.Any("none", "None", cv.positive_time_period),
                vol.Optional(CONF_TARGET_CURRENCY): vol.All(cv.string, vol.Upper),
                vol.Optional(
                    CONF_SHOW_TRENDING_ICON, default=DEFAULT_CONF_SHOW_TRENDING_ICON
                ): cv.boolean,
                vol.Optional(
                    CONF_DECIMAL_PLACES, default=DEFAULT_CONF_DECIMAL_PLACES
                ): vol.Coerce(int),
                vol.Optional(
                    CONF_INCLUDE_FIFTY_DAY_VALUES,
                    default=DEFAULT_CONF_INCLUDE_FIFTY_DAY_VALUES,
                ): cv.boolean,
                vol.Optional(
                    CONF_INCLUDE_POST_VALUES, default=DEFAULT_CONF_INCLUDE_POST_VALUES
                ): cv.boolean,
                vol.Optional(
                    CONF_INCLUDE_PRE_VALUES, default=DEFAULT_CONF_INCLUDE_PRE_VALUES
                ): cv.boolean,
                vol.Optional(
                    CONF_INCLUDE_TWO_HUNDRED_DAY_VALUES,
                    default=DEFAULT_CONF_INCLUDE_TWO_HUNDRED_DAY_VALUES,
                ): cv.boolean,
            }
        )
    },
    # The complete HA configuration is passed down to`async_setup`, allow the extra keys.
    extra=vol.ALLOW_EXTRA,
)


def parse_scan_interval(scan_interval: Union[timedelta, str]) -> timedelta:
    """Parse and validate scan_interval."""
    if isinstance(scan_interval, str):
        if isinstance(scan_interval, str):
            if scan_interval.lower() == "none":
                scan_interval = None
            else:
                raise vol.Invalid(
                    f"Invalid {CONF_SCAN_INTERVAL} specified: {scan_interval}"
                )
    elif scan_interval < MINIMUM_SCAN_INTERVAL:
        raise vol.Invalid("Scan interval should be at least 30 seconds.")

    return scan_interval


def normalize_input(defined_symbols):
    """Normalize input and remove duplicates."""
    symbols = set()
    normalized_symbols = []

    for value in defined_symbols:
        if isinstance(value, str):
            if value not in symbols:
                symbols.add(value)
                normalized_symbols.append({"symbol": value})
        else:
            if value["symbol"] not in symbols:
                symbols.add(value["symbol"])
                normalized_symbols.append(value)

    return (list(symbols), normalized_symbols)


async def async_setup(hass, config) -> bool:
    """Set up the component."""
    domain_config = config.get(DOMAIN, {})
    defined_symbols = domain_config.get(CONF_SYMBOLS, [])

    symbols, normalized_symbols = normalize_input(defined_symbols)
    domain_config[CONF_SYMBOLS] = normalized_symbols

    scan_interval = parse_scan_interval(domain_config.get(CONF_SCAN_INTERVAL))

    # Populate parsed value into domain_config
    domain_config[CONF_SCAN_INTERVAL] = scan_interval

    coordinator = YahooSymbolUpdateCoordinator(symbols, hass, scan_interval)

    # Refresh coordinator to get initial symbol data
    _LOGGER.info(
        "Requesting data from coordinator with update interval of %s.", scan_interval
    )
    await coordinator.async_refresh()

    # Pass down the coordinator and config to platforms.
    hass.data[DOMAIN] = {
        HASS_DATA_COORDINATOR: coordinator,
        HASS_DATA_CONFIG: domain_config,
    }

    async def handle_refresh_symbols(_call):
        """Refresh symbol data."""
        _LOGGER.info("Processing refresh_symbols")
        await coordinator.async_request_refresh()

    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH,
        handle_refresh_symbols,
    )

    if not coordinator.last_update_success:
        _LOGGER.debug("Coordinator did not report any data, requesting async_refresh")
        hass.async_create_task(coordinator.async_request_refresh())

    hass.async_create_task(
        discovery.async_load_platform(hass, "sensor", DOMAIN, {}, config)
    )

    return True


class YahooSymbolUpdateCoordinator(DataUpdateCoordinator):
    """Yahoo finance data update coordinator."""

    @staticmethod
    def parse_symbol_data(symbol_data):
        """Return data pieces which we care about, use 0 for missing numeric values."""
        data = {}

        # get() ensures that we have an entry in symbol_data.
        for group in NUMERIC_DATA_GROUPS:
            for value in NUMERIC_DATA_GROUPS[group]:
                key = value[0]
                data[key] = symbol_data.get(key, 0)

        for key in STRING_DATA_KEYS:
            data[key] = symbol_data.get(key)

        return data

    def __init__(self, symbols, hass, update_interval) -> None:
        """Initialize."""
        self._symbols = symbols
        self.data = None
        self.loop = hass.loop
        self.websession = async_get_clientsession(hass)
        self._update_interval = update_interval
        self._failure_update_interval = timedelta(seconds=FAILURE_ASYNC_REQUEST_REFRESH)

        super().__init__(
            hass,
            _LOGGER,
            name="YahooSymbolUpdateCoordinator",
            update_method=self._async_update,
            update_interval=update_interval,
        )

    def get_next_update_interval(self):
        """Get the update interval for the next async_track_point_in_utc_time call."""
        if self.last_update_success:
            return self._update_interval
        else:
            _LOGGER.warning(
                "Error obtaining data, retrying in %d seconds.",
                FAILURE_ASYNC_REQUEST_REFRESH,
            )
            return self._failure_update_interval

    @callback
    def _schedule_refresh(self) -> None:
        """Schedule a refresh."""
        if self._unsub_refresh:
            self._unsub_refresh()
            self._unsub_refresh = None

        # We _floor_ utcnow to create a schedule on a rounded second,
        # minimizing the time between the point and the real activation.
        # That way we obtain a constant update frequency,
        # as long as the update process takes less than a second

        update_interval = self.get_next_update_interval()
        if update_interval is not None:
            self._unsub_refresh = async_track_point_in_utc_time(
                self.hass,
                self._handle_refresh_interval,
                utcnow().replace(microsecond=0) + update_interval,
            )

    def get_symbols(self):
        """Return symbols tracked by the coordinator."""
        return self._symbols

    async def _async_request_refresh_later(self, _now):
        """Request async_request_refresh."""
        await self.async_request_refresh()

    def add_symbol(self, symbol) -> bool:
        """Add symbol to the symbol list."""
        if symbol not in self._symbols:
            self._symbols.append(symbol)

            # Request a refresh to get data for the missing symbol.
            # This would have been called while data for sensor was being parsed.
            # async_request_refresh has debouncing built into it, so multiple calls
            # to add_symbol will still resut in single refresh.
            event.async_call_later(
                self.hass,
                DELAY_ASYNC_REQUEST_REFRESH,
                self._async_request_refresh_later,
            )

            _LOGGER.info(
                "Added %s and requested update in %d seconds.",
                symbol,
                DELAY_ASYNC_REQUEST_REFRESH,
            )
            return True

        return False

    async def get_json(self):
        """Get the JSON data."""
        json = None

        async with async_timeout.timeout(WEBSESSION_TIMEOUT, loop=self.loop):
            response = await self.websession.get(BASE + ",".join(self._symbols))
            json = await response.json()

        _LOGGER.debug("Data = %s", json)
        return json

    async def _async_update(self):
        """
        Return updated data if new JSON is valid.

        The exception will get properly handled in the caller (DataUpdateCoordinator.async_refresh)
        which also updates last_update_success. UpdateFailed is raised if JSON is invalid.
        """

        json = await self.get_json()

        if json is None:
            raise UpdateFailed("No data received")

        if "quoteResponse" not in json:
            raise UpdateFailed("Data invalid, 'quoteResponse' not found.")

        quoteResponse = json["quoteResponse"]  # pylint: disable=invalid-name

        if "error" in quoteResponse:
            if quoteResponse["error"] is not None:
                raise UpdateFailed(quoteResponse["error"])

        if "result" not in quoteResponse:
            raise UpdateFailed("Data invalid, no 'result' found")

        result = quoteResponse["result"]
        if result is None:
            raise UpdateFailed("Data invalid, 'result' is None")

        data = {}
        for symbol_data in result:
            symbol = symbol_data["symbol"]
            data[symbol] = self.parse_symbol_data(symbol_data)

            _LOGGER.debug(
                "Updated %s to %s",
                symbol,
                data[symbol][DATA_REGULAR_MARKET_PRICE],
            )

        _LOGGER.info("Data updated")
        return data
