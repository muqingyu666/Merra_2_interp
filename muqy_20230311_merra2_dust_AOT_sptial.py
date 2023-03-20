#                  ___====-_  _-====___
#            _--^^^#####//      \\#####^^^--_
#         _-^##########// (    ) \\##########^-_
#        -############//  |\^^/|  \\############-
#      _/############//   (@::@)   \\############\_
#     /#############((     \\//     ))#############\
#    -###############\\    (oo)    //###############-
#   -#################\\  / VV \  //#################-
#  -###################\\/      \//###################-
# _#/|##########/\######(   /\   )######/\##########|\#_
# |/ |#/\#/\#/\/  \#/\##\  |  |  /##/\#/  \/\#/\#/\#| \|
# `  |/  V  V  `   V  \#\| |  | |/#/  V   '  V  V  \|  '
#    `   `  `      `   / | |  | | \   '      '  '   '
#                     (  | |  | |  )
#                    __\ | |  | | /__
#                   (vvv(VVV)(VVV)vvv)
#                       神兽保佑
#                      代码无BUG!

"""

    Function for utilizing MERRA2 data
    
    Owner: Mu Qingyu
    version 1.0
    Created: 2023-03-11
    
    Including the following parts:

        1) Read in MERRA2 data
        
        2) 

"""

import glob
import os
import re
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib
import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
import xarray as xr

# extract the data from 2010 to 2014 like above
data_merra2 = xr.open_mfdataset(
    [
        "/RAID01/data/merra2/merra_2_daily_2010.nc",
        "/RAID01/data/merra2/merra_2_daily_2011.nc",
        "/RAID01/data/merra2/merra_2_daily_2012.nc",
        "/RAID01/data/merra2/merra_2_daily_2013.nc",
        "/RAID01/data/merra2/merra_2_daily_2014.nc",
        "/RAID01/data/merra2/merra_2_daily_2015.nc",
        "/RAID01/data/merra2/merra_2_daily_2016.nc",
        "/RAID01/data/merra2/merra_2_daily_2017.nc",
        "/RAID01/data/merra2/merra_2_daily_2018.nc",
        "/RAID01/data/merra2/merra_2_daily_2019.nc",
        "/RAID01/data/merra2/merra_2_daily_2020.nc",
    ]
)

# -------------------------- Data preprocessing --------------------------
# 选择2010-2019年的数据
data_decade = data_merra2.sel(time=slice("2010", "2019"))

# 计算"DUEXTT25"变量在2010-2019年的平均值
mean_decade = data_decade["DUEXTT25"].mean(dim=["time"])

# 计算2020年的"DUEXTT25"变量的平均值
mean_2020 = data_merra2.sel(time="2020")["DUEXTT25"].mean(
    dim=["time"]
)

# 计算"DUEXTT25"变量在2010-2020年的时间平均值
mean_data = data_merra2.sel(time=slice("2010", "2021"))[
    "DUEXTT25"
].mean(dim="time")

# 计算每个格点的距平值
anomaly_data = (
    data_merra2.sel(time=slice("2010", "2021"))["DUEXTT25"]
    - mean_data
)

# 计算20N至50N纬度带的平均值，并将结果存储为一个列表
lat_band_mean_list = []
for year in range(2010, 2021):
    lat_band_mean = anomaly_data.sel(
        lat=slice(20, 50), time=f"{year}"
    ).mean(dim=["lat", "time"])
    lat_band_mean_360 = lat_band_mean.values
    lat_band_mean_list.append(lat_band_mean_360)


# ------------------------------ Plotting functions ------------------------------
def plot_spatial_after_interp(
    data,
    var_name,
    title,
):
    mpl.style.use("seaborn-v0_8-ticks")
    mpl.rc("font", family="Times New Roman")

    lon = np.linspace(-180, 179, 360)
    lat = np.linspace(-90, 89, 180)

    lons, lats = np.meshgrid(lon, lat)

    fig, (ax1) = plt.subplots(
        ncols=1,
        nrows=1,
        figsize=(11, 7),
        constrained_layout=True,
    )
    plt.rcParams.update({"font.family": "Times New Roman"})

    ax1 = plt.subplot(
        111,
        projection=ccrs.PlateCarree(central_longitude=0),
    )
    ax1.set_facecolor("silver")
    # ax1.set_global()
    b = ax1.pcolormesh(
        lon,
        lat,
        data,
        transform=ccrs.PlateCarree(),
        cmap="RdBu_r",
    )
    ax1.coastlines(resolution="50m", lw=0.9)
    ax1.set_title(title, fontsize=24)

    gl = ax1.gridlines(
        linestyle="-.", lw=0.2, alpha=0.5, draw_labels=True
    )
    gl.top_labels = False
    cb2 = fig.colorbar(
        b,
        ax=ax1,
        location="right",
        shrink=0.65,
        extend="both",
    )
    cb2.set_label(label=var_name, size=24)
    cb2.ax.tick_params(labelsize=24)

    gl.xlabel_style = {"size": 18}
    gl.ylabel_style = {"size": 18}

    plt.show()


plot_spatial_after_interp(
    data=mean_2020 - mean_decade,
    var_name="AOT",
    title="Dust AOT at 550nm 2020 - 2010-2019",
)


def plot_each_year_dust_lat_mean(lat_mean_dust_lst):
    """plot the lat_mean_dust_lst, means plot each line for each year, the x axis is the longitude, the y axis is the dust AOT at 550nm"""
    mpl.style.use("seaborn-v0_8-ticks")
    mpl.rc("font", family="Times New Roman")

    fig, ax = plt.subplots(figsize=(12, 3))
    plt.rcParams.update({"font.family": "Times New Roman"})

    for i in range(5, 11):
        ax.plot(
            np.linspace(-180, 179, 360),
            lat_mean_dust_lst[i],
            label=f"{2010+i}",
        )

    ax.set_xlabel("Longitude", fontsize=22)
    ax.set_ylabel("Dust AOT at 550nm", fontsize=22)
    ax.tick_params(labelsize=20)

    # 创建新轴并放置图例
    ax.legend(
        loc="center",
        fontsize=14,
        bbox_to_anchor=(1.07, 0.5),
        bbox_transform=ax.transAxes,
    )

    plt.show()


plot_each_year_dust_lat_mean(lat_band_mean_list)
