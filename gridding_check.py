import xarray as xr
import matplotlib.pyplot as plt

# Load the ERA5 dataset (replace 'era5_data.nc' with your file path)
dataset = xr.open_dataset('ERA5_ssrd.nc')

# Select the 'ssrd' variable
ssrd = dataset['ssrd']

# Choose a specific time frame (e.g., first time step)
time_index = 41  # Change this index to select a different time frame
selected_time = ssrd.isel(valid_time=time_index)

# Plot the heatmap
plt.figure(figsize=(12, 6))
selected_time.plot(cmap='viridis', cbar_kwargs={'label': 'SSRD (J m⁻²)'})
plt.title(f"SSRD Heatmap at Time: {str(selected_time.valid_time.values)}")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
