import os
import numpy as np
import pandas as pd
import xarray as xr
from pathlib import Path
from typing import List, Optional, Callable

############################################################################################################

def extract_merra2_data_and_interp(
    start_date: str,
    end_date: str,
    data_dir: str = "/RAID01/data/merra2",
    output_dir: str = "/RAID01/data/merra2",
    lat_range: tuple = (-90, 90),
    lon_range: tuple = (-180, 180),
    resolution: float = 1.0,
    interpolation_method: str = "cubic",
    file_naming_func: Optional[Callable[[pd.Timestamp], str]] = None,
    variables: Optional[List[str]] = None,
    preprocess_func: Optional[Callable[[xr.Dataset], xr.Dataset]] = None,
    postprocess_func: Optional[Callable[[xr.Dataset], xr.Dataset]] = None,
):
    """
    Extract MERRA-2 data, interpolate it to a custom resolution, compute daily means,
    and save the results to yearly NetCDF files.

    Parameters:
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        data_dir (str): Directory containing MERRA-2 data files.
        output_dir (str): Directory to save the output NetCDF files.
        lat_range (tuple): Latitude range for interpolation (min, max).
        lon_range (tuple): Longitude range for interpolation (min, max).
        resolution (float): Resolution for the output grid (in degrees).
        interpolation_method (str): Interpolation method (e.g., 'linear', 'cubic').
        file_naming_func (Callable): Function to generate input file names from dates.
        variables (List[str]): List of variables to extract. If None, all variables are used.
        preprocess_func (Callable): Function to preprocess the dataset before interpolation.
        postprocess_func (Callable): Function to postprocess the dataset before saving.
    """
    # Generate date range
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    # Predefine new latitude and longitude for interpolation
    new_lat = np.arange(lat_range[0], lat_range[1], resolution)
    new_lon = np.arange(lon_range[0], lon_range[1], resolution)

    # Process data year by year
    for year in range(dates[0].year, dates[-1].year + 1):
        year_dir = Path(data_dir) / str(year)
        daily_mean_data_list = []

        # Filter dates for the current year
        year_dates = dates[dates.year == year]

        for date in year_dates:
            # Generate file name using the custom function or default logic
            if file_naming_func:
                file_name = file_naming_func(date)
            else:
                if year == 2010:
                    file_name = f"MERRA2_300.tavg1_2d_aer_Nx.{date.strftime('%Y%m%d')}.nc4"
                elif year == 2020 and date.month == 9:
                    file_name = f"MERRA2_401.tavg1_2d_aer_Nx.{date.strftime('%Y%m%d')}.nc4"
                else:
                    file_name = f"MERRA2_400.tavg1_2d_aer_Nx.{date.strftime('%Y%m%d')}.nc4"

            file_path = year_dir / file_name

            if file_path.exists():
                # Open the dataset
                with xr.open_dataset(file_path) as data:
                    # Preprocess the dataset (if provided)
                    if preprocess_func:
                        data = preprocess_func(data)

                    # Select specific variables (if provided)
                    if variables:
                        data = data[variables]

                    # Interpolate the data
                    interp_data = data.interp(
                        lat=new_lat, lon=new_lon, method=interpolation_method
                    )

                    # Compute daily mean and append to list
                    daily_mean_data = interp_data.mean(dim="time", skipna=True)
                    daily_mean_data_list.append(daily_mean_data)

        # Concatenate and save yearly data
        if daily_mean_data_list:
            daily_mean_data_all = xr.concat(daily_mean_data_list, dim="time")
            daily_mean_data_all["time"] = year_dates

            # Postprocess the dataset (if provided)
            if postprocess_func:
                daily_mean_data_all = postprocess_func(daily_mean_data_all)

            # Save the output
            output_file_path = Path(output_dir) / f"merra_2_daily_{year}.nc"
            daily_mean_data_all.to_netcdf(output_file_path)
            print(f"Saved {output_file_path}")

# Example of a custom file naming function
def custom_file_naming(date: pd.Timestamp) -> str:
    if date.year == 2010:
        return f"MERRA2_300.tavg1_2d_aer_Nx.{date.strftime('%Y%m%d')}.nc4"
    elif date.year == 2020 and date.month == 9:
        return f"MERRA2_401.tavg1_2d_aer_Nx.{date.strftime('%Y%m%d')}.nc4"
    else:
        return f"MERRA2_400.tavg1_2d_aer_Nx.{date.strftime('%Y%m%d')}.nc4"

# Example of a preprocessing function
def preprocess_data(dataset: xr.Dataset) -> xr.Dataset:
    # Example: Convert units or filter data
    dataset["variable_name"] = dataset["variable_name"] * 1.0  # Example operation
    return dataset

# Example of a postprocessing function
def postprocess_data(dataset: xr.Dataset) -> xr.Dataset:
    # Example: Add metadata or compute additional variables
    dataset.attrs["description"] = "Processed MERRA-2 data"
    return dataset

############################################################################################################

if __name__ == "__main__":
    # Execute the function with custom parameters
    extract_merra2_data_and_interp(
        start_date="2010-01-01",
        end_date="2020-12-31",
        data_dir="/RAID01/data/merra2",
        output_dir="/RAID01/data/merra2/output",
        lat_range=(-90, 90),
        lon_range=(-180, 180),
        resolution=1.0,
        interpolation_method="cubic",
        file_naming_func=custom_file_naming,
        variables=["variable1", "variable2"],  # Specify variables to extract
        preprocess_func=preprocess_data,      # Custom preprocessing
        postprocess_func=postprocess_data,    # Custom postprocessing
    )
