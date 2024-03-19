import sys
import tkinter
import math
import numpy as np
import matplotlib.pyplot as plt
import os

from tkinter import filedialog
from matplotlib.widgets import Button

plot_x = 1 # Default x coordinate for initial spectrum
plot_y = 1
selected_area_begin = 600 # Default lower energy limit in area summation for mapping plot
selected_area_end = 700

output = "output"  # Output folder for saving data

# Create the output folder if it doesn't exist
if not os.path.exists(output):
    os.makedirs(output)

def import_data():
    root = tkinter.Tk()
    root.withdraw()
    file_path = tkinter.filedialog.askopenfilename(
        title = "Select a raw data file (.csv).",
        filetypes = [("(*.csv) file", "*.csv"), ("All files", "*.*")]
    )
    if not file_path:
        sys.exit("Error: No file selected.")
    file_name = file_path.split("/")[-1]
    file_directory = "/".join(file_path.split("/")[:-1])
    print("Selected file is \'" + file_name + "\'")

    with open(file_path, 'r') as file:
        raw_data = file.read()
    rows = raw_data.strip().split("\n")
    separated_data = [row.strip().split(",") for row in rows]
    PIXEL_COUNT: int = int(math.sqrt(len(rows) - 1))
    sliced_result = np.array(np.array(separated_data)[:, 3:-1], dtype=float)
    return sliced_result, PIXEL_COUNT

def select_area(selected_area_begin = None, selected_area_end = None):
    selection_mask = (spectrum_energy >= selected_area_begin) & (spectrum_energy <= selected_area_end)
    print(selection_mask, selection_mask.sum())
    return selection_mask

# Function to save 2D array to CSV file
def export_2d_data(data, file_path):
    np.savetxt(file_path, data, delimiter=",")

# Function to save spectrum data to CSV file
def export_spectrum_data(x_data, y_data, file_path):
    with open(file_path, 'w') as file:
        file.write("Energy,Intensity\n")
        for x, y in zip(x_data, y_data):
            file.write(f"{x},{y}\n")

# Function to handle export button click for mapping plot
def export_mapping(output_folder = output):
    file_path = tkinter.filedialog.asksaveasfilename(
        initialdir=output_folder,
        title="Save Integrated Area Data",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        export_2d_data(integrated_area_baseline_subtract, file_path)
        print(f"Integrated area data saved to: {file_path}")

# Function to handle export button click for spectrum
def export_spectrum(output_folder = output):
    file_path = tkinter.filedialog.asksaveasfilename(
        initialdir=output_folder,
        title="Save Spectrum Data",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        export_spectrum_data(spectrum_energy, spectrum_intensity, file_path)
        print(f"Spectrum data saved to: {file_path}")

result, PIXEL_COUNT = import_data()
print("A size of selected file is " + str(PIXEL_COUNT) + " x " + str(PIXEL_COUNT))

# Initial plot for spectrum
spectrum_energy = result[0]
selection_mask = select_area(selected_area_begin, selected_area_end)
line_number = int(plot_x * PIXEL_COUNT + plot_y)
spectrum_intensity = result[line_number]

def find_index_baseline(arr = spectrum_energy, selected_area_begin : int = selected_area_begin, selected_area_end : int = selected_area_end):
    baseline_left_index = None
    baseline_right_index = None
    for j, num in enumerate(spectrum_energy):
        if num <= selected_area_begin:
            if baseline_left_index is None or spectrum_energy[j] > spectrum_energy[baseline_left_index]:
                baseline_left_index = j
    for i, num in enumerate(spectrum_energy):
        if num >= selected_area_end:
            if baseline_right_index is None or spectrum_energy[i] < spectrum_energy[baseline_right_index]:
                baseline_right_index = i
    return baseline_left_index, baseline_right_index

# Calculate total area from the selected energy range
selected_point_count = selection_mask.sum()
integrated_area = np.zeros((PIXEL_COUNT, PIXEL_COUNT))
integrated_area_baseline_subtract = np.zeros((PIXEL_COUNT, PIXEL_COUNT))
i = 0
for y in range(PIXEL_COUNT):
    for x in range(PIXEL_COUNT):
        integrated_area[x, y] = (result[i + 1] * selection_mask).sum()
        baseline_left = result[i + 1][find_index_baseline(result[i + 1])[0]]
        baseline_right = result[i + 1][find_index_baseline(result[i + 1])[1]]
        integrated_area_baseline_subtract[x, y] = integrated_area[x, y] - (selected_point_count * (baseline_left + baseline_right) * 0.5)
        i += 1

# Accumulate the count in the file name
count = 0  # Added to keep track of the count
output_file_dir = "output"  # Added to specify the output folder
os.makedirs(output_file_dir, exist_ok=True)  # Added to create the output folder if it doesn't exist
output_file_path = os.path.join(output, f"data_plot_{plot_x}_{plot_y}_{count}.txt")  # Modified to include plot_x and plot_y
while os.path.exists(output_file_path):  # Added to check for existing files and increment count if necessary
    count += 1  # Increment count
    output_file_path = os.path.join(output, f"data_plot_{plot_x}_{plot_y}_{count}.txt")  # Modified to include plot_x and plot_y

# Save data to the output file
with open(output_file_path, 'w') as file:  # Modified to use the calculated output file path
    file.write("X\tY\n")
    for x, y in zip(spectrum_energy, spectrum_intensity):
        file.write(f"{x}\t{y}\n")

# Plot the rotated image with adjusted intensity range
fig, axs = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={'width_ratios': [3, 2]})

im = axs[0].imshow(integrated_area_baseline_subtract, interpolation='none', aspect='equal')
fig.colorbar(im, ax=axs[0], label='Intensity (a.u)')  # Add color bar indicating intensity
axs[0].set_xlabel('')  # Label for the x-axis
axs[0].set_ylabel('')  # Label for the y-axis
axs[0].set_title(f'{selected_area_begin} ~ {selected_area_end} nm')  # Title for the plot

axs[1].plot(spectrum_energy, spectrum_intensity)
axs[1].set_title(f'({plot_x}, {plot_y}) spectrum')  # Title for the plot

# Create export buttons
button_export_mapping = Button(plt.axes([0.01, 0.2, 0.07, 0.1]), "Export\nmapping")
button_export_mapping.on_clicked(export_mapping)
button_export_spectrum = Button(plt.axes([0.01, 0.05, 0.07, 0.1]), "Export\nspectrum")
button_export_spectrum.on_clicked(export_spectrum)

def onclick(event):
    global plot_x, plot_y, spectrum_intensity
    if event.inaxes == axs[0]:  # Event check for click in subplot[0]
        x_index = int(event.xdata)
        y_index = int(event.ydata)
        print(f'Clicked at (x={x_index}, y={y_index})')  # Print coordinate from mouse click
        plot_x = x_index  # Update coordinate
        plot_y = y_index

        # Update spectrum number
        line_number = int(plot_x * PIXEL_COUNT + plot_y)
        spectrum_intensity = result[line_number]

        # Update subplot[1]
        axs[1].clear()
        axs[1].plot(spectrum_energy, spectrum_intensity)
        axs[1].set_title(f'({plot_x}, {plot_y}) spectrum')  # Title for the plot
        axs[1].set_xlabel('Energy')  # Label for the x-axis
        axs[1].set_ylabel('Intensity')  # Label for the y-axis
        axs[1].set_ylim(-200, 2500)

        plt.draw()

# Sync mouse click event
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()