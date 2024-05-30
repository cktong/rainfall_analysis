from rainfall_analysis import RainfallAnalyzer
from datetime import datetime, timedelta
import os

def main(start_datetime_str, num_steps, step_interval_minutes):
    color_file = "extracted_colors.json"
    start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
    
    rainfall_analyzer = RainfallAnalyzer(color_file)
    
    for step in range(num_steps):
        current_datetime = start_datetime + timedelta(minutes=step * step_interval_minutes)
        year = current_datetime.strftime("%Y")
        month = current_datetime.strftime("%m")
        day = current_datetime.strftime("%d")
        time = current_datetime.strftime("%H%M")
        datetime_str = f"{year}-{month}-{day}T{time[:2]}:{time[2:]}:00"
        
        # Construct the URL for the image
        url = f"http://www.weather.gov.sg/files/rainarea/50km/v2/dpsri_70km_{year}{month}{day}{time}0000dBR.dpsri.png"
        try:
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
        
        except Exception as e:
            print(f"Failed to process data for {datetime_str}: {e}")

if __name__ == "__main__":
    start_datetime_str = "2024-05-27 14:00"  # Enter the starting date and time here
    num_steps = 12  # Number of steps to query and analyze
    step_interval_minutes = 5  # Interval between steps in minutes
    os.makedirs("outputs", exist_ok=True)
    main(start_datetime_str, num_steps, step_interval_minutes)
