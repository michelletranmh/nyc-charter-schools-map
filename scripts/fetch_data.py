"""Save a snapshot of NYC charter school locations from NYC Open Data.

The map loads data live from the API. This snapshot is a backup the map
falls back to if the API is ever down. No dependencies needed.

Usage:  python3 scripts/fetch_data.py
"""
import json
import pathlib
import urllib.parse
import urllib.request

DATASET = "wg9x-4ke6"  # 2019-2020 School Locations (NYC DOE / LCGMS)
params = {
    "$where": "managed_by_name='Charter'",
    "$limit": "5000",
    "$order": "location_name",
}
url = f"https://data.cityofnewyork.us/resource/{DATASET}.json?" + urllib.parse.urlencode(params)

with urllib.request.urlopen(url, timeout=30) as resp:
    rows = json.load(resp)

out = pathlib.Path(__file__).resolve().parent.parent / "data" / "charter_schools.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(rows, indent=1))

open_count = sum(1 for r in rows if r.get("status_descriptions") == "Open")
print(f"Saved {len(rows)} rows ({open_count} marked open) to {out}")
