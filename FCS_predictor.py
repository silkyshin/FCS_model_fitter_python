import numpy as np
import matplotlib.pyplot as plt
import argparse

# --- 1. Parse command-line arguments ---
parser = argparse.ArgumentParser(description="Predict FCS G0 and diffusion time from ODE solution")
parser.add_argument('--csv', type=str, required=True, help="Path to ODE solution CSV")
parser.add_argument('--sfactor', type=float, default=1.0, help="Scaling exponent v for tau_n = n^v (default 1.0)")
args = parser.parse_args()

csv_file = args.csv
v = args.sfactor

# --- 2. Load ODE solution CSV ---
data = np.loadtxt(csv_file, delimiter=',', skiprows=1)  # skip header
t = data[:,0]
M_t = data[:,1:]  # concentrations of oligomers

# --- 3. Number of monomers per species ---
n = np.arange(1, M_t.shape[1]+1)

# --- 4. Normalize M_t to total monomer equivalents ---
total_monomers = np.sum(M_t * n, axis=1, keepdims=True)
M_norm = (M_t * n) / total_monomers

# --- 5. Predicted G0(t) ---
G0_pred = np.sum(M_norm**2, axis=1)

# --- 6. Predicted diffusion time ---
tau_n = n**v
tauD_pred = np.sum(M_norm * tau_n, axis=1)

# --- 7. Plot ---
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

# --- 8. Save predictions ---
save_file = csv_file.replace(".csv", "_FCS_pred.csv")
header = "t,G0,tauD"
np.savetxt(save_file, np.column_stack([t, G0_pred, tauD_pred]), delimiter=',', header=header, comments='', fmt='%.4g')
print(f"Predictions saved to {save_file}")
