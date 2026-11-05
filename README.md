# NYC Charter Schools Map

An interactive map of every charter school location in New York City's five boroughs.

**Live map:** https://YOUR-USERNAME.github.io/nyc-charter-schools-map/

![screenshot](screenshot.png)

## What it does

- Plots **260 open charter school locations** (278 including those marked closed) across all five boroughs, color-coded by borough
- Click any pin for the school's address, grade levels, neighborhood, district, year opened, leader, and phone number, plus a Google Maps link
- Filter by borough and school level, search by name, neighborhood, or address, and optionally show closed schools
- Pins cluster when zoomed out so dense areas like the South Bronx and Central Brooklyn stay readable
- Works on mobile

| Borough | Open charter schools |
|---|---|
| Brooklyn | 93 |
| Bronx | 83 |
| Manhattan | 54 |
| Queens | 24 |
| Staten Island | 6 |

## Data

- **Source:** [2019–2020 School Locations](https://data.cityofnewyork.us/d/wg9x-4ke6) (NYC Department of Education, via NYC Open Data). This is the most recent school locations dataset on NYC Open Data that includes coordinates.
- **Filter:** `managed_by_name = 'Charter'` (the dataset tags every school as either `DOE` or `Charter`)
- **Loading:** the map pulls data **live from the NYC Open Data API** when the page opens, so nothing needs re-deploying if the city updates the dataset. If the API is unavailable, it falls back to the snapshot in `data/charter_schools.json`.
- **Cleaning:** removed 5 duplicate rows (same school code and address), and hid schools marked `Closed` by default.

## Known limitations

1. **The data is from the 2019–20 school year.** NYC Open Data hasn't published a newer locations file. Schools that opened, moved, or closed since then won't be reflected, and leader names and phone numbers may be out of date.
2. **One school can have several pins.** Multi-site charters (for example, a K–12 network with separate elementary and high school buildings) appear once per location, which is what a family looking for a nearby school needs.
3. **Several schools can share one building.** Charter schools are often co-located with other schools, so a few pins sit on the same spot. Clicking the cluster spreads them out.
4. **Borough comes from the school code** (`K` = Brooklyn, `X` = Bronx, `M` = Manhattan, `Q` = Queens, `R` = Staten Island), the DOE's standard convention.

## What I'd do next

- **Get current data.** Join to the DOE's current [LCGMS school report](https://infohub.nyced.org/reports-and-policies/citywide-information-and-data/lcgms) or the NY State Education Department school directory, and geocode new addresses with NYC's free Geoclient API.
- **Add decision-useful layers.** Enrollment, demographics, and test results (from the DOE and the NYC Charter School Center) so the map answers *"which schools are good and have seats near me?"* and not just *"where are they?"*
- **Find gaps in access.** Overlay school district boundaries and child population to show which neighborhoods have few charter options.
- **Let users ask questions in plain English**, such as "K–5 charters within a mile of the 2/3 train in Crown Heights," by sending the user's question and the school data to an LLM.

## How I built it

Time-boxed to one hour, built with an AI assistant (Claude) as a pair programmer:

1. **Scoped the ask:** "a map of all charter schools in NYC" → a shareable, interactive web map a reviewer can open with one click (GitHub Pages), with no build step or API keys.
2. **Found and checked the data:** compared NYC Open Data datasets, confirmed the charter flag and coordinates, and checked counts by borough and status.
3. **Built** a single-page map with [Leaflet](https://leafletjs.com/) and [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster), with basemap tiles from CARTO and OpenStreetMap.
4. **Tested** the filters, de-duplication, popups, and the fallback to the saved snapshot in a headless browser.

My role was product decisions (scope, data source, what to show in popups, hiding closed schools by default, documenting limitations); the AI did most of the code writing.

## Run it locally

```bash
python3 scripts/fetch_data.py   # optional: refresh the backup snapshot
python3 -m http.server 8000      # then open http://localhost:8000
```

## Files

```
index.html               the map (HTML, CSS, and JS in one file)
data/charter_schools.json backup snapshot of the dataset
scripts/fetch_data.py    refreshes the snapshot from the NYC Open Data API
```
