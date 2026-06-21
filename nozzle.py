import math

# ==========================================================
# AREA RELATIONS
# ==========================================================

def throat_area(thrust, chamber_pressure, thrust_coefficient):
    """
    Calculate throat area.

    At = F / (Pc * Cf)
    """

    return thrust / (chamber_pressure * thrust_coefficient)


def exit_area(throat_area, expansion_ratio):
    """
    Calculate exit area.

    Ae = ε * At
    """

    return expansion_ratio * throat_area


# ==========================================================
# DIAMETERS
# ==========================================================

def throat_diameter(throat_area):
    """
    Calculate throat diameter.
    """

    return math.sqrt((4 * throat_area) / math.pi)


def exit_diameter(exit_area):
    """
    Calculate exit diameter.
    """

    return math.sqrt((4 * exit_area) / math.pi)


# ==========================================================
# CONICAL NOZZLE LENGTH
# ==========================================================

def nozzle_length(throat_diameter,
                  exit_diameter,
                  half_angle=15):
    """
    Conical nozzle length.

    Parameters
    ----------
    throat_diameter : m
    exit_diameter : m
    half_angle : degrees

    Returns
    -------
    Length in metres
    """

    theta = math.radians(half_angle)

    return (exit_diameter - throat_diameter) / (2 * math.tan(theta))


# ==========================================================
# SURFACE AREA
# ==========================================================

def slant_length(throat_diameter,
                 exit_diameter,
                 nozzle_length):
    """
    Slant length of the conical section.
    """

    return math.sqrt(
        nozzle_length**2 +
        ((exit_diameter - throat_diameter) / 2)**2
    )


def nozzle_surface_area(throat_diameter,
                        exit_diameter,
                        nozzle_length):
    """
    Lateral surface area.

    Useful for thermal calculations.
    """

    l = slant_length(
        throat_diameter,
        exit_diameter,
        nozzle_length
    )

    r1 = throat_diameter / 2
    r2 = exit_diameter / 2

    return math.pi * (r1 + r2) * l


# ==========================================================
# INTERNAL VOLUME
# ==========================================================

def nozzle_volume(throat_diameter,
                  exit_diameter,
                  nozzle_length):
    """
    Internal volume of a conical frustum.
    """

    r1 = throat_diameter / 2
    r2 = exit_diameter / 2

    return (
        math.pi
        * nozzle_length
        * (r1**2 + r1*r2 + r2**2)
        / 3
    )


# ==========================================================
# NOZZLE WALL ANGLE
# ==========================================================

def nozzle_half_angle(nozzle_length,
                      throat_diameter,
                      exit_diameter):
    """
    Calculates half angle from geometry.
    """

    return math.degrees(
        math.atan(
            (exit_diameter - throat_diameter)
            / (2 * nozzle_length)
        )
    )


# ==========================================================
# AXIAL PROFILE
# ==========================================================

def nozzle_profile(throat_diameter,
                   exit_diameter,
                   nozzle_length,
                   n_points=100):
    """
    Returns x and radius coordinates of
    a straight conical nozzle.
    """

    x = []
    r = []

    rt = throat_diameter / 2
    re = exit_diameter / 2

    for i in range(n_points + 1):

        xi = nozzle_length * i / n_points

        ri = rt + (re - rt) * xi / nozzle_length

        x.append(xi)
        r.append(ri)

    return x, r
