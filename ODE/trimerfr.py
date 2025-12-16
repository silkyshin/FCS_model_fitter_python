# Model info
model_name = "1-3-6 trimer based nucleation model"
kinetic_constants = ['k1','k_1','k2','k_2']

def ode_model(t, M, k):
    M1, M3, M6 = M
    k1, k_1, k2, k_2 = k

    dM1 = -3*k1*M1**3 + 3*k_1*M3
    dM3 = k1*M1**3 - k_1*M3 - 2*k2*M3**2 + 2*k_2*M6
    dM6 = 2*k3*M3**2 - k_3*M6

    return [dM1,dM3,dM6]
