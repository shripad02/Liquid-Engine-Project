import math
import numpy as np
from scipy.optimize import fsolve

# basic equations
Impulse = float(input("Desired impulse "))
burn_time = float(int("burn time in s "))
g = 9.8 # accn due to gravity
m_dot = float(input("Mass flow rate in kg/s ")) # mass flow rate exiting nozzle
p_exit = float(input("exit pressure in Pa ")) # nozzle exit pressure
p_atm = 101325 # atm pressure in pascals
gamma = float(input("Gas constant gamma "))
R = 287 # in J/KgK units
T_c = int(input("Chamber temperature ")) # T_c is chamber temperature in K at equillibrium
P_c = int(input("Chamber Pressure ")) # P_c is chamber pressure in Pa at equillibrium
p_ratio = math.sqrt(1-pow(p_exit/P_c, gamma-1/gamma))
c_star = float(input("Input c_star value in m/s "))
O_F_ratio = input(float("O_F ratio "))

# function for calculating exit velocity
def exit_velocity():
    v_exit = math.sqrt((2*g*gamma)/(gamma+1))*math.sqrt(R*T_c)*p_ratio
    return v_exit

#function for calculating area ratio of nozzle Ae/At
def area_ratio():
    epsilon01 = pow(2/(gamma+1), 1/(gamma+1))*(pow(P_c/p_exit, 1/gamma))
    epsilon02 = math.sqrt((gamma+1)/(gamma-1))*p_ratio
    return epsilon01/epsilon02

#function to calculate pressure at throat 
def p_throat():
    p_t = P_c*pow(2/(gamma+1), gamma/(gamma+1))
    return p_t

# function to calculate velocity at throat
def V_throat():
    v_throat = math.sqrt((2*g*gamma)/(gamma+1))*math.sqrt(R*T_c)
    return 

#function to model area_mach relation
def area_mach(M_guess, a_local):
    if M_guess <= 0:
        return 1e6
    term01 = 1/M_guess
    term02 = (2/(gamma+1))*(1+(gamma-1)/2)*M_guess**2
    expo = (gamma+1)/(2*(gamma-1))
    return( term01*(term02**expo)) - a_local

# function for pressure calculation at any section and also finding local mach number
def P_x(Ax, is_divergent=True):
    a_local = Ax/A_t
    initial_guess = 2
    a_m = area_mach(initial_guess, a_local=a_local)
    if np.isclose(a_local, 1):
        M = 1
    else:
        return a_m
    M = fsolve(a_m , initial_guess)[0]
    
    P_x = P_c*(1+((gamma-1)/2)*M**2)**(-gamma/gamma-1)
    return P_x

# function to calculate velocity at any section
def V_x(p_x):
    v_t = V_throat()
    v_x = v_t*math.sqrt(pow((gamma+1)/(gamma-1)))*math.sqrt(1-pow(p_x/P_c, (gamma-1)/gamma))
    return v_x
        
        


a_r = area_ratio()
C_f = (math.sqrt(pow(2*gamma**2/(gamma-1)))*math.sqrt(pow(2/(gamma+1), 1/(gamma+1)))*p_ratio) + ((p_exit-p_atm)/P_c)*a_r # thrust coefficient
F = Impulse*burn_time
A_t = F/(P_c*C_f)
A_exit = a_r* A_t


# trhust chamber analysis
#chamber volume - for effective combution of the fuel and oxidizer the volume of combution chamber is a deciding parameter
# propellant stay time can be defined by paprameter of L_star - L_star = Vc/Athroat
L_chamber = input("Combustion chamber lenght in m ")
d_chamber = input("Combution chamber diameter ")
V_chamber = math.pi*L_chamber*d_chamber**2  #V-chamber = M_propellant*t_propellant*V_avg
L_star = V_chamber/A_t  #L_star 
# c_star increases with value of L_star upto a point , but highher L_star has a problem of pre colling and more frictional losses

#contraction ratio = Ac/A_t
A_chamber = math.pi*d_chamber**2
contraction_ratio = A_chamber/A_t # between 2 to 5 for pressure feed systems, for turbopumped high pressure systems it should be between 1.3 to 2.5
V_chamber_combustion = A_t*(L_chamber*contraction_ratio + ((math.sqrt(A_t/math.pi))/3)*1.17084*(pow(contraction_ratio, 1/3)-1)) # for 45 degree angle
Total_area_combution = 2*L_chamber*(math.sqrt(math.pi*A_t*contraction_ratio)) + (contraction_ratio - 1)*A_t

#conical nozzle parameters
D_throat = math.sqrt(4*A_t/math.pi)
D_exit = math.sqrt(4*A_exit/math.pi)
D_fillet= int()
L_nozzle = (D_throat*(area_ratio**0.5-1) + D_fillet*0.0284)/0.48015



