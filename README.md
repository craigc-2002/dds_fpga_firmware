# DDS FPGA Firmware

FPGA firmware for Direct Digital Synthesis MEng final year project. 
The firmware is written in VHDL and will be synthesised for a Lattice iCE40HX8K on the Alchitry Cu development board.
The DDS interfaces with a DAC and analogue signal chain on a custom PCB.

Project aim is to design and build a DDS with very low phase modulation spurs in the output spectrum.

## Architecture
The DDS consists of a phase accumulator, phase to amplitude conversion and an interface to the DAC.
The phase accumulator is 32 bits wide and adds the phase increment on each clock cycle.
The phase to amplitude conversion is performed using a sine amplitude lookup table, with a gradient lookup table to allow for interpolation between points of the sine ROM.
This eliminates phase truncation from the output.
