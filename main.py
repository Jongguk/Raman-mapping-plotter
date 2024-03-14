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
        filetypes = [("csv file", "*.csv"), ("All files", "*.*")]
    )
    if not file_path:
        sys.exit("Error: No file selected.")
    file_name = file_path.split("/")[-1]
    file_directory = "/".join(file_path.split("/")[:-1])
    print("Selected file is: " + file_name)

    with open(file_path, 'r') as file:
        raw_data = file.readlines()

    csv_data = [line.strip().split(",") for line in raw_data]
    return csv_data
# Initialize CONSTANTS
# X_PIXEL_COUNT =
# Y_PIXEL_COUNT =
# CCD_COUNT = 

result = import_data()
print(result[0])
spectrum_energy = result[0][3:-1]
test_spectrum_intensity = result[1][3:-1]

