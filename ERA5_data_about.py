import xarray as xr
import pandas as pd

# Load the dataset
ds = xr.open_dataset('era5_north_america_ssrd.nc')

# Basic overview
print("=== Dataset Structure ===")
print(ds)

# Detailed time analysis
print("\n=== Time Analysis ===")
time_var = ds['valid_time']
print(f"Time dimension name: {time_var.dims[0]}")
print(f"Number of time steps: {len(time_var)}")
print(f"Start time: {pd.to_datetime(time_var.min().values).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"End time: {pd.to_datetime(time_var.max().values).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Temporal resolution: {pd.infer_freq(time_var.to_index())}")

# Spatial analysis
print("\n=== Spatial Analysis ===")
print(f"Latitude range: {ds.latitude.min().item():.2f}°N to {ds.latitude.max().item():.2f}°N")
print(f"Longitude range: {ds.longitude.min().item():.2f}°E to {ds.longitude.max().item():.2f}°E")
print(f"Spatial resolution: {abs(ds.latitude[1] - ds.latitude[0]).item():.2f}° (lat) x {abs(ds.longitude[1] - ds.longitude[0]).item():.2f}° (lon)")

# Variable details
print("\n=== Variable Details ===")
print("Variables available:")
for var in ds.data_vars:
    print(f"- {var}: {ds[var].attrs.get('long_name', 'No description available')}")
    print(f"  Units: {ds[var].attrs.get('units', 'Not specified')}")
    print(f"  Shape: {ds[var].shape}")

# Special parameters analysis
print("\n=== Special Parameters ===")
print(f"expver unique values: {ds['expver'].values} (ECMWF experiment version)")
print(f"number unique values: {ds['number'].values} (Ensemble member numbers)")

# Data quality check
print("\n=== Data Quality ===")
print(f"Missing values in ssrd: {ds['ssrd'].isnull().sum().item()}")
print(f"Missing values in tp: {ds['tp'].isnull().sum().item()}")
print(f"ssrd value range: {ds['ssrd'].min().item():.2f} to {ds['ssrd'].max().item():.2f}")
print(f"tp value range: {ds['tp'].min().item():.2f} to {ds['tp'].max().item():.2f}")
