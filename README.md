# Climate-Aerosol Interaction Analysis

## Project Overview
This repository analyzes the relationship between aerosol optical depth (AOD) and surface solar radiation downwards (SSRD) across North America using ERA5 and MERRA-2 reanalysis data from March 2020.

## Key Findings
- Central United States shows pronounced negative relationship between AOD and SSRD (aerosol dimming effect)
- Gulf of Mexico coastal regions display some positive relationships
- Northern regions show moderate negative relationships
- Western coastal areas exhibit mixed patterns

![North America Heat Map: SSRD vs. AOD Sensitivity](/heatmap.jpg)

## Data Sources
- **ERA5 Reanalysis**: Hourly data (t2m, tp, ssrd)
- **MERRA-2 (M2T1NXAER)**: Aerosol optical depth data

## Methodology
1. **Data Preprocessing**:
   - Regridding ERA5 data to match MERRA2's resolution
   - North America domain focus (20°N-60°N, 140°W-50°W)
   - Merging 30 days of hourly data

2. **Statistical Analysis**:
   - Linear regression
   - SVM models with RBF and linear kernels
   - Grid-specific analysis
   - Outlier filtering for sparse data regions

## Repository Structure
- **`gridding_check.py`**: Validates spatial harmonization
- **Preprocessing Scripts**: Data retrieval and preparation
- **`Model_Climate.ipynb`**: Main analysis notebook

## Requirements
- Python 3.x
- Libraries: xarray, numpy, pandas, scikit-learn, matplotlib, cartopy
- Climate Data Operators (CDO)
