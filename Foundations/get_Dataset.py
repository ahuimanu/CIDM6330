import requests
import pandas as pd

# BLS API endpoint
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# Request payload
payload = {
    "seriesid": ['EIUIR'],  # separate series IDs
    "startyear": "1999",
    "endyear": "2025",
    "registrationkey": "a8a5e1c87c69445a8db4e07d6d4f6fe9"
}

# Make request
response = requests.post(url, json=payload)
json_data = response.json()

# Store rows here
rows = []

# Parse JSON
for series in json_data["Results"]["series"]:
    series_id = series["seriesID"]

    for item in series["data"]:
        period = item["period"]

        # Keep only monthly data
        if period.startswith("M"):
            year = int(item["year"])
            month = int(period[1:])  # M01 → 1
            value = float(item["value"])

            rows.append([series_id, year, month, value])

# Create DataFrame
df = pd.DataFrame(rows, columns=["series_id", "year", "month", "value"])

# Create proper datetime column
df["date"] = pd.to_datetime(dict(year=df.year, month=df.month, day=1))

# Optional: sort
df = df.sort_values(["series_id", "date"])


df.to_csv("bls_data.csv", index=False)

print(df.head())