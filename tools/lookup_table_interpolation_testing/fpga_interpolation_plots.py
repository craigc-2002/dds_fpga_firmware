import csv
import numpy as np
import matplotlib.pyplot as plt

input_fname = "interpolation_results.csv"

phase_values = []
lookup_table_output_values = []
interpolated_values = []
numerical_values = []
gradient_values = []
interp_values = []

with open(input_fname) as in_file:
    reader = csv.reader(in_file)

    for line in reader:
        phase_values.append(int(line[0]))
        numerical_values.append(float(line[1]))
        interpolated_values.append(int(line[2]))
        lookup_table_output_values.append(int(line[3]))
        gradient_values.append(int(line[4]))
        interp_values.append(int(line[5]))


lookup_table_length = 1024

phase_counter_bit_width = 32-6 # model a 32 bit accumulator with 6 bits truncated (no point running sim for trunacted bits)
lookup_address_bit_width = int(np.log2(lookup_table_length))

lower_addr_bit_width = (phase_counter_bit_width - lookup_address_bit_width)
lower_addr_bit_mask = (2**lower_addr_bit_width) - 1

max_interpolation_bits = 16
lower_addr_truncation = lower_addr_bit_width - max_interpolation_bits if lower_addr_bit_width > max_interpolation_bits else 0


# table_error_values = np.array(lookup_table_output_values) - np.array(numerical_values)
# table_error_values_dB = 20 * np.log10(np.abs(table_error_values)/max(numerical_values))
# table_max_error = max(abs(table_error_values))

# interp_error_values = np.array(interpolated_values) - np.array(numerical_values)
# interp_error_values_dB = 20 * np.log10(np.abs(interp_error_values)/max(numerical_values))
# interp_max_error = max(abs(interp_error_values))

# interp_rms_error = np.sqrt(np.sum(interp_error_values**2)/len(interp_error_values))

interpolated_values_normalised = interpolated_values - np.average(interpolated_values)
output_fft = np.fft.rfft(interpolated_values_normalised, n=len(interpolated_values))
output_fft /= len(interpolated_values)
fft_f = np.fft.rfftfreq(len(interpolated_values), 1/len(interpolated_values))

plt.figure()
plt.plot(fft_f, output_fft)
plt.title("FFT of interpolated output")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (dB)")
plt.show()

# print(f"{lookup_table_length} Table Values")
# print(f"Lookup table address width: {lookup_address_bit_width} bits")
# print(f"Lower phase address width: {lower_addr_bit_width} bits")
# print(f"Lower address truncation: {lower_addr_truncation} bits")
# print(f"Lower phase address width used: {lower_addr_bit_width - lower_addr_truncation} bits")
# print()

# print("Raw Table")
# print(f"Max error: {table_max_error}")
# print(f"= {max(table_error_values_dB)} dBfs")
# print()

# print("Interpolation")
# print(f"Max error: {interp_max_error}")
# print(f"= {max(interp_error_values_dB)} dBfs")
# print(f"RMS error: {interp_rms_error}")
# print(f"= {20 * np.log10(interp_rms_error/max(numerical_values))} dBfs")

# plt.figure()
# plt.title("Lookup Table Values v Real Values")
# plt.plot(phase_values, lookup_table_output_values, label="Lookup Table Values")
# plt.plot(phase_values, interpolated_values, label="Interpolated Values")
# plt.plot(phase_values, numerical_values, label="Sine Values")
# plt.grid(True)
# plt.legend()

# plt.figure()
# plt.title("Error in Interpolated Values")
# plt.plot(phase_values, interp_error_values_dB)
# plt.ylabel("Error from ideal sine wave (dBfs)")
# plt.xlabel("Phase value")
# plt.grid(True)

# plt.figure()
# plt.title("Linear Interpolation Gradient")
# plt.plot(gradient_values)

# plt.figure()
# plt.title("Linear Interpolation Value")
# plt.plot(interp_values)

plt.show()