import xarray as xr

# Load the .nc4 file
file_path = 'merra2_north_america_aot.nc4'  # Replace with your file path
ds = xr.open_dataset(file_path)

# Print dataset structure
print(ds)

# List all variables in the dataset
print("\nVariables in the dataset:")
print(list(ds.data_vars))

# Check dimensions of the dataset
print("\nDimensions:")
print(ds.dims)

# Example: Inspect aerosol-related variables
aerosol_vars = [var for var in ds.data_vars if 'aerosol' in var.lower() or 'aer' in var.lower()]
print("\nAerosol-related variables:")
print(aerosol_vars)

# If you want to inspect a specific variable (e.g., 'TOTEXTTAU' for total aerosol optical thickness)
if 'TOTEXTTAU' in ds.data_vars:
    print("\nDetails of TOTEXTTAU variable:")
    print(ds['TOTEXTTAU'])  # Replace with your desired aerosol variable name

# Visualize metadata (attributes) for a variable
if 'TOTEXTTAU' in ds.data_vars:
    print("\nAttributes of TOTEXTTAU:")
    print(ds['TOTEXTTAU'].attrs)
