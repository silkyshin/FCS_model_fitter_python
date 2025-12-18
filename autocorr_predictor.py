import numpy as np
import matplotlib.pyplot as plt
import argparse

# parse command line arguments
parser = argparse.ArgumentParser(description="Predict FCS curves from ODE solution")
parser.add_argument('--csv', type=str, required=True, help="Path to ODE solution CSV")
parser.add_argument('--sfactor', type=float, default=0.5, help="Scaling exponent v for tau_n = n^v")
parser.add_argument('--tripletF', type=float, default=0.2, help="Triplet fraction F")
parser.add_argument('--tripletTau', type=float, default=0.015, help="Triplet lifetime tau_m (s)")
parser.add_argument('--baseline', type=float, default=1.0, help="Baseline C")
parser.add_argument('--lagMin', type=float, default=0.001, help="Min lag time (s)")
parser.add_argument('--lagMax', type=float, default=1000, help="Max lag time (s)")
parser.add_argument('--numLag', type=int, default=200, help="Number of lag times")
parser.add_argument('--saveTimepoints', type=str, default=None,
                    help="Comma-separated list of ODE timepoints to save curves (default: last timepoint only)")
args = parser.parse_args()

# might implement lag time detection script given experiment

# load ODE solution
data = np.loadtxt(args.csv, delimiter=',', skiprows=1)
t = data[:, 0]
M_t = data[:, 1:]  # species concentrations

# monomer per species
n = np.arange(1, M_t.shape[1] + 1)

# normalize monomer equivalents
total_monomers = np.sum(M_t * n, axis=1, keepdims=True)
M_norm = (M_t * n) / total_monomers

# diffusion times of oligomers
tau_n = n**args.sfactor

# lag times
tau_corr = np.logspace(np.log10(args.lagMin), np.log10(args.lagMax), args.numLag)

# triplet state correction
F = args.tripletF
tau_m = args.tripletTau
C = args.baseline

# determine what timepoints to save
if args.saveTimepoints:
    timepoints = [float(tp) for tp in args.saveTimepoints.split(',')]
else:
    timepoints = [t[-1]]  # default: last timepoint

# find closest indices in t
time_indices = [np.argmin(np.abs(t - tp)) for tp in timepoints]

# compute fcs curves
G_curves = {}
for idx in time_indices:
    G_tau = np.zeros_like(tau_corr)
    for j, dtau in enumerate(tau_corr):
        # weighted sum over species
        G_diff = np.sum(M_norm[idx]**2 / (1 + dtau / tau_n))
        G_tau[j] = G_diff * (1 - F + F * np.exp(-dtau / tau_m)) + C
    G_curves[t[idx]] = G_tau

# plot
plt.figure(figsize=(8,5))
for tp, G_tau in G_curves.items():
    plt.semilogx(tau_corr, G_tau, label=f"t = {tp:.2g} s")
plt.xlabel("Lag time τ (s)")
plt.ylabel("G(τ)")
plt.title("Predicted FCS curves")
plt.legend()
plt.tight_layout()
plt.show()

# save
for tp, G_tau in G_curves.items():
    save_file = args.csv.replace(".csv", f"_FCS_pred_{int(tp)}s.csv")
    header = "tau," + ",".join([f"G(t={tp:.2g})"])
    np.savetxt(save_file, np.column_stack([tau_corr, G_tau]), delimiter=',', header=header, comments='', fmt='%.6g')
    print(f"Saved predicted FCS curve at t={tp:.2g}s to {save_file}")
