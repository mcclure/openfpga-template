#-------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE
# SPDX-FileCopyrightText: (c) 2023, OpenGateware authors and contributors
#-------------------------------------------------------------------------------
#
# Infinite Impulse Response (IIR) Low-Pass Filter Generator
#
# Copyright (c) 2023, Marcus Andrade <marcus@opengateware.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#-------------------------------------------------------------------------------

import numpy as np
from scipy.signal import butter
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

COEFF_WIDTH = 18


def print_verilog_1st(A2, B1, B2):
    # Set Verilog Output
    A2_verilog = f"-{COEFF_WIDTH}'d{-A2}" if A2 < 0 else f"{COEFF_WIDTH}'d{A2}"
    B1_verilog = f"-{COEFF_WIDTH}'d{-B1}" if B1 < 0 else f"{COEFF_WIDTH}'d{B1}"
    B2_verilog = f"-{COEFF_WIDTH}'d{-B2}" if B2 < 0 else f"{COEFF_WIDTH}'d{B2}"
    # Print the Verilog output
    result_text_box.insert(tk.END, f"\nVerilog Ouput:\n")
    result_text_box.insert(tk.END, f"localparam signed [{COEFF_WIDTH - 1}:0] A2 = {A2_verilog};\n")
    result_text_box.insert(tk.END, f"localparam signed [{COEFF_WIDTH - 1}:0] B1 = {B1_verilog};\n")
    result_text_box.insert(tk.END, f"localparam signed [{COEFF_WIDTH - 1}:0] B2 = {B2_verilog};\n")


def print_verilog_2nd(B1, B2, B3, A2, A3):
    # Set Verilog Output
    A2_verilog = f"-{COEFF_WIDTH}'d{-A2}" if A2 < 0 else f"{COEFF_WIDTH}'d{A2}"
    A3_verilog = f"-{COEFF_WIDTH}'d{-A3}" if A3 < 0 else f"{COEFF_WIDTH}'d{A3}"
    B1_verilog = f"-{COEFF_WIDTH}'d{-B1}" if B1 < 0 else f"{COEFF_WIDTH}'d{B1}"
    B2_verilog = f"-{COEFF_WIDTH}'d{-B2}" if B2 < 0 else f"{COEFF_WIDTH}'d{B2}"
    B3_verilog = f"-{COEFF_WIDTH}'d{-B3}" if B3 < 0 else f"{COEFF_WIDTH}'d{B3}"
    # Print the Verilog output
    result_text_box.insert(tk.END, f"\nVerilog Ouput:\n")
    result_text_box.insert(tk.END, f"localparam signed [{COEFF_WIDTH - 1}:0] A2 = {A2_verilog};\n")
    result_text_box.insert(tk.END, f"localparam signed [{COEFF_WIDTH - 1}:0] A3 = {A3_verilog};\n")
    result_text_box.insert(tk.END, f"localparam signed [{COEFF_WIDTH - 1}:0] B1 = {B1_verilog};\n")
    result_text_box.insert(tk.END, f"localparam signed [{COEFF_WIDTH - 1}:0] B2 = {B2_verilog};\n")
    result_text_box.insert(tk.END, f"localparam signed [{COEFF_WIDTH - 1}:0] B3 = {B3_verilog};\n")


def quit_application():
    root.destroy()


