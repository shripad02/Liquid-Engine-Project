import math

# ==========================================================
# CHAMBER GEOMETRY
# ==========================================================

def chamber_area(chamber_diameter):
    """
    Cross-sectional area of combustion chamber.

    Ac = πDc²/4
    """

    return (math.pi * chamber_diameter**2) / 4


def chamber_volume(chamber_diameter,
                   chamber_length):
    """
    Cylindrical chamber volume.

    Vc = πDc²Lc/4
    """

    return (
        math.pi
        * chamber_diameter**2
        * chamber_length
        / 4
    )


# ==========================================================
# CHARACTERISTIC LENGTH
# ==========================================================

def characteristic_length(chamber_volume,
                          throat_area):
    """
    Characteristic Length

    L* = Vc / At
    """

    return chamber_volume / throat_area


def chamber_volume_from_Lstar(L_star,
                              throat_area):
    """
    Required chamber volume.

    Vc = L* At
    """

    return L_star * throat_area


def chamber_length(chamber_volume,
                   chamber_diameter):
    """
    Chamber length.

    L = 4Vc / πDc²
    """

    return (
        4 * chamber_volume
    ) / (
        math.pi * chamber_diameter**2
    )


# ==========================================================
# CONTRACTION RATIO
# ==========================================================

def contraction_ratio(chamber_area,
                      throat_area):
    """
    Ac / At
    """

    return chamber_area / throat_area


def chamber_area_from_ratio(throat_area,
                            contraction_ratio):
    """
    Ac = (Ac/At) At
    """

    return contraction_ratio * throat_area


def chamber_diameter(chamber_area):
    """
    Chamber diameter.
    """

    return math.sqrt(
        (4 * chamber_area)
        / math.pi
    )


# ==========================================================
# CHAMBER RESIDENCE TIME
# ==========================================================

def residence_time(chamber_volume,
                   mass_flow_rate,
                   density):
    """
    Propellant residence time.

    τ = V / Q

    Q = mdot / ρ
    """

    volumetric_flow = mass_flow_rate / density

    return chamber_volume / volumetric_flow


# ==========================================================
# CHAMBER GAS DENSITY
# ==========================================================

def chamber_density(chamber_pressure,
                    gas_constant,
                    chamber_temperature):
    """
    Ideal gas equation.

    ρ = P / RT
    """

    return chamber_pressure / (
        gas_constant
        * chamber_temperature
    )


# ==========================================================
# STAY TIME (Alternative)
# ==========================================================

def stay_time(chamber_mass,
              mass_flow_rate):
    """
    Gas stay time.

    τ = m/mdot
    """

    return chamber_mass / mass_flow_rate


# ==========================================================
# CONVERGING SECTION
# ==========================================================

def converging_length(chamber_diameter,
                      throat_diameter,
                      converging_half_angle=45):
    """
    Straight conical converging section.
    """

    theta = math.radians(converging_half_angle)

    return (
        chamber_diameter
        - throat_diameter
    ) / (
        2 * math.tan(theta)
    )


# ==========================================================
# TOTAL CHAMBER LENGTH
# ==========================================================

def total_chamber_length(cylindrical_length,
                         converging_length):
    """
    Overall chamber length.
    """

    return cylindrical_length + converging_length


# ==========================================================
# CHAMBER WETTED AREA
# ==========================================================

def wetted_area(chamber_diameter,
                chamber_length):
    """
    Cylindrical wall area.

    Useful for cooling calculations.
    """

    return (
        math.pi
        * chamber_diameter
        * chamber_length
    )


# ==========================================================
# CHAMBER MASS
# ==========================================================

def chamber_gas_mass(chamber_density,
                     chamber_volume):
    """
    Gas mass inside chamber.

    m = ρV
    """

    return chamber_density * chamber_volume
