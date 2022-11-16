import random

WIND = [[0.2, 0.73, 0.07], [0.11, 0.74, 0.15], [0.04, 0.61, 0.35]]

DEGRADATION1 = [[0.95, 0.05, 0, 0], [0, 0.94, 0.05, 0.01], [0, 0, 0.86, 0.14], [0, 0, 0, 1]]
DEGRADATION2 = [[0.9, 0.09, 0.01, 0], [0, 0.87, 0.11, 0.02], [0, 0, 0.79, 0.21], [0, 0, 0, 1]]

TEAMS = 1
INTERVENTION_STATE = 3

delta = 0.8


def sim_windturbine(duration, nb):
    day = 0
    wind_state = 0
    windturbines_state = [0 for _ in range(nb)]

    intervention = [0 for _ in range(TEAMS)]
    windturbines_intervention = [-1 for _ in range(nb)]
    while day < duration:

        ##

        i = 0
        while i < nb:
            turbine = windturbines_state[i]

            if turbine >= INTERVENTION_STATE and wind_state < 2 and windturbines_intervention[i] == -1:
                team = -1
                for u in range(TEAMS):
                    if intervention[u] == 0:
                        print(i)
                        team = u
                        break

                if team != -1:
                    windturbines_intervention[i] = team

            i += 1

        turbine = 0
        while turbine < nb:
            team = windturbines_intervention[turbine]

            if team != -1:
                intervention[team] += 1

                if intervention[team] == 3:
                    windturbines_state[team] = 3

                if intervention[team] == 5:
                    windturbines_state[team] = 0
                    intervention[team] = 0
                    windturbines_intervention[turbine] = -1
            turbine += 1

        efficiency = get_efficiency(windturbines_state)

        ## End of day
        windturbines_state = [get_degradation(windturbines_state[i], wind_state) for i in range(nb)]
        wind_state = get_wind_state(wind_state)
        print("Day :", day)
        print("Wind : ", wind_state)
        print("Turbine : ", windturbines_state)
        print("Efficiency : ", efficiency)
        print("Intervention : ", intervention)

        day += 1


def get_degradation(windturbine_state, wind_state):
    rand = random.randint(0, 100) / 100
    line = []

    match wind_state:
        case 1:
            line = DEGRADATION1[windturbine_state]
        case 2:
            line = DEGRADATION2[windturbine_state]

    i = 0
    while i < len(line):
        rand = rand - line[i]
        if rand <= 0 and line[i] != 0:
            return i
        i += 1
    return windturbine_state


def get_wind_state(wind_state):
    rand = random.randint(0, 100) / 100
    line = WIND[wind_state]

    i = 0
    while i < len(line):
        rand = rand - line[i]
        if rand <= 0:
            return i
        i += 1
    return 0


def get_efficiency(windturbines_state):
    available = 0
    for tubine in windturbines_state:
        if tubine < 3:
            available += 1

    return available / len(windturbines_state)


if __name__ == '__main__':
    sim_windturbine(100, 3)
