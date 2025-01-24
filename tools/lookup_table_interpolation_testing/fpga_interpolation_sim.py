# calculate values for a lookup table of n values from the sine function
# plot the lookup table values versus the exact value of the function
# plot the lookup table values with a simple linear interpolation and the error compared to the numerical sine function
# This implemnentation uses fixed point integer representation with 16-bit precision to give as close as possible to a bit-accurate simulation of the calculation in the FPGA
# THIS IS THE MOST ACCURATE ONE!!

import numpy as np
import matplotlib.pyplot as plt

output_fname = "interpolation_results.csv"

lookup_table_length = 1024

phase_counter_bit_width = 32-6 # model a 32 bit accumulator with 6 bits truncated (no point running sim for trunacted bits)
lookup_address_bit_width = int(np.log2(lookup_table_length))

lower_addr_bit_width = (phase_counter_bit_width - lookup_address_bit_width)
lower_addr_bit_mask = (2**lower_addr_bit_width) - 1

max_interpolation_bits = 16
lower_addr_truncation = lower_addr_bit_width - max_interpolation_bits if lower_addr_bit_width > max_interpolation_bits else 0

# calculate the values for the sine lookup table
dac_bits = 16
lookup_table = [int(((2**(dac_bits-1))-1) * (1 + np.sin(np.pi*2 * i /(2**lookup_address_bit_width)))) for i in range(2**lookup_address_bit_width)]

# gradient lookup table
gradient_table = []
gradient_bit_shift = 29 # value gradient is shifted by to store 16 bits SIGNED integer
for i in range(len(lookup_table)):
    current_value = lookup_table[i]
    next_value = lookup_table[i + 1] if i < (len(lookup_table) - 1) else lookup_table[0] # handle the special case of when the lookup table address wraps around
    gradient = int(((next_value - current_value) / 2**(lower_addr_bit_width)) * 2**gradient_bit_shift) # 16 bit signed fixed point representation
    gradient_table.append(gradient)

# iterate over all values for input phase and calculate the sine value using both the raw lookup table, and with first order interpolation
# also calculate the numerical value at that point to allow the errors to be calculated
phase_values = []
lookup_table_output_values = []
interpolated_values = []
numerical_values = []
gradient_values = []
interp_values = []

for i in range(2**phase_counter_bit_width):
    phase_values.append(i)
    numerical_values.append(((2**(dac_bits-1))-1) * (1 + np.sin(np.pi*2 * i /(2**phase_counter_bit_width))))

    table_address = int(i >> lower_addr_bit_width)
    lower_phase_address = int(i & lower_addr_bit_mask)

    current_value = lookup_table[table_address]
    lookup_table_output_values.append(current_value)

    # perform linear interpolation between current point and next based on lower phase address
    # gradient is stored in a seperate lookup table with a bit shift to give a full 16 bits of precision
    gradient = gradient_table[table_address]
    truncated_lower_phase_address = int(lower_phase_address / (2**lower_addr_truncation)) # truncate lower phase address to 16 bits. Will lead to loss of precision with 4 bits completely truncated but will make calculation easier
    interp = int(truncated_lower_phase_address * gradient * (2**lower_addr_truncation) / (2**gradient_bit_shift)) # bit shifts to account for the fact that the gradient values are shifted and there are 6 bits truncated

    interpolated_value = current_value + interp

    gradient_values.append(gradient)
    interp_values.append(interp)
    interpolated_values.append(interpolated_value)

with open(output_fname, "+w") as f:
    for i in range(len(interpolated_values)):
        print(f"{phase_values[i]}, {numerical_values[i]}, {interpolated_values[i]}, {lookup_table_output_values[i]}, {gradient_values[i]}, {interp_values[i]}", file=f)
