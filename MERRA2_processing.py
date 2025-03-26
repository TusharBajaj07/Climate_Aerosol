import xarray as xr
import pandas as pd
import glob
import os

# Step 1: Process MERRA-2 files
merra_dir = "merra2_data_march/"
merra_files = sorted(glob.glob(os.path.join(merra_dir, "MERRA2_*.nc4")))

# List to store processed subsets
merra_subsets = []
aot_vars = ['BCEXTTAU', 'DUEXTTAU', 'SSEXTTAU', 'SUEXTTAU', 'TOTEXTTAU']

for file in merra_files:
    ds = xr.open_dataset(file)
    subset = ds.sel(
        lat=slice(20, 60),
        lon=slice(-140, -50)
    )[aot_vars]
    merra_subsets.append(subset)

# Combine all time steps
merra_combined = xr.concat(merra_subsets, dim='time')

# Step 2: Temporal Alignment (MERRA-2 → ERA5 time grid)
merra_combined['time'] = merra_combined.time - pd.Timedelta(minutes=30)

# Step 3: Save with proper encoding
merra_combined.to_netcdf(
    'merra2_north_america_aot.nc4',
    encoding={var: {'dtype': 'float32', 'zlib': True} for var in aot_vars}
)

print(f"MERRA-2 processing complete. Final shape: {merra_combined.dims}")
