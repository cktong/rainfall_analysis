from PIL import Image
import numpy as np
import json
import requests
import io
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import h5py
import os

# Define a class to map RGB colors to magnitudes automatically
class AutoColormap:
    def __init__(self, rgb_colors):
        self.rgb_colors = rgb_colors
        self.rgb_array = np.array(rgb_colors) / 255.0  # Normalize RGB values to [0, 1]
        self.num_colors = len(rgb_colors)

    def to_magnitude(self, rgb_value):
        # Find the index of the closest RGB color
        idx = np.argmin(np.linalg.norm(self.rgb_array - (rgb_value / 255.0), axis=1))
        # Return the corresponding magnitude, starting from 1
        return idx + 1

class RainfallAnalyzer:
    def __init__(self, color_file):
        self.extracted_colors = self.load_colors(color_file)
        self.auto_cmap = AutoColormap(self.extracted_colors)
        self.cmap = ListedColormap(np.array(self.extracted_colors) / 255.0)
        self.min_lat, self.max_lat = 1.47, 1.14
        self.min_lon, self.max_lon = 103.55, 104.1

    def load_colors(self, color_file):
        with open(color_file, "r") as file:
            extracted_colors = json.load(file)
        extracted_colors.reverse()
        return extracted_colors

    def fetch_image(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            image_bytes = response.content
            return Image.open(io.BytesIO(image_bytes))
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def analyze_rainfall(self, image):
        rain_data = np.array(image)
        num_rows, num_cols = rain_data.shape[:2]
        latitudes = np.linspace(self.min_lat, self.max_lat, num_rows)
        longitudes = np.linspace(self.min_lon, self.max_lon, num_cols)
        magnitude = np.empty([num_rows, num_cols])

        for i in range(num_rows):
            for j in range(num_cols):
                rgb_value = rain_data[i, j][:3]
                if sum(rgb_value) == 0:
                    magnitude[i, j] = np.NaN
                else:
                    magnitude[i, j] = self.auto_cmap.to_magnitude(rgb_value)
        
        return magnitude, latitudes, longitudes

    def save_geojson(self, magnitudes, latitudes, longitudes, output_file):
        features = []
        num_rows, num_cols = magnitudes.shape

        for i in range(num_rows):
            for j in range(num_cols):
                if not np.isnan(magnitudes[i, j]):
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [longitudes[j], latitudes[i]]
                        },
                        "properties": {
                            "magnitude": magnitudes[i, j]
                        }
                    }
                    features.append(feature)

        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }
        
        with open(output_file, "w") as f:
            json.dump(geojson_data, f, indent=2)
        print("GeoJSON file saved:", output_file)

    def plot_magnitude(self, magnitude, output_file, title):
        plt.figure(figsize=(10, 8))
        plt.imshow(magnitude, cmap=self.cmap, aspect='auto')
        plt.colorbar(label='Rain Magnitude')
        plt.title(title)
        plt.show()
        plt.savefig(output_file)
        print("Plot saved:", output_file)

    def save_hdf5(self, magnitudes, latitudes, longitudes, datetime_str, output_file):
        if not os.path.exists(output_file):
            with h5py.File(output_file, 'w') as hf:
                hf.create_dataset('magnitudes', data=magnitudes[np.newaxis, ...], maxshape=(None, magnitudes.shape[0], magnitudes.shape[1]))
                hf.create_dataset('latitudes', data=latitudes)
                hf.create_dataset('longitudes', data=longitudes)
                hf.create_dataset('datetimes', data=np.array([datetime_str], dtype='S'))
        else:
            with h5py.File(output_file, 'a') as hf:
                magnitudes_ds = hf['magnitudes']
                magnitudes_ds.resize((magnitudes_ds.shape[0] + 1, magnitudes_ds.shape[1], magnitudes_ds.shape[2]))
                magnitudes_ds[-1] = magnitudes

                datetimes_ds = hf['datetimes']
                datetimes_ds.resize((datetimes_ds.shape[0] + 1,))
                datetimes_ds[-1] = np.string_(datetime_str)

        print("HDF5 file saved/appended:", output_file)