def calculate():
    try:
        CUTOFF_FREQUENCY = float(input_freq_entry.get())
        SAMPLE_RATE = float(target_freq_entry.get())
        COEFF_SCALE = int(target_width_entry.get())
        BTYPE = filter_type.get()
        NYQUIST = SAMPLE_RATE / 2
        FILTER_ORDER = 1

        result_text_box.config(state=tk.NORMAL)  # Enable text box to modify text
        result_text_box.delete("1.0", tk.END)  # Clear existing text

        result_text_box.insert(tk.END, f"{BTYPE} Low-Pass Filter\n\n")
        result_text_box.insert(tk.END, f"Sample Rate: {SAMPLE_RATE}\n")
        result_text_box.insert(tk.END, f"Nyquist: {NYQUIST}\n\n")

        if BTYPE == "2nd Order":
            print("2nd Order Filter")
            B, A = butter(N=2, Wn=CUTOFF_FREQUENCY / NYQUIST, btype='low')
            # Scale the coefficients
            A_scaled = np.ceil(A * (2 ** COEFF_SCALE)).astype(int)
            B_scaled = np.ceil(B * (2 ** COEFF_SCALE)).astype(int)
            # Extracting the required coefficients
            A1 = A_scaled[0]
            A2 = A_scaled[1]
            A3 = A_scaled[2]
            B1 = B_scaled[0]
            B2 = B_scaled[1]
            B3 = B_scaled[2]
            # Verification: B1 + B2 + B3 - A2 - A3 should sum to 2^COEFF_SCALE
            sum_verification = B1 + B2 + B3 - A2 - A3
            expected_sum = 2 ** COEFF_SCALE
        else:
            print("1st Order Filter")
            # Design the filter (1st order Butterworth low-pass)
            B, A = butter(N=1, Wn=CUTOFF_FREQUENCY / NYQUIST, btype='low')
            # Scale the coefficients
            A_scaled = np.ceil(A * (2 ** COEFF_SCALE)).astype(int)
            B_scaled = np.ceil(B * (2 ** COEFF_SCALE)).astype(int)
            # Extracting the required coefficients
            A1 = A_scaled[0]
            A2 = A_scaled[1]
            B1 = B_scaled[0]
            B2 = B_scaled[1]
            # Verification: B1 + B2 - A2 should sum to 2^COEFF_SCALE
            sum_verification = B1 + B2 - A2
            expected_sum = 2 ** COEFF_SCALE

        result_text_box.insert(tk.END, f"Coefficients:\n")
        result_text_box.insert(tk.END, f"B = {B}\n")
        result_text_box.insert(tk.END, f"A = {A}\n\n")
        if BTYPE == "2nd Order":
            # Print the scaled coefficients
            result_text_box.insert(tk.END, f"Scaled Coefficients:\n")
            result_text_box.insert(tk.END, f"B = [{B1}   {B2}   {B3}]\n")
            result_text_box.insert(tk.END, f"A = [{A1}   {A2}   {A3}]\n")
        else:
            result_text_box.insert(tk.END, f"Scaled Coefficients:\n")
            result_text_box.insert(tk.END, f"B = [{B1}   {B2}]\n")
            result_text_box.insert(tk.END, f"A = [{A1}   {A2}]\n")

        # Print the verification result
        if sum_verification == expected_sum:
            result_text_box.insert(tk.END, f"\nVerification: Passed\n")
        else:
            result_text_box.insert(tk.END, f"\nVerification: Failed\n")
            result_text_box.insert(tk.END, f"Sum = {sum_verification} | Expected Sum = {expected_sum}")

        if sum_verification == expected_sum:
            if BTYPE == "2nd Order":
                print_verilog_2nd(B1, B2, B3, A2, A3)
            else:
                print_verilog_1st(A2, B1, B2)

        result_text_box.config(state=tk.DISABLED)  # Disable text box to make it read-only
    except ValueError:
        result_text_box.config(state=tk.NORMAL)
        result_text_box.delete("1.0", tk.END)
        result_text_box.insert(tk.END, "Please enter valid numbers.")
        result_text_box.config(state=tk.DISABLED)


# Create the main window
root = tk.Tk()
root.title("IIR Low-Pass Filter")

# Create a Checkbutton that toggles the value
value_label = tk.Label(root, text="Order").grid(row=0, column=0, sticky='w', padx=10, pady=5)
filter_type = tk.StringVar()
dropdown = ttk.Combobox(root, textvariable=filter_type, state="readonly")
dropdown['values'] = ("1st Order", "2nd Order")
dropdown.set("1st Order")

# Input fields and labels
tk.Label(root, text="Cutoff Frequency (Hz):").grid(row=1, column=0, sticky='w', padx=10, pady=5)
default_freq = tk.StringVar(value="3500")
input_freq_entry = tk.Entry(root, textvariable=default_freq)

tk.Label(root, text="Sample Rate (Hz):").grid(row=2, column=0, sticky='w', padx=10, pady=5)
default_target = tk.StringVar(value="96000")
target_freq_entry = tk.Entry(root, textvariable=default_target)

tk.Label(root, text="Coefficient scaling factor:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
default_width = tk.StringVar(value="15")
target_width_entry = tk.Entry(root, textvariable=default_width)

# Result display area
result_text_box = tk.Text(root, height=22, width=44)
result_text_box.config(state=tk.DISABLED)

# Buttons
calculate_button = tk.Button(root, text="Calculate", command=calculate)
quit_button = tk.Button(root, text="Quit", command=quit_application)

# Set the column configuration
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)

# Add padding around the widgets for better spacing
dropdown.grid(row=0, column=1, padx=10, pady=0)
input_freq_entry.grid(row=1, column=1, padx=10, pady=5)
target_freq_entry.grid(row=2, column=1, padx=10, pady=5)
target_width_entry.grid(row=3, column=1, padx=10, pady=5)
result_text_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
calculate_button.grid(row=5, column=0, padx=10, pady=5)
quit_button.grid(row=5, column=1, padx=10, pady=5)

# Run the application
root.mainloop()
