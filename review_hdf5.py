import h5py
import numpy as np
from random import randint
import matplotlib.pyplot as plt


def review_hdf5(file_path, num_samples=5):
    with h5py.File(file_path, 'r') as hf:
        # List all datasets in the file
        print("Datasets in the file:")
        for name in hf:
            print(name)
        
        # Load datasets
        magnitudes = hf['magnitudes']
        latitudes = hf['latitudes'][:]
        longitudes = hf['longitudes'][:]
        datetimes = hf['datetimes'][:]

        # Print metadata
        print(f"\nNumber of time steps: {magnitudes.shape[0]}")
        print(f"Latitude range: {latitudes[0]} to {latitudes[-1]}")
        print(f"Longitude range: {longitudes[0]} to {longitudes[-1]}")
        print("Datetimes:")
        for dt in datetimes:
            print(dt.decode('utf-8'))

        # Choose a specific time step to review
        time_step = 0  # Change this to review different time steps
        time_step = randint(0,magnitudes.shape[0])
        datetime_str = datetimes[time_step].decode("utf-8")
        magnitude_data = magnitudes[time_step, :, :]

        # Print the shape and some sample values of the magnitude data
        print(f"\nReviewing data for timestamp: {datetime_str}")
        print(f"Shape of magnitude data: {magnitude_data.shape}")
        print(f"Number of non-NaN entries: {np.count_nonzero(~np.isnan(magnitude_data))}")
        
        # Generate random indices and sample data values
        print("\nSample data values (latitude, longitude, magnitude):")
        num_rows, num_cols = magnitude_data.shape
        random_indices = np.random.choice(num_rows * num_cols, num_samples, replace=False)
        for idx in random_indices:
            row, col = divmod(idx, num_cols)
            lat = latitudes[row]
            lon = longitudes[col]
            value = magnitude_data[row, col]
            print(f"({lat:.2f}, {lon:.2f}): {value}")

        # Plot data for the specific time step
        output_file = "outputs/review_hdf5.png"
        plt.figure(figsize=(10, 8))
        plt.imshow(magnitude_data, cmap='viridis', aspect='auto')
        plt.colorbar(label='Rain Magnitude')
        plt.title(f'Rain Magnitude at {datetime_str}')
        plt.show()
        plt.savefig(output_file)
        print("Plot saved:", output_file)


if __name__ == "__main__":
    file_path = "outputs/rainfall_magnitudes.h5"  # Change to your HDF5 file path
    review_hdf5(file_path, num_samples=5)  # Change num_samples to sample different number of points
