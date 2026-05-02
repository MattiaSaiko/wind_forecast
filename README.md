# Wind Forecast — Home Assistant Custom Component

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2024.1.0%2B-blue.svg)](https://www.home-assistant.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🇬🇧 English

### Overview

**Wind Forecast** is a Home Assistant custom integration that fetches wind data from [Open-Meteo](https://open-meteo.com/) — a free, no-API-key weather service. It exposes current wind conditions and a 7-day forecast as standard HA sensors, ready for automations, dashboards, and Lovelace cards.

### Features

- **No API key required** — uses the free Open-Meteo API
- **Current conditions**: wind speed, gust, and bearing at 10 m height
- **7-day daily forecast**: max wind speed, max gust, dominant wind bearing per day
- **Convenience sensors**: dedicated sensors for today and tomorrow
- **Multiple zones**: add as many locations as needed via the UI
- **HACS compatible**

### Requirements

| Requirement | Version |
|---|---|
| Home Assistant | ≥ 2024.1.0 |
| HACS | any |
| Internet access | — |

### Installation

#### Via HACS (recommended)

1. Open HACS → **Integrations** → ⋮ → **Custom repositories**
2. Add this repository URL, category **Integration**
3. Search for **Wind Forecast** and install
4. Restart Home Assistant

#### Manual

1. Copy `custom_components/wind_forecast/` into your HA `config/custom_components/` folder
2. Restart Home Assistant

### Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Wind Forecast**
3. Fill in:
   - **Zone name** — a label for this location (e.g. `Home`, `Mountain Cabin`)
   - **Latitude** — defaults to HA location
   - **Longitude** — defaults to HA location
4. Submit — sensors appear immediately

You can add multiple entries for different locations.

### Sensors

All sensor names follow the pattern `sensor.wind_forecast_<zone>_<type>`.

#### Current conditions (updated every 60 min)

| Sensor | Unit | Description |
|---|---|---|
| `wind_speed` | km/h | Current wind speed at 10 m |
| `wind_gust` | km/h | Current wind gust at 10 m |
| `wind_bearing` | ° | Current wind direction |

#### Convenience — Today & Tomorrow

| Sensor | Unit | Description |
|---|---|---|
| `wind_max_today` | km/h | Max wind speed today |
| `wind_gust_max_today` | km/h | Max gust today |
| `wind_bearing_today` | ° | Dominant wind direction today |
| `wind_max_tomorrow` | km/h | Max wind speed tomorrow |
| `wind_gust_max_tomorrow` | km/h | Max gust tomorrow |
| `wind_bearing_tomorrow` | ° | Dominant wind direction tomorrow |

#### 7-day daily forecast

For each day `N` (0 = today … 6 = day after 6 days):

| Sensor | Unit | Description |
|---|---|---|
| `wind_max_day_<N>` | km/h | Max wind speed |
| `wind_gust_max_day_<N>` | km/h | Max gust |
| `wind_bearing_dominant_day_<N>` | ° | Dominant wind direction |

Daily sensors also carry `extra_state_attributes` with the full 7-day array and date list — useful for template sensors and custom cards.

### Data source

[Open-Meteo](https://open-meteo.com/) — free, open-source weather API. No registration, no API key. Data refreshes every hour.

---

## 🇮🇹 Italiano

### Panoramica

**Wind Forecast** è un'integrazione personalizzata per Home Assistant che recupera i dati del vento da [Open-Meteo](https://open-meteo.com/) — un servizio meteorologico gratuito e senza chiave API. Espone le condizioni attuali e le previsioni a 7 giorni come sensori HA standard, pronti per automazioni, dashboard e card Lovelace.

### Funzionalità

- **Nessuna API key** — usa la API gratuita di Open-Meteo
- **Condizioni attuali**: velocità del vento, raffica e direzione a 10 m di altezza
- **Previsione giornaliera a 7 giorni**: velocità massima, raffica massima e direzione dominante
- **Sensori di convenienza**: sensori dedicati per oggi e domani
- **Zone multiple**: aggiungi tutte le località che vuoi tramite UI
- **Compatibile con HACS**

### Requisiti

| Requisito | Versione |
|---|---|
| Home Assistant | ≥ 2024.1.0 |
| HACS | qualsiasi |
| Accesso Internet | — |

### Installazione

#### Tramite HACS (consigliato)

1. Apri HACS → **Integrazioni** → ⋮ → **Repository personalizzati**
2. Aggiungi l'URL di questo repository, categoria **Integration**
3. Cerca **Wind Forecast** e installa
4. Riavvia Home Assistant

#### Manuale

1. Copia la cartella `custom_components/wind_forecast/` nella cartella `config/custom_components/` di HA
2. Riavvia Home Assistant

### Configurazione

1. Vai su **Impostazioni → Dispositivi e servizi → Aggiungi integrazione**
2. Cerca **Wind Forecast**
3. Compila:
   - **Nome zona** — etichetta per questa posizione (es. `Casa`, `Rifugio`)
   - **Latitudine** — predefinita dalla posizione di HA
   - **Longitudine** — predefinita dalla posizione di HA
4. Conferma — i sensori appaiono immediatamente

È possibile aggiungere più voci per diverse località.

### Sensori

Tutti i sensori seguono il pattern `sensor.wind_forecast_<zona>_<tipo>`.

#### Condizioni attuali (aggiornate ogni 60 min)

| Sensore | Unità | Descrizione |
|---|---|---|
| `wind_speed` | km/h | Velocità del vento attuale a 10 m |
| `wind_gust` | km/h | Raffica attuale a 10 m |
| `wind_bearing` | ° | Direzione del vento attuale |

#### Convenienza — Oggi e Domani

| Sensore | Unità | Descrizione |
|---|---|---|
| `wind_max_today` | km/h | Velocità massima oggi |
| `wind_gust_max_today` | km/h | Raffica massima oggi |
| `wind_bearing_today` | ° | Direzione dominante oggi |
| `wind_max_tomorrow` | km/h | Velocità massima domani |
| `wind_gust_max_tomorrow` | km/h | Raffica massima domani |
| `wind_bearing_tomorrow` | ° | Direzione dominante domani |

#### Previsione giornaliera a 7 giorni

Per ogni giorno `N` (0 = oggi … 6 = tra 6 giorni):

| Sensore | Unità | Descrizione |
|---|---|---|
| `wind_max_day_<N>` | km/h | Velocità massima del vento |
| `wind_gust_max_day_<N>` | km/h | Raffica massima |
| `wind_bearing_dominant_day_<N>` | ° | Direzione dominante |

I sensori giornalieri espongono anche `extra_state_attributes` con l'array completo a 7 giorni e la lista delle date — utile per template sensor e card personalizzate.

### Sorgente dati

[Open-Meteo](https://open-meteo.com/) — API meteo gratuita e open-source. Nessuna registrazione, nessuna chiave API. I dati si aggiornano ogni ora.

---

## License / Licenza

MIT — see [LICENSE.md](LICENSE.md)
