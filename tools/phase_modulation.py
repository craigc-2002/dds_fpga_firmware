# Model a DDS with a truncated phase accumulator by phase modulating a sine wave with a phase error signal
# The phase error signal is a sawtooth wave with an amplitude determined by number of truncated bits and frequency determined by truncated bits of frequency tuning word
# Plot the FFT of the sine wave and compare to that of the phase error signal
# The sinusoidal signal is also amplitude modulated with the signal to allow the spectrum of the narrowband PM to be compared

import numpy as np
from matplotlib import pyplot as plt
from scipy import signal

accumulator = 0
accumulator_bits = 32
lookup_table_bits = 10 # 10-bit sine lookup address
truncated_bits = accumulator_bits - lookup_table_bits

f_clk = 100e6

# bits to the right of _ are truncated
phase_increment = 0b0000001011_0000000000000000101001 # provides spurs at 1 kHz
phase_increment = 46137385

f_out = phase_increment * f_clk / (2**accumulator_bits)
truncated_phase_increment = phase_increment % (2**truncated_bits)

error_period = (2**truncated_bits) / truncated_phase_increment # period of phase error in number of samples for the continuous time waveform
error_frequency = f_clk / error_period # frequency of phase error waveform

# number of samples before sampled output waveform repeats
numeric_period = int((2**accumulator_bits) / np.gcd(phase_increment, 2**accumulator_bits))

# number of samples to run simulation for (50000 sine waves)
sine_period = int(f_clk / f_out) # number of ref clock cycles per output sine wave
sim_duration = sine_period * 50000

def phase_error(t):
    return (2**(truncated_bits-1)) * (1 + signal.sawtooth(2 * np.pi * error_frequency * t))

time_values = np.linspace(0, (sim_duration / f_clk), sim_duration)

acc_values = []
for i in range(sim_duration):
    acc_values.append(accumulator)
    accumulator += phase_increment
    accumulator %= 2**accumulator_bits

acc_values = np.array(acc_values)

error_values = phase_error(time_values)
sine_values = (2**(accumulator_bits-1)) * (1 + np.sin(2 * np.pi * f_out * time_values))

# amplitude modulate the ideal output with the phase error output
amplitude_modulated_sine_values = (2**(accumulator_bits-1)) * (1 + np.sin((2 * np.pi * f_out * time_values))) * (phase_error(time_values) / 2**accumulator_bits)

# phase modulated sine wave with the phase error output
phase_modulated_sine_values = (2**(accumulator_bits-1)) * (1 + np.sin((2 * np.pi * f_out * time_values) + (phase_error(time_values) / 2**truncated_bits)))

normalised_error = error_values - np.average(error_values) # normalise by subtracting the average to remove the 0Hz peak
fft_error = abs(np.fft.fft(normalised_error))
fft_sampled_error_scaled = ((fft_error)/(2**truncated_bits * len(error_values)))

fft_am_output = abs(np.fft.fft(amplitude_modulated_sine_values))

phase_modulated_sine_values_normalised = phase_modulated_sine_values - np.average(phase_modulated_sine_values)
fft_pm_output = abs(np.fft.rfft(phase_modulated_sine_values_normalised))
fft_pm_output_scaled = (2 * (fft_pm_output)/len(phase_modulated_sine_values))
fft_pm_output_scaled = (fft_pm_output_scaled / np.max(fft_pm_output_scaled))

print(f"Phase increment word: {phase_increment} - {phase_increment:b}")
print(f"Output frequency: {(f_out/1e6):.4f} MHz")
print(f"Truncated phase increment: {truncated_phase_increment} -   {truncated_phase_increment:b}")
print(f"Error frequency: {(error_frequency/1e6):.5f} MHz")

plt.figure()
plt.title("Phase Error Sequence")
plt.plot(time_values, error_values)

plt.figure()
plt.title("Ideal DDS Output")
plt.plot(time_values[:sine_period * 5], sine_values[:sine_period * 5], label="Ideal") # show the first 5 sine wave cycles
plt.plot(time_values[:sine_period * 5], phase_modulated_sine_values[:sine_period * 5], label="PM") # show the first 5 sine wave cycles
plt.legend()

plt.figure()
plt.title("Amplitude Modulated DDS Output")
plt.plot(time_values[:sine_period * 5], amplitude_modulated_sine_values[:sine_period * 5]) # show the first 5 sine wave cycles

plt.figure()
plt.title("Phase Modulated DDS Output")
plt.plot(time_values[:sine_period * 5], phase_modulated_sine_values[:sine_period * 5]) # show the first 5 sine wave cycles

plt.figure()
plt.title("FFT of phase error sequence")
plt.plot(np.fft.fftfreq(len(error_values), (1/f_clk)), fft_sampled_error_scaled)

plt.figure()
plt.title("FFT of AM DDS output")
plt.plot(np.fft.fftfreq(len(amplitude_modulated_sine_values), (1/f_clk)), fft_am_output)

ax = plt.figure()
plt.title("FFT of Phase Modulated DDS output")
plt.plot(np.fft.rfftfreq(len(phase_modulated_sine_values_normalised), (1/f_clk)), fft_pm_output_scaled)
plt.xlabel("Frequency (Hz)")

plt.show()