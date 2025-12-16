# Model info
model_name = "1-2-4-8 dimer-higher order oligomer model with equilibrium constants and assuming kn is the same"
kinetic_constants = ['k1','K1','k_assoc','K24','K48']

def ode_model(t, M, k):
    M1, M2, M4, M8 = M
    k1, K1, k_assoc, K24, K48 = k

    # Define reverse rates with equilibrium constant Kn
    k_1 = k1 / K1
    k_2 = k_assoc / K24
    k_3 = k_assoc / K48
  
    dM1 = -2*k1*M1**2 + 2*k_1*M2
    dM2 = k1*M1**2 - k_1*M2 - 2*k_assoc*M2**2 + 2*k_2*M4
    dM4 = k_assoc*M2**2 - k_2*M4 - 2*k_assoc*M4**2 + 2*k_3*M8
    dM8 = 2*k_assoc*M4**2 - k_3*M8

    return [dM1,dM2,dM4,dM8]
