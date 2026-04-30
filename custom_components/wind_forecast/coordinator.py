from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, DOMAIN, UPDATE_INTERVAL_MINUTES

_LOGGER = logging.getLogger(__name__)


class WindForecastCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, latitude: float, longitude: float, name: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"Wind Forecast {name}",
            update_interval=timedelta(minutes=UPDATE_INTERVAL_MINUTES),
        )
        self.latitude = latitude
        self.longitude = longitude

    async def _async_update_data(self) -> dict:
        session = async_get_clientsession(self.hass)
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "hourly": "windspeed_10m,windgusts_10m,winddirection_10m",
            "daily": "windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant",
            "forecast_days": 7,
            "timezone": "auto",
            "windspeed_unit": "kmh",
        }
        try:
            async with session.get(API_URL, params=params) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"API returned status {resp.status}")
                data = await resp.json()
        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(f"Error fetching wind data: {err}") from err

        utc_offset = data.get("utc_offset_seconds", 0)
        local_tz = timezone(timedelta(seconds=utc_offset))
        now_local = datetime.now(timezone.utc).astimezone(local_tz)
        current_hour_str = now_local.strftime("%Y-%m-%dT%H:00")

        hourly_times = data["hourly"]["time"]
        try:
            current_index = hourly_times.index(current_hour_str)
        except ValueError:
            _LOGGER.warning(
                "Current hour %s not found in hourly data, using index 0", current_hour_str
            )
            current_index = 0

        return {
            "hourly": data["hourly"],
            "daily": data["daily"],
            "current_index": current_index,
        }
