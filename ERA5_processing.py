import xarray as xr

# Load dataset
era5_ds = xr.open_dataset('ERA5_ssrd_regridded.nc')

# Verify latitude values
print("Original latitude range:", era5_ds.lat.values[[0, -1]])

# Reverse slice order for descending latitudes
north_america_era5 = era5_ds.sel(
    lat=slice(20, 60),    # Low to high (for descending coordinates)
    lon=slice(-140, -50)  # Normal west to east
)
ssrd_north_america = north_america_era5['ssrd']

# Save the subsetted data for further use (optional)
ssrd_north_america.to_netcdf('era5_north_america_ssrd.nc')

print(f"ERA5 subsetting complete. Shape of subsetted SSRD data: {ssrd_north_america.shape}")
# Check results
print("Subset latitude values:", north_america_era5.lat.values)
print("Subset dimensions:", north_america_era5['ssrd'].shape)
