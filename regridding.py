# Import required libraries
import xarray as xr
import xesmf as xe

# 1. Load MERRA-2 data to get target grid
# -----------------------------------------------------------------------------
merra_path = "merra2_data_march/MERRA2_400.tavg1_2d_aer_Nx.20200301.nc4"
merra_ds = xr.open_dataset(merra_path, engine='netcdf4')

# Subset North America region (60N-20N, 140W-50W)
merra_na = merra_ds.sel(
    lat=slice(60, 20),
    lon=slice(-140, -50)
)

# 2. Load ERA5 data
# -----------------------------------------------------------------------------
era_path = "data_stream-oper_stepType-accum.nc"
era_ds = xr.open_dataset(era_path)

# Subset same region (coordinates might have different names)
era_na = era_ds.sel(
    latitude=slice(60, 20),
    longitude=slice(-140, -50)
)

# 3. Create regridder
# -----------------------------------------------------------------------------
# Create target grid from MERRA-2 coordinates
target_grid = xr.Dataset({
    'lat': (['lat'], merra_na.lat.values),
    'lon': (['lon'], merra_na.lon.values)
})

# Create conservative regridder (preserves energy during regridding)
regridder = xe.Regridder(
    era_na, 
    target_grid,
    'conservative',
    periodic=True  # Important for global datasets
)

# 4. Regrid ERA5 data
# -----------------------------------------------------------------------------
# Apply regridding to SSRD variable
ssrd_regridded = regridder(era_na['ssrd'])

# Convert from accumulated J/m² to W/m²
ssrd_regridded = ssrd_regridded / 3600  # 1 hour = 3600 seconds

# Add coordinate metadata
ssrd_regridded = ssrd_regridded.assign_attrs({
    'long_name': 'Surface solar radiation downwards',
    'units': 'W/m²'
})

# 5. Save regridded data
# -----------------------------------------------------------------------------
output_path = "ERA5_SSRD_regridded_to_MERRA2_NA.nc"
ssrd_regridded.to_netcdf(output_path)

print(f"Regridding complete! Saved to {output_path}")
