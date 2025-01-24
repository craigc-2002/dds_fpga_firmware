# program to generate VHD files for the lookup tables required for the DDS
# Will create lookup tables for sine and the gradient (with a scale factor)

import numpy as np
from vhdl_lookup_table_generator import VHDLLookupGenerator

lookup_table_length = 1024

phase_counter_bit_width = 32
lookup_address_bit_width = int(np.log2(lookup_table_length))

lower_addr_bit_width = (phase_counter_bit_width - lookup_address_bit_width)
lower_addr_bit_mask = (2**lower_addr_bit_width) - 1

max_interpolation_bits = 16
lower_addr_truncation = lower_addr_bit_width - max_interpolation_bits if lower_addr_bit_width > max_interpolation_bits else 0

# calculate the values for the sine lookup table
dac_bits = 16
sine_lookup_table = [int(((2**(dac_bits-1))-1) * (1 + np.sin(np.pi*2 * i /(2**lookup_address_bit_width)))) for i in range(2**lookup_address_bit_width)]

# calculate the values for the gradient lookup table
gradient_table = []
gradient_bit_shift = 29 # value gradient is shifted by to store 16 bits

for i in range(len(sine_lookup_table)):
    current_value = sine_lookup_table[i]
    next_value = sine_lookup_table[i + 1] if i < (len(sine_lookup_table) - 1) else sine_lookup_table[0] # handle the special case of when the lookup table address wraps around
    gradient = int(((next_value - current_value) / 2**(lower_addr_bit_width)) * 2**gradient_bit_shift) # 16 bit signed fixed point representation
    gradient_table.append(gradient)

# place the lookup tables into VHDL files
# VHDLLookupGenerator(sine_lookup_table, "SINE_ROM", "sine_rom.vhd").generate_table()
VHDLLookupGenerator(gradient_table, "GRADIENT_ROM", "gradient_rom.vhd", data_type="signed").generate_table()

print(sine_lookup_table)
print(max(sine_lookup_table))
print(min(sine_lookup_table))

# print(gradient_table)
print(max(gradient_table))
print(min(gradient_table))