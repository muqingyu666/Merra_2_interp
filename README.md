# MERRA-2 Data Interpolation and Processing Tool 🌍📊

Welcome to the **MERRA-2 Data Interpolation and Processing Tool**! This tool is designed to make working with MERRA-2 reanalysis data easier and more flexible. Whether you need to interpolate irregular 0.5˚×0.625˚ data to a clean 1˚×1˚ grid, compute daily averages, or customize the processing pipeline, this tool has you covered. Let’s dive in! 🚀

---

## What Does This Tool Do? 🤔

This tool takes MERRA-2 aerosol diagnostic data (which comes in an irregular 0.5˚×0.625˚ grid) and **interpolates it to a uniform grid** of your chosen resolution (default is 1˚×1˚). It also calculates the **daily average** of the data, making it ready for analysis or modeling. The interpolation method is **cubic spline** by default, but you can customize it to use other methods like linear interpolation.

---

## Why Use This Tool? 🚀

- **Handle Irregular Grids**: Convert MERRA-2’s 0.5˚×0.625˚ grid to a uniform grid that’s easier to work with. 🗺️
- **Daily Averages**: Automatically compute daily means for your data. 📅
- **Fully Customizable**: Define your own grid, select specific variables, preprocess data, and more. 🛠️
- **Save Time**: Automate repetitive tasks and focus on your analysis. ⏱️

---

## Key Features ✨

### 1. **Custom Grid Definition**
   - Set your own latitude and longitude range (`lat_range`, `lon_range`).
   - Choose the resolution of the output grid (`resolution`).

### 2. **Flexible Interpolation**
   - Use cubic spline, linear, or other interpolation methods (`interpolation_method`).

### 3. **Variable Selection**
   - Extract only the variables you need (`variables`).

### 4. **Preprocessing and Postprocessing**
   - Apply custom preprocessing steps (e.g., unit conversion, filtering) with `preprocess_func`.
   - Add metadata or compute derived variables before saving with `postprocess_func`.

### 5. **Custom File Naming**
   - Define your own file naming convention with `file_naming_func`.

### 6. **Efficient Processing**
   - Process data year by year to reduce memory usage.
   - Save results to NetCDF files for easy access and sharing.

---

## How to Use 🛠️

### Installation
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install numpy pandas xarray
   ```

### Basic Usage
Run the script with default parameters:
```python
extract_merra2_data_and_interp(
    start_date="2010-01-01",
    end_date="2020-12-31",
    data_dir="/path/to/merra2/data",
    output_dir="/path/to/output",
)
```

### Custom Usage
Customize the tool to fit your needs:
```python
# Example: Custom grid, variables, and preprocessing
extract_merra2_data_and_interp(
    start_date="2010-01-01",
    end_date="2020-12-31",
    lat_range=(-60, 60),
    lon_range=(-120, 120),
    resolution=0.5,
    interpolation_method="linear",
    variables=["variable1", "variable2"],
    preprocess_func=my_preprocess_function,
    postprocess_func=my_postprocess_function,
    file_naming_func=my_file_naming_function,
)
```

---

## Example Use Cases 🌟

### 1. **Interpolate to a Specific Region**
   - Set `lat_range` and `lon_range` to focus on a specific geographic area.

### 2. **Extract Specific Variables**
   - Use the `variables` parameter to extract only the variables you need.

### 3. **Unit Conversion**
   - Apply a `preprocess_func` to convert units or filter data.

### 4. **Add Metadata**
   - Use a `postprocess_func` to add metadata or compute derived variables.

---

## Output 📂
The tool saves the processed data as yearly NetCDF files in the specified `output_dir`. Each file contains the interpolated and daily-averaged data for the corresponding year.

Example output file:  
`merra_2_daily_2011.nc`

---

## Customization Options 🎨

### 1. **File Naming**
   - Define a custom function (`file_naming_func`) to generate input file names based on dates.

### 2. **Preprocessing**
   - Use `preprocess_func` to apply transformations (e.g., unit conversion, filtering) before interpolation.

### 3. **Postprocessing**
   - Use `postprocess_func` to add metadata or compute derived variables before saving.

### 4. **Variable Selection**
   - Specify a list of variables (`variables`) to extract from the dataset.

---

## Requirements 🧰
- Python 3.8+
- Libraries: `numpy`, `pandas`, `xarray`

---

## License 📜
This project is open-source and available under the **MIT License**. Feel free to use, modify, and share it!

---

## Contributions Welcome! 🤝
Found a bug? Have an idea for improvement? Open an issue or submit a pull request. Let’s make this tool even better! 💪

---

## Questions or Feedback? 📬
Reach out to [muqy20@lzu.edu.cn](mailto:muqy20@lzu.edu.cn). We’d love to hear from you!

---

Happy data processing! 🎉  
Let’s make working with MERRA-2 data a breeze! 🌬️
