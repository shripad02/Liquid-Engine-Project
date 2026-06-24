class ThermalSolver:

    def __init__(
        self,
        geometry,
        material
    ):

        self.geometry = geometry
        self.material = material

    # ----------------------------------
    # Total Thermal Resistance
    # ----------------------------------

    def total_resistance(
        self,
        hg,
        hc
    ):

        t = self.geometry.wall_thickness

        k = self.material.conductivity()

        return (

            1.0 / hg

            +

            t / k

            +

            1.0 / hc

        )

    # ----------------------------------
    # Heat Flux
    # ----------------------------------

    def heat_flux(
        self,
        Thot,
        Tcool,
        hg,
        hc
    ):

        Rtot = self.total_resistance(
            hg,
            hc
        )

        q = (

            Thot
            -
            Tcool

        ) / Rtot

        return q

    # ----------------------------------
    # Hot Side Wall Temperature
    # ----------------------------------

    def inner_wall_temp(
        self,
        Thot,
        q,
        hg
    ):

        return (

            Thot
            -
            q / hg

        )

    # ----------------------------------
    # Coolant Side Wall Temperature
    # ----------------------------------

    def outer_wall_temp(
        self,
        Tcool,
        q,
        hc
    ):

        return (

            Tcool
            +
            q / hc

        )

    # ----------------------------------
    # Thermal Safety Check
    # ----------------------------------

    def thermal_check(
        self,
        Twi,
        Twc
    ):

        status = []

        if Twc > self.material.max_outer_wall_temp:

            status.append(
                "OUTER WALL LIMIT EXCEEDED"
            )

        if Twi > self.material.max_inner_wall_temp:

            status.append(
                "INNER WALL LIMIT EXCEEDED"
            )

        if len(status) == 0:

            status.append(
                "PASS"
            )

        return status

    # ----------------------------------
    # Thermal Margin
    # ----------------------------------

    def thermal_margin(
        self,
        Twi,
        Twc
    ):

        outer_margin = (

            self.material.max_outer_wall_temp
            -
            Twc

        )

        inner_margin = (

            self.material.max_inner_wall_temp
            -
            Twi

        )

        return {

            "OuterMargin": outer_margin,

            "InnerMargin": inner_margin

        }

    # ----------------------------------
    # Solve One Station
    # ----------------------------------

    def solve_station(
        self,
        Thot,
        Tcool,
        hg,
        hc
    ):

        q = self.heat_flux(

            Thot,
            Tcool,
            hg,
            hc

        )

        Twi = self.inner_wall_temp(

            Thot,
            q,
            hg

        )

        Twc = self.outer_wall_temp(

            Tcool,
            q,
            hc

        )

        margin = self.thermal_margin(

            Twi,
            Twc

        )

        status = self.thermal_check(

            Twi,
            Twc

        )

        return {

            "HeatFlux": q,

            "InnerWallTemp": Twi,

            "CoolantSideWallTemp": Twc,

            "TotalResistance":
            self.total_resistance(
                hg,
                hc
            ),

            "InnerMargin":
            margin["InnerMargin"],

            "OuterMargin":
            margin["OuterMargin"],

            "Status":
            status

        }    
