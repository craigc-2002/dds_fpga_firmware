# plot for final report illustrating the truncation of the phase accumulator

import matplotlib.pyplot as plt

truncated_bits = 22
accumulator_bits = truncated_bits + 2

accumulator = 0

acc_vals = []
trunc_vals = []

for i in range(2**accumulator_bits):
    acc_vals.append(accumulator)
    trunc_vals.append(accumulator % (2**truncated_bits))
    accumulator += 1

plt.figure()
plt.plot(acc_vals, label="Phase accumulator value")
plt.plot(trunc_vals, label="Phase error")
plt.xlabel("Phase accumulator value")
plt.title("Phase accumulator truncation")
plt.legend()
plt.show()
