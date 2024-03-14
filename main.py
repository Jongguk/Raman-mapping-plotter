import sys
import tkinter
import numpy as np
import matplotlib.pyplot as plt

from tkinter import filedialog

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
    print("Selected file is: " + file_name)

    with open(file_path, 'r') as file:
        raw_data = file.read()
    rows = raw_data.strip().split("\n")
    converted_data = [row.strip().split(",") for row in rows]

    return converted_data

result = np.array(import_data())
sliced_result = np.array(result[:,3:-1], dtype = float)
spectrum_energy = sliced_result[0]
spectrum_intensity = sliced_result[1]

plt.plot(spectrum_energy, spectrum_intensity)
plt.show()