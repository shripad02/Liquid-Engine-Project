import math

# ==========================================================
# CONSTANTS
# ==========================================================

G0 = 9.80665          # Standard gravity (m/s²)
P_ATM = 101325        # Atmospheric pressure (Pa)

# ==========================================================
# BASIC PERFORMANCE
# ==========================================================

def thrust(total_impulse, burn_time):
    """
    Calculates average thrust.

    Parameters
    ----------
    total_impulse : float
        Total impulse (N·s)

    burn_time : float
        Burn duration (s)

    Returns
    -------
    float
        Average thrust (N)
    """

    return total_impulse / burn_time


def mass_flow_rate(propellant_mass, burn_time):
    """
    Calculates average mass flow rate.

    m_dot = m / t
    """

    return propellant_mass / burn_time


def characteristic_velocity(Pc, At, mdot):
    """
    Characteristic velocity.

    c* = Pc At / mdot
    """

    return (Pc * At) / mdot


def thrust_coefficient(gamma, Pc, Pe, area_ratio,
                       Pa=P_ATM):
    """
    Calculates thrust coefficient.

    Cf = Momentum term + Pressure term
    """

    momentum = math.sqrt(

        (2 * gamma**2 / (gamma - 1))

        * (2 / (gamma + 1))
        ** ((gamma + 1) / (gamma - 1))

        * (1 - (Pe / Pc)
        ** ((gamma - 1) / gamma))

    )

    pressure = ((Pe - Pa) / Pc) * area_ratio

    return momentum + pressure


def specific_impulse(thrust, mdot):
    """
    Isp = F / (m_dot g0)
    """

    return thrust / (mdot * G0)


def effective_exhaust_velocity(Isp):
    """
    c = Isp g0
    """

    return Isp * G0


def throat_area(thrust, Pc, Cf):
    """
    At = F / (Pc Cf)
    """

    return thrust / (Pc * Cf)


def exit_area(throat_area, expansion_ratio):
    """
    Ae = ε At
    """

    return throat_area * expansion_ratio


# ==========================================================
# EXHAUST VELOCITY
# ==========================================================

def exit_velocity(gamma, R, Tc, Pc, Pe):
    """
    Ideal isentropic exhaust velocity.
    """

    return math.sqrt(

        (2 * gamma * R * Tc)

        / (gamma - 1)

        * (1 - (Pe / Pc)
        ** ((gamma - 1) / gamma))

    )


# ==========================================================
# THROAT CONDITIONS
# ==========================================================

def throat_pressure(Pc, gamma):
    """
    Critical pressure.
    """

    return Pc * (2 / (gamma + 1)) ** (gamma / (gamma - 1))


def throat_temperature(Tc, gamma):
    """
    Critical temperature.
    """

    return Tc * (2 / (gamma + 1))


def throat_density(Pc, Tc, gamma, R):
    """
    Density at throat.
    """

    Pt = throat_pressure(Pc, gamma)
    Tt = throat_temperature(Tc, gamma)

    return Pt / (R * Tt)


def throat_velocity(gamma, R, Tc):
    """
    Sonic velocity at throat.

    M = 1
    """

    Tt = throat_temperature(Tc, gamma)

    return math.sqrt(gamma * R * Tt)
