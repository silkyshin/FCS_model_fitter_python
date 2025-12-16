# Model info
model_name = "1-2-4-6 even order oligomerization model with equilibrium constants and assume kn is the same"
kinetic_constants = ['k1','K1','k_assoc','K24','K46']

def ode_model(t, M, k):
    M1, M2, M4, M6 = M
    k1, K1, k_assoc, K24, K46 = k

    # Define reverse rates from equilibrium constants Kn
    k_1 = k1 / K1
    k_2 = k_assoc / K24
    k_3 = k_assoc / K46
  
    dM1 = -2*k1*M1**2 + 2*k_1*M2
    dM2 = k1*M1**2 - k_1*M2 - 2*k_assoc*M2**2 + 2*k_2*M4 - k_assoc*M2*M4 + k_3*M6
    dM4 = k_assoc*M2**2 - k_2*M4 - k_assoc*M4*M2 + k_3*M6
    dM6 = k_assoc*M2*M4 - k_3*M6

    return [dM1,dM2,dM4,dM6]
