# -*- coding: utf-8 -*-
import numpy as np
import warnings

def fire(A_w, h_w, A_t, A_f, t_alpha, b, q, gamma_fi_Q):


    # PREMISES
    O = A_w * h_w ** 0.5 / A_t
    Q_d = q * A_f

    # AA.1
    Q_max_v_k = 1.21 * A_w * np.sqrt(h_w)  # [MW] AA.1

    # AA.2
    Q_max_f_k = 0.25 * A_f  # [MW] AA.2

    Q_max_k = min(Q_max_f_k, Q_max_v_k)  # [MW]

    # AA.5
    Q_max_v_d = gamma_fi_Q * Q_max_v_k  # [MW] AA.5
    Q_max_f_d = gamma_fi_Q * Q_max_f_k  # [MW]AA.6, gamma_fi_Q see BB.5.3

    # AA.7
    t_1 = t_alpha * np.sqrt(Q_max_v_d)  # [s] AA.7
    T_1_v = - 8.75 / O - 0.1 * b + 1175  # [deg.C] AA.8, b is heat storage capacity

    # AA.9
    Q_2 = 0.7 * Q_d - t_1 ** 3 / (3 * t_alpha ** 2)  # AA.9(a)
    t_2 = t_1 + Q_2 / Q_max_v_d  # [s] AA.9(b)

    # AA.10
    T_2_v = (0.004 * b -17) / O - 0.4 * b + 2175  # [deg.C] AA.10
    if T_2_v >= 1134:
        warnings.warn("Theta_2_v = {}, is greater than maximum allowed 1134 and is forced to 1134.")
        T_2_v = 1134

    # AA.11
    Q_d = q * A_f  # [MJ], total fire load in the compartment
    Q_3 = 0.3 * Q_d
    t_3 = t_2 + (2 * Q_3)

    # AA.12
    Q_3_v = -5. / O - 0.16 * b + 1060  # [deg.C]

    # AA.13
    t_1 = t_alpha




    pass

if __name__ == '__main__':
    pass
