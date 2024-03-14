import sys
import tkinter
import math
import numpy as np
import matplotlib.pyplot as plt

from tkinter import filedialog

plot_x = 8 # 스펙트럼 뽑을 x 좌표
plot_y = 9 # 스펙트럼 뽑을 y 좌표
selected_area_begin = 540 # 맵핑할때 사용할 면적 범위 시작 (에너지)
selected_area_end = 560 # 맵핑할때 사용할 면적 범위 끝

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
    seperated_data = [row.strip().split(",") for row in rows]
    PIXEL_COUNT: int = int(math.sqrt(len(rows) - 1))
    sliced_result = np.array(np.array(seperated_data)[:,3:-1], dtype = float)
    
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

# print((result[1:] * selection_mask).sum())
integrated_area = np.zeros((PIXEL_COUNT, PIXEL_COUNT))

i = 0
for y in range(PIXEL_COUNT):
    for x in range(PIXEL_COUNT):
        integrated_area[x, y] = (result[i + 1] * selection_mask).sum()
        i += 1
        # print(integrated_area)

print(integrated_area)

line_number = plot_x * PIXEL_COUNT + plot_y
spectrum_intensity = result[line_number]

output_file_path = "data_plot.txt"
with open(output_file_path, 'w') as file:
    file.write("X\tY\n")
    for x, y in zip(spectrum_energy, spectrum_intensity):
        file.write(f"{x}\t{y}\n")

plt.imshow(integrated_area, interpolation='none')
# plt.plot(spectrum_energy, spectrum_intensity)
plt.show()