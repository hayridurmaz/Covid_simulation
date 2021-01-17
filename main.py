import math
import matplotlib.pyplot as plt


def getPeopleRecovered(t, z_list):
    recovered_t_delay = 2
    death_t_delay = 2
    p_recovered = 0.9
    p_death = 0.1
    rt_half = 0

    if t < recovered_t_delay:
        rt_half = p_recovered * 0
    else:
        rt_half = p_recovered * z_list[t - recovered_t_delay]

    if t < death_t_delay:
        rt = p_death * 0 + rt_half
    else:
        rt = p_death * z_list[t - death_t_delay] + rt_half
    print("getPeopleRecovered", math.floor(rt))
    return math.floor(rt)


def getPeopleInQuarantine(t, z_list):
    detected_t_delay = 2
    undetected_t_delay = 2
    p_detected = 0.9
    p_undetected = 0.1
    q_half = 0

    if t < detected_t_delay:
        q_half = p_detected * 0
    else:
        q_half = p_detected * z_list[t - detected_t_delay]

    if t < undetected_t_delay:
        qt = p_undetected * 0 + q_half
    else:
        qt = p_undetected * z_list[t - undetected_t_delay] + q_half
    print("getPeopleInQarantine", math.floor(qt))
    return math.floor(qt)


def infectionRate(t, z_list, total_pop):
    tdelay = 0
    mi = 1.01
    temp = (z_list[t - tdelay] * mi) / (total_pop)
    print("infectionRate", temp)
    return temp


if __name__ == '__main__':
    z = []
    rt_list = []
    qt_list = []

    recovered = []

    z.append(10)

    for i in range(0, len(z)):
        print("i:", i, ", infected people number =", z[i])

    # print("recovered",recoveredPeople(0,z))

    total_pop = 5000

    total_recovered = 0

    for t in range(0, 12):
        #    recovered.append(getPeopleRecovered(t,z))
        #    for i in range(0,len(recovered)):
        #        total_recovered = total_recovered + recovered[i]

        z_next = math.floor(
            (total_pop - getPeopleRecovered(t, z) - getPeopleInQuarantine(t, z)) * infectionRate(t, z, total_pop)) + z[
                     t]
        print("t :", t, " , z_next :", z_next)
        if z_next > total_pop:
            print("simulation is stopped")
            break
        else:
            z.append(z_next)

    plt.plot(z)
    plt.show()

