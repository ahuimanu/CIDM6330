import requests
import pandas as pd
import json

#Declaring API
url = "https://api.eia.gov/v2/electricity/retail-sales/data/"

#Parameters from EIA
params = {
    "frequency": "monthly",
    "data[0]": "customers",
    "data[1]": "price",
    "data[2]": "revenue",
    "data[3]": "sales",
    "start": "2001-01",
    "end": "2025-01",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": 0,
    "length": 5000,
    "api_key": "UJTVnGeM5ruvaNk9th2NeNPWthknAHmPOJ58vTjI"
}

try:
    #Attempt the GET Request 
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        records = data['response']['data']
        
        # Convert to a Pandas DataFrame for easy viewing
        df = pd.DataFrame(records)
        
        # Print the first few rows to verify
        print("Data successfully retrieved!")
        print(df.head())
        
        # Option: Save to CSV for use in Alteryx or Excel
        df.to_csv("electricity_sales_data.csv", index=False)
        print("Data saved to electricity_sales_data.csv")
        
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")
