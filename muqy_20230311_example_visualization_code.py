import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# -------------------------- Data Loading --------------------------
def load_merra2_data(file_paths):
    """
    Load MERRA-2 data from a list of NetCDF files.

    Parameters:
        file_paths (list): List of file paths to MERRA-2 NetCDF files.

    Returns:
        xr.Dataset: Combined MERRA-2 dataset.
    """
    print("Loading MERRA-2 data...")
    return xr.open_mfdataset(file_paths, combine="by_coords")


# -------------------------- Data Preprocessing --------------------------
def preprocess_data(data, variable, start_year, end_year):
    """
    Preprocess MERRA-2 data:
    1. Compute decadal averages.
    2. Compute annual anomalies.
    3. Calculate latitude-band averages.

    Parameters:
        data (xr.Dataset): MERRA-2 dataset.
        variable (str): Variable to process (e.g., "DUEXTT25").
        start_year (int): Start year for analysis.
        end_year (int): End year for analysis.

    Returns:
        tuple: Contains decadal mean, annual mean, anomalies, and latitude-band averages.
    """
    print("Preprocessing data...")

    # Select data for the specified time range
    data = data.sel(time=slice(str(start_year), str(end_year)))

    # Compute decadal mean (2010-2019)
    decadal_mean = data[variable].sel(time=slice("2010", "2019")).mean(dim="time")

    # Compute annual mean for 2020
    annual_mean = data[variable].sel(time="2020").mean(dim="time")

    # Compute long-term mean (2010-2020)
    long_term_mean = data[variable].mean(dim="time")

    # Compute anomalies
    anomalies = data[variable] - long_term_mean

    # Compute latitude-band averages (20N to 50N)
    lat_band_means = [
        anomalies.sel(lat=slice(20, 50), time=str(year)).mean(dim=["lat", "time"]).values
        for year in range(start_year, end_year + 1)
    ]

    return decadal_mean, annual_mean, anomalies, lat_band_means


# -------------------------- Plotting Functions --------------------------
def plot_spatial_data(data, title, variable_name, cmap="RdBu_r"):
    """
    Plot spatial data on a global map.

    Parameters:
        data (xr.DataArray): Data to plot.
        title (str): Plot title.
        variable_name (str): Variable name for the colorbar label.
        cmap (str): Colormap for the plot.
    """
    print("Plotting spatial data...")

    # Set up the plot
    plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    ax.set_facecolor("silver")

    # Plot the data
    mesh = ax.pcolormesh(
        data.lon, data.lat, data, transform=ccrs.PlateCarree(), cmap=cmap
    )

    # Add coastlines and gridlines
    ax.coastlines(resolution="50m", linewidth=0.9)
    gl = ax.gridlines(linestyle="-.", linewidth=0.2, alpha=0.5, draw_labels=True)
    gl.top_labels = False

    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation="vertical", shrink=0.65, extend="both")
    cbar.set_label(variable_name, size=14)
    cbar.ax.tick_params(labelsize=12)

    # Add title
    plt.title(title, fontsize=16)

    plt.show()


def plot_time_series(data, years, title, ylabel):
    """
    Plot a time series of latitude-band averages.

    Parameters:
        data (list): List of latitude-band averages for each year.
        years (list): List of years corresponding to the data.
        title (str): Plot title.
        ylabel (str): Label for the y-axis.
    """
    print("Plotting time series...")

    # Set up the plot
    plt.figure(figsize=(10, 4))
    for i, year in enumerate(years):
        plt.plot(np.linspace(-180, 179, 360), data[i], label=str(year))

    # Add labels and legend
    plt.xlabel("Longitude", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)

    plt.show()


# -------------------------- Main Script --------------------------
if __name__ == "__main__":
    # Define file paths
    file_paths = [
        f"/RAID01/data/merra2/merra_2_daily_{year}.nc" for year in range(2010, 2021)
    ]

    # Load MERRA-2 data
    data = load_merra2_data(file_paths)

    # Preprocess data
    decadal_mean, annual_mean, anomalies, lat_band_means = preprocess_data(
        data, "DUEXTT25", 2010, 2020
    )

    # Plot spatial data: 2020 anomaly
    plot_spatial_data(
        annual_mean - decadal_mean,
        title="Dust AOT at 550nm (2020 - 2010-2019 Mean)",
        variable_name="AOT",
    )

    # Plot time series: Latitude-band averages
    plot_time_series(
        lat_band_means,
        years=range(2010, 2021),
        title="Dust AOT at 550nm (20N-50N Latitude Band)",
        ylabel="Dust AOT at 550nm",
    )
