

def calc_gsop(t_v, t_ot, z_ot):
    return (t_v - t_ot) * z_ot


def calc_r_s(a, b, d_d):
    return a * d_d + b


def calc_f(a_fas, a_ok):
    return a_ok / (a_fas + a_ok)


def calc_comp(a_n_sum, v_ot):
    return a_n_sum / v_ot


def calc_k_obsh(a_n_sum, a_fas, r_pr_st, a_ok, r_pr_ok, a_pokr, r_pr_per, a_cherd, r_pr_cherd):
    return 1 / a_n_sum * (a_fas / r_pr_st + a_ok / r_pr_ok + a_pokr / r_pr_per + a_cherd / r_pr_cherd)


def calc_n_v(a_sh, cnt_floors, t_ot, n_vent=168, b_v=0.85, n_inf=168, v_ot=53748.20):
    l_vent = 3 * a_sh
    g_inf = 0.3 * b_v * 1268.5 if cnt_floors <= 3 else \
            0.45 * b_v * 1268.5 if 4 <= cnt_floors <= 9 else \
            0.6 * b_v * 1268.5

    p_vent = 353/(273 + t_ot)

    return ((l_vent * n_vent) / 168 + (g_inf * n_inf) / (168 * p_vent)) / (b_v * v_ot)


def calc_k_ob(k_obsh, k_komp):
    return k_obsh * k_komp


def calc_k_vent(n_vent=1.3, b_v=0.85, k_ef=0.4):
    c = 1
    return 0.28 * c * n_vent * b_v * (1 - k_ef)


def calc_k_bit(a_sh, v_ot, t_v, t_ot):
    q_bit = 17

    return (q_bit * a_sh) / (v_ot * (t_v - t_ot))


def calc_k_rad(v_ot, gsop):
    q_god_rad = 1241327.5
    return (1.16 * q_god_rad) / (v_ot * gsop)


def calc_u(gsop):
    return 0.7 + 0.000025 * (gsop - 1000)


def calc_q_ot_p(k_ob, k_vent, k_bit, k_rad, u, bh=1.05, z=0.95, e=0.1):
    return (k_ob + k_vent - (k_bit + k_rad) * u * z) * (1 - e) * bh


def calc_q(gsop, q_ot_p):
    return 0.024 * gsop * q_ot_p


def calc_q_god_ot(gsop, v_ot, q_ot_p):
    return 0.24 * gsop * v_ot * q_ot_p


def calc_energo_effencity(q_p_ot, q_tr_ot):
    print(q_p_ot, q_tr_ot)
    return (q_p_ot - q_tr_ot) / q_p_ot * 100


def calc_q_tr_ot(cnt_floors):
    if cnt_floors == 1:
        return 0.455
    elif cnt_floors == 2:
        return 0.414
    elif cnt_floors == 3:
        return 0.372
    elif cnt_floors in [4, 5]:
        return 0.359
    elif cnt_floors in [6, 7]:
        return 0.336
    elif cnt_floors in [8, 9]:
        return 0.319
    elif cnt_floors in [10, 11]:
        return 0.301
    else:
        return 0.290


def get_result(energo_effencity):
    print(energo_effencity)
    if energo_effencity <= -60:
        return 'A++', 'Класс очень высокий', 'Экономически стимулированный'
    elif -60 < energo_effencity <= -50:
        return 'A++', 'Класс очень высокий', 'Экономически стимулированный'
    elif -50 < energo_effencity <= -40:
        return 'A', 'Класс очень высокий', 'Экономически стимулированный'
    elif -40 < energo_effencity <= -30:
        return 'B+', 'Высокий', 'Экономически стимулированный'
    elif -30 < energo_effencity <= -15:
        return 'B', 'Высокий', 'Экономически стимулированный'
    elif -5 < energo_effencity <= -15:
        return 'C+', 'Нормальный', 'Мероприятия не разрабатываются'
    elif -5 < energo_effencity <= 5:
        return 'C', 'Нормальный', 'Мероприятия не разрабатываются'
    elif 5 < energo_effencity <= 15:
        return 'C-', 'Нормальный', 'Мероприятия не разрабатываются'
    elif 15 < energo_effencity <= 50:
        return 'D', 'Пониженный', 'Реконструкция при соответствующем экономическом обосновании'
    else:
        return 'E', 'Низкий', 'Реконструкция при соответствующем экономическом обосновании, или снос'
