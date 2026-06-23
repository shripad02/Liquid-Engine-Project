class ThermalSolver:

    def __init__(
        self,
        geometry,
        material
    ):

        self.geometry = geometry

        self.material = material


    def total_resistance(
        self,
        hg,
        hc
    ):

        t = self.geometry.wall_thickness

        k = self.material.conductivity()

        return (

            1/hg

            +

            t/k

            +

            1/hc

        )



    def heat_flux(
        self,
        Taw,
        Tcool,
        hg,
        hc
    ):

        R = self.total_resistance(
            hg,
            hc
        )

        return (

            Taw
            -
            Tcool

        ) / R



    def inner_wall_temp(
        self,
        Taw,
        q,
        hg
    ):

        return Taw - q/hg



    def outer_wall_temp(
        self,
        Tcool,
        q,
        hc
    ):

        return Tcool + q/hc



    def solve_station(
        self,
        Taw,
        Tcool,
        hg,
        hc
    ):

        q = self.heat_flux(
            Taw,
            Tcool,
            hg,
            hc
        )

        Twi = self.inner_wall_temp(
            Taw,
            q,
            hg
        )

        Two = self.outer_wall_temp(
            Tcool,
            q,
            hc
        )

        return {

            "HeatFlux": q,

            "InnerWallTemp": Twi,

            "OuterWallTemp": Two

        }
