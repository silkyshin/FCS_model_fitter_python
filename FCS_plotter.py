import numpy as np
import matplotlib.pyplot as plt
import argparse

# 1. Parse command line arguments
parser = argparse.ArgumentParser(description="Plot FCS timecourse data from CSV")
parser.add_argument('--csv', type=str, required=True,
                    help='Path to FCS data CSV (columns: time,G0,tau)')
args = parser.parse_args()
csv_file = args.csv

# 2. Load CSV
data = np.genfromtxt(csv_file, delimiter=',', names=True)

time = data['time']
G0   = data['G0']
tau  = data['tau']

# 3. Plot
plt.figure(figsize=(8,6))

plt.subplot(2,1,1)
plt.plot(time, G0, 'o-', color='blue')
plt.xlabel('Time (s)')
plt.ylabel('G0')
plt.title('FCS Amplitude G0 vs Time')
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(time, tau, 'o-', color='red')
plt.xlabel('Time (s)')
plt.ylabel('Diffusion time (s)')
plt.title('FCS Diffusion Time vs Time')
plt.grid(True)

plt.tight_layout()
plt.show()
