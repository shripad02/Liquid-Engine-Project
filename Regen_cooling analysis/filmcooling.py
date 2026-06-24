import numpy as np


class FilmCooling:

    def __init__(
        self,
        chamber_length,
        film_fraction, 
        T_film
    ):

        self.L = chamber_length

        self.film_fraction = film_fraction
        self.T_film = T_film

    # ----------------------------------
    # Initial Effectiveness
    # ----------------------------------

    def initial_effectiveness(self):

        eta0 = (

            4.0
            *
            self.film_fraction

        )

        eta0 = min(
            eta0,
            0.9
        )

        return eta0

    # ----------------------------------
    # Local Effectiveness
    # ----------------------------------

    def effectiveness(
        self,
        x
    ):

        eta0 = self.initial_effectiveness()

        a = 2.0

        eta = (

            eta0

            *

            np.exp(
                -a
                *
                x
                /
                self.L
            )

        )

        return eta

    # ----------------------------------
    # Corrected Hot Side Temperature
    # ----------------------------------

    def corrected_temperature(
        self,
        x,
        Twg,
    ):

        eta = self.effectiveness(
            x
        )

        Thot_eff = (

            Twg

            -

            eta

            *

            (

                Twg
                -
                self.T_film

            )

        )

        return {

            "FilmEffectiveness":
            eta,

            "CorrectedTemperature":
            Thot_eff

        }
