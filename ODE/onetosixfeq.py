# Model info
model_name = "1-2-3-4-5-6 linear stepwise with equilibrium constants"
kinetic_constants = ['k1','K1','k2','K2','k3','K3','k4','K4','k5','K5']

def ode_model(t, M, k):
    M1, M2, M3, M4, M5, M6 = M
    k1, K1, k2, K2, k3, K3, k4, K4, k5, K5 = k

    # Define reverse rates using equilibrium constants Kn
    k_1 = k1 / K1
    k_2 = k2 / K2
    k_3 = k3 / K3
    k_4 = k4 / K4
    k_5 = k5 / K5

    dM1 = -2*k1*M1**2 + 2*k_1*M2 - k2*M1*M2 + k_2*M3 - k3*M1*M3 + k_3*M4 - k4*M1*M4 + k_4*M5 - k5*M1*M5 + k_5*M6
    dM2 = k1*M1**2 - k_1*M2 - k2*M1*M2 + k_2*M3
    dM3 = k2*M1*M2 - k_2*M3 - k3*M1*M3 + k_3*M4
    dM4 = k3*M1*M3 - k_3*M4 - k4*M1*M4 + k_4*M5
    dM5 = k4*M1*M4 - k_4*M5 - k5*M1*M5 + k_5*M6
    dM6 = k5*M1*M5 - k_5*M6

    return [dM1,dM2,dM3,dM4,dM5,dM6]
