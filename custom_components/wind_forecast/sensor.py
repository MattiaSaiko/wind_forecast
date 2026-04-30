from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WindForecastCoordinator

# (key, friendly_name, unit, device_class, hourly_key)
_CURRENT = [
    ("wind_speed", "Wind Speed", "km/h", SensorDeviceClass.WIND_SPEED, "windspeed_10m"),
    ("wind_gust", "Wind Gust", "km/h", SensorDeviceClass.WIND_SPEED, "windgusts_10m"),
    ("wind_bearing", "Wind Bearing", "°", None, "winddirection_10m"),
]

# (key_prefix, friendly_prefix, unit, device_class, daily_key, attr_key)
_DAILY_TYPES = [
    ("wind_max_day", "Wind Max Day", "km/h", SensorDeviceClass.WIND_SPEED, "windspeed_10m_max", "forecast_wind_max"),
    ("wind_gust_max_day", "Wind Gust Max Day", "km/h", SensorDeviceClass.WIND_SPEED, "windgusts_10m_max", "forecast_wind_gust_max"),
    ("wind_bearing_dominant_day", "Wind Bearing Day", "°", None, "winddirection_10m_dominant", "forecast_wind_bearing_dominant"),
]

# (key, friendly_name, unit, device_class, daily_key, day_index, attr_key)
_CONVENIENCE = [
    ("wind_max_today", "Wind Max Today", "km/h", SensorDeviceClass.WIND_SPEED, "windspeed_10m_max", 0, "forecast_wind_max"),
    ("wind_gust_max_today", "Wind Gust Max Today", "km/h", SensorDeviceClass.WIND_SPEED, "windgusts_10m_max", 0, "forecast_wind_gust_max"),
    ("wind_bearing_today", "Wind Bearing Today", "°", None, "winddirection_10m_dominant", 0, "forecast_wind_bearing_dominant"),
    ("wind_max_tomorrow", "Wind Max Tomorrow", "km/h", SensorDeviceClass.WIND_SPEED, "windspeed_10m_max", 1, "forecast_wind_max"),
    ("wind_gust_max_tomorrow", "Wind Gust Max Tomorrow", "km/h", SensorDeviceClass.WIND_SPEED, "windgusts_10m_max", 1, "forecast_wind_gust_max"),
    ("wind_bearing_tomorrow", "Wind Bearing Tomorrow", "°", None, "winddirection_10m_dominant", 1, "forecast_wind_bearing_dominant"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: WindForecastCoordinator = hass.data[DOMAIN][entry.entry_id]
    zone_name = entry.data[CONF_NAME]
    entities: list[SensorEntity] = []

    for key, friendly, unit, device_class, hourly_key in _CURRENT:
        entities.append(
            WindForecastCurrentSensor(coordinator, entry, key, friendly, unit, device_class, hourly_key, zone_name)
        )

    for day in range(7):
        for key_prefix, friendly_prefix, unit, device_class, daily_key, attr_key in _DAILY_TYPES:
            entities.append(
                WindForecastDailySensor(
                    coordinator, entry,
                    f"{key_prefix}_{day}", f"{friendly_prefix} {day}",
                    unit, device_class, daily_key, day, attr_key, zone_name,
                )
            )

    for key, friendly, unit, device_class, daily_key, day_idx, attr_key in _CONVENIENCE:
        entities.append(
            WindForecastDailySensor(
                coordinator, entry,
                key, friendly,
                unit, device_class, daily_key, day_idx, attr_key, zone_name,
            )
        )

    async_add_entities(entities)


class _WindForecastBase(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: WindForecastCoordinator,
        entry: ConfigEntry,
        key: str,
        friendly_name: str,
        unit: str,
        device_class,
        zone_name: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_name = f"Wind Forecast {zone_name} {friendly_name}"
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class


class WindForecastCurrentSensor(_WindForecastBase):
    def __init__(self, coordinator, entry, key, friendly_name, unit, device_class, hourly_key, zone_name):
        super().__init__(coordinator, entry, key, friendly_name, unit, device_class, zone_name)
        self._hourly_key = hourly_key
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        if self.coordinator.data is None:
            return None
        idx = self.coordinator.data["current_index"]
        return self.coordinator.data["hourly"][self._hourly_key][idx]


class WindForecastDailySensor(_WindForecastBase):
    def __init__(self, coordinator, entry, key, friendly_name, unit, device_class, daily_key, day_index, attr_key, zone_name):
        super().__init__(coordinator, entry, key, friendly_name, unit, device_class, zone_name)
        self._daily_key = daily_key
        self._day_index = day_index
        self._attr_key = attr_key

    @property
    def native_value(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data["daily"][self._daily_key][self._day_index]

    @property
    def extra_state_attributes(self):
        if self.coordinator.data is None:
            return {}
        daily = self.coordinator.data["daily"]
        return {
            self._attr_key: daily[self._daily_key],
            "forecast_dates": daily["time"],
        }
