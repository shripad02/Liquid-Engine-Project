import math
from scipy.optimize import fsolve

# ==========================================================
# TEMPERATURE RELATIONS
# ==========================================================

def static_temperature(T0, gamma, M):
    """
    Static temperature

    T = T0 / (1 + ((γ-1)/2) M²)
    """

    return T0 / (1 + ((gamma - 1) / 2) * M**2)


def total_temperature(T, gamma, M):
    """
    Total (stagnation) temperature

    T0 = T(1 + ((γ-1)/2) M²)
    """

    return T * (1 + ((gamma - 1) / 2) * M**2)


# ==========================================================
# PRESSURE RELATIONS
# ==========================================================

def static_pressure(P0, gamma, M):
    """
    Static pressure

    P = P0 / (1 + ((γ-1)/2) M²)^(γ/(γ-1))
    """

    return P0 / (
        1 + ((gamma - 1) / 2) * M**2
    ) ** (gamma / (gamma - 1))


def total_pressure(P, gamma, M):
    """
    Total pressure

    P0 = P(1 + ((γ-1)/2) M²)^(γ/(γ-1))
    """

    return P * (
        1 + ((gamma - 1) / 2) * M**2
    ) ** (gamma / (gamma - 1))


# ==========================================================
# DENSITY RELATIONS
# ==========================================================

def static_density(rho0, gamma, M):
    """
    Static density

    ρ = ρ0 / (1 + ((γ-1)/2) M²)^(1/(γ-1))
    """

    return rho0 / (
        1 + ((gamma - 1) / 2) * M**2
    ) ** (1 / (gamma - 1))


def density(P, R, T):
    """
    Ideal gas law

    ρ = P / RT
    """

    return P / (R * T)


# ==========================================================
# SPEED OF SOUND
# ==========================================================

def speed_of_sound(gamma, R, T):
    """
    Local speed of sound

    a = √γRT
    """

    return math.sqrt(gamma * R * T)


# ==========================================================
# FLOW VELOCITY
# ==========================================================

def velocity(M, gamma, R, T):
    """
    Local flow velocity

    V = Ma
    """

    a = speed_of_sound(gamma, R, T)

    return M * a


# ==========================================================
# MACH NUMBER
# ==========================================================

def mach_number(V, gamma, R, T):
    """
    Mach number

    M = V / a
    """

    a = speed_of_sound(gamma, R, T)

    return V / a


# ==========================================================
# AREA-MACH RELATION
# ==========================================================

def area_mach_equation(M, gamma, area_ratio):
    """
    Isentropic area-Mach equation.

    Used internally by fsolve.
    """

    lhs = (1 / M) * (
        (2 / (gamma + 1))
        * (1 + ((gamma - 1) / 2) * M**2)
    ) ** ((gamma + 1) / (2 * (gamma - 1)))

    return lhs - area_ratio


def mach_from_area(area_ratio, gamma, supersonic=True):
    """
    Solve Mach number from A/A*

    Parameters
    ----------
    area_ratio : float

    supersonic : bool
        True -> supersonic root
        False -> subsonic root
    """

    guess = 2.5 if supersonic else 0.2

    M = fsolve(
        area_mach_equation,
        guess,
        args=(gamma, area_ratio)
    )[0]

    return M


# ==========================================================
# EXIT CONDITIONS
# ==========================================================

def exit_conditions(P0, T0, gamma, R, area_ratio):
    """
    Computes exit properties from chamber conditions.
    """

    M = mach_from_area(area_ratio, gamma, True)

    T = static_temperature(T0, gamma, M)

    P = static_pressure(P0, gamma, M)

    rho = density(P, R, T)

    a = speed_of_sound(gamma, R, T)

    V = velocity(M, gamma, R, T)

    return {
        "Mach": M,
        "Temperature": T,
        "Pressure": P,
        "Density": rho,
        "Speed_of_sound": a,
        "Velocity": V
    }
