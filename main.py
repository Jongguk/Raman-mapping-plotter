import sys
import tkinter
import math
import numpy as np
import matplotlib.pyplot as plt
import os

from tkinter import filedialog

plot_x = 8 # 스펙트럼 뽑을 x 좌표
plot_y = 9 # 스펙트럼 뽑을 y 좌표
selected_area_begin = 540 # 맵핑할때 사용할 면적 범위 시작 (에너지)
selected_area_end = 560 # 맵핑할때 사용할 면적 범위 끝

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

result, PIXEL_COUNT = import_data()
print("A size of selected file is " + str(PIXEL_COUNT) + " x " + str(PIXEL_COUNT))

# Test case for spectrum
spectrum_energy = result[0]
selection_mask = select_area(selected_area_begin, selected_area_end)

integrated_area = np.zeros((PIXEL_COUNT, PIXEL_COUNT))

i = 0
for y in range(PIXEL_COUNT):
    for x in range(PIXEL_COUNT):
        integrated_area[x, y] = (result[i + 1] * selection_mask).sum()
        i += 1

print(integrated_area)

line_number = int(plot_x * PIXEL_COUNT + plot_y)
spectrum_intensity = result[line_number]

# Accumulate the counts in the file name
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

# Rotate integrated_area 90 degrees to the right (#240316)
rotated_area = np.rot90(integrated_area, k=-1)

# Define the extent for the intensity range
extent = [selected_area_begin, selected_area_end, 0, PIXEL_COUNT]

# Plot the rotated image with adjusted intensity range
plt.imshow(rotated_area, interpolation='none', extent=extent, origin='lower')
plt.colorbar(label='Intensity (a.u)')  # Add color bar indicating intensity
plt.xlabel('')  # Label for the x-axis
plt.ylabel('')  # Label for the y-axis
plt.title(f'{selected_area_begin} ~ {selected_area_end} nm')  # Title for the plot

# Plot the rotated image (#240316)
plt.imshow(rotated_area, interpolation='none')
# plt.imshow(integrated_area, interpolation='none')
# plt.plot(spectrum_energy, spectrum_intensity)
plt.show()