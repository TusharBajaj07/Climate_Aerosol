import cdsapi

c = cdsapi.Client()

# Define regions (adjusted for March-April 2020 focus)
regions = {
   #"southeast_asia": [30, 90, -15, 150],  # [North, West, South, East]
    "north_america": [60, -140, 20, -50]
}

# Download hourly data for March-April 2020
for region_name, coordinates in regions.items():
    c.retrieve(
        'reanalysis-era5-single-levels',  # Hourly dataset
        {
            'product_type': 'reanalysis',
            'variable': [
                '2m_temperature',
                'total_precipitation',
                'surface_solar_radiation_downwards'
            ],
            'year': '2020',
            'month': ['03'],  # March-April
            'day': [f'{d:02d}' for d in range(1,32)],  # All days (1-31)
            'time': [f'{h:02d}:00' for h in range(24)],  # All hours
            'area': coordinates,
            'format': 'netcdf',
        },
        f'era5_{region_name}_hourly_202003-202004.nc'
    )

print("Download requests submitted! Track progress at:")
print("https://cds.climate.copernicus.eu/cdsapp#!/yourrequests")

