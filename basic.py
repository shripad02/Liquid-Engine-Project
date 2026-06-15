import math


# basic thrust equation
Ae = float(input("Nozzle outer area in m^2")) # exit area of nozzle
g = 9.8 # accn due to gravity
m_dot = float(input("Mass flow rate in kg/s")) # mass flow rate exiting nozzle
p_exit = float(input("exit pressure in Pa")) # nozzle exit pressure
p_atm = 101325 # atm pressure in pascals
gamma = float(input("Gas constant gamma"))
R = 287 # in J/KgK units
T_c = int(input("Chamber temperature")) # T_c is chamber temperature in K at equillibrium
P_c = int(input("Chamber Pressure")) # P_c is chamber pressure in Pa at equillibrium
p_ratio = math.sqrt(1-pow(p_exit/P_c, gamma-1/gamma))

# function for calculating exit velocity
def exit_velocity():
    v_exit = math.sqrt((2*g*gamma)/gamma+1)*math.sqrt(R*T_c)*p_ratio
    return v_exit

#function for calculating area ratio of nozzle

print(p_ratio)