from rainfall_analysis import RainfallAnalyzer
from datetime import datetime

def main():
    color_file = "extracted_colors.json"
    month, day, year, time = "05", "27", "2024", "1400"
    datetime_str = f"{year}-{month}-{day}T{time[:2]}:{time[2:]}:00"
    
    rainfall_analyzer = RainfallAnalyzer(color_file)
    
    # Construct the URL for the image
    url = f"http://www.weather.gov.sg/files/rainarea/50km/v2/dpsri_70km_{year}{month}{day}{time}0000dBR.dpsri.png"
    image = rainfall_analyzer.fetch_image(url)
    
    # Analyze rainfall
    magnitude, latitudes, longitudes = rainfall_analyzer.analyze_rainfall(image)
    
    # Save GeoJSON
    geojson_output_file = f"outputs/rainfall_magnitude_{year}{month}{day}{time}.geojson"
    rainfall_analyzer.save_geojson(magnitude, latitudes, longitudes, geojson_output_file)
    
    # Plot magnitude
    plot_output_file = f"outputs/rain_magnitude_plot_{year}{month}{day}{time}.png"
    title = f'Rain Levels {year}/{month}/{day} Time: {time}'
    rainfall_analyzer.plot_magnitude(magnitude, plot_output_file, title)

    # Save HDF5 file and append new data
    hdf5_output_file = "outputs/rainfall_magnitudes.h5"
    rainfall_analyzer.save_hdf5(magnitude, latitudes, longitudes, datetime_str, hdf5_output_file)

if __name__ == "__main__":
    main()
