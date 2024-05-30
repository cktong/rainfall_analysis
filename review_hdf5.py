import h5py
import numpy as np
import matplotlib.pyplot as plt

def review_hdf5(file_path):
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
        datetime_str = datetimes[time_step].decode("utf-8")
        magnitude_data = magnitudes[time_step, :, :]

        # Print the shape and some sample values of the magnitude data
        print(f"\nReviewing data for timestamp: {datetime_str}")
        print(f"Shape of magnitude data: {magnitude_data.shape}")
        print(f"Number of non-NaN entries: {np.count_nonzero(~np.isnan(magnitude_data))}")
        
        # Sample some data values
        print("\nSample data values:")
        sample_indices = [(0, 0), (10, 10), (20, 20), (30, 30)]  # Change or extend as needed
        for idx in sample_indices:
            value = magnitude_data[idx]
            print(f"Value at index {idx}: {value}")

        output_file = "outputs/review_hdf5.png"
        # Plot data for the specific time step
        plt.figure(figsize=(10, 8))
        plt.imshow(magnitude_data, cmap='viridis', aspect='auto')
        plt.colorbar(label='Rain Magnitude')
        plt.title(f'Rain Magnitude at {datetime_str}')
        plt.show()
        plt.savefig(output_file)
        print("Plot saved:", output_file)


if __name__ == "__main__":
    file_path = "outputs/rainfall_magnitudes.h5"  # Change to your HDF5 file path
    review_hdf5(file_path)
