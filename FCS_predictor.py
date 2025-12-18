import numpy as np
import matplotlib.pyplot as plt
import argparse

# parse command line args
parser = argparse.ArgumentParser(description="Predict FCS G0 and diffusion time from ODE solution")
parser.add_argument('--csv', type=str, required=True, help="Path to ODE solution CSV")
parser.add_argument('--sfactor', type=float, default=0.5, help="Scaling exponent v for tau_n = n^v (default 0.5)")
args = parser.parse_args()

csv_file = args.csv
v = args.sfactor

# load ODE solutions - could try to make it more flexible
data = np.loadtxt(csv_file, delimiter=',', skiprows=1)  # skip header
t = data[:,0]
M_t = data[:,1:]  # concentrations of oligomers

# monomer per oligomer size
n = np.arange(1, M_t.shape[1]+1)

# M_t normalization
total_monomers = np.sum(M_t * n, axis=1, keepdims=True)
M_norm = (M_t * n) / total_monomers

# G0(t) prediction
G0_pred = np.sum(M_norm**2, axis=1)

# tau prediction
tau_n = n**v
tauD_pred = np.sum(M_norm * tau_n, axis=1)

# plot - maybe do parse to change styles for ease of use?
plt.figure(figsize=(8,6))
plt.subplot(2,1,1)
plt.plot(t, G0_pred, '-', label='Predicted G0')
plt.xlabel("Time (s)")
plt.ylabel("G0")
plt.legend()

plt.subplot(2,1,2)
plt.plot(t, tauD_pred, '-', label='Predicted tauD')
plt.xlabel("Time (s)")
plt.ylabel("τD (s)")
plt.legend()
plt.tight_layout()
plt.show()

# save
save_file = csv_file.replace(".csv", "_FCS_pred.csv")
header = "t,G0,tauD"
np.savetxt(save_file, np.column_stack([t, G0_pred, tauD_pred]), delimiter=',', header=header, comments='', fmt='%.4g')
print(f"Predictions saved to {save_file}")
