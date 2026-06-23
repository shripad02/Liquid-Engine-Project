"""
Module 02
Coolant Property Manager

Supported Backends:

1. constant
2. correlation
3. coolprop

Usage:

coolant = Coolant(backend="correlation")

props = coolant.get_properties(
    T=350,
    P=2.5e6
)
"""

import numpy as np


# ==================================================
# CONSTANT PROPERTY MODEL
# ==================================================

class EthanolConstant:

    def get_properties(self, T, P):

        rho = 785.0
        mu = 1.10e-3
        cp = 2500.0
        k = 0.17

        Pr = cp * mu / k

        return {
            "rho": rho,
            "mu": mu,
            "cp": cp,
            "k": k,
            "Pr": Pr
        }


# ==================================================
# CORRELATION MODEL
# ==================================================

class EthanolCorrelation:

    def density(self, T):

        return 806.0 - 0.88 * (T - 273.15)

    def viscosity(self, T):

        return (
            1.2e-3 *
            np.exp(
                -0.018 * (T - 293.15)
            )
        )

    def cp(self, T):

        return (
            2400.0
            +
            2.5 * (T - 300)
        )

    def conductivity(self, T):

        return (
            0.171
            -
            1.5e-4 * (T - 300)
        )

    def get_properties(self, T, P):

        rho = self.density(T)

        mu = self.viscosity(T)

        cp = self.cp(T)

        k = self.conductivity(T)

        Pr = cp * mu / k

        return {
            "rho": rho,
            "mu": mu,
            "cp": cp,
            "k": k,
            "Pr": Pr
        }


# ==================================================
# COOLPROP MODEL
# ==================================================

class EthanolCoolProp:

    def __init__(self):

        try:

            from CoolProp.CoolProp import PropsSI

            self.PropsSI = PropsSI

        except ImportError:

            raise ImportError(
                "\nInstall CoolProp:\n"
                "pip install CoolProp"
            )

    def get_properties(self, T, P):

        PropsSI = self.PropsSI

        rho = PropsSI(
            "D",
            "T", T,
            "P", P,
            "Ethanol"
        )

        mu = PropsSI(
            "V",
            "T", T,
            "P", P,
            "Ethanol"
        )

        cp = PropsSI(
            "C",
            "T", T,
            "P", P,
            "Ethanol"
        )

        k = PropsSI(
            "L",
            "T", T,
            "P", P,
            "Ethanol"
        )

        Pr = PropsSI(
            "PRANDTL",
            "T", T,
            "P", P,
            "Ethanol"
        )

        return {
            "rho": rho,
            "mu": mu,
            "cp": cp,
            "k": k,
            "Pr": Pr
        }


# ==================================================
# MAIN WRAPPER CLASS
# ==================================================

class Coolant:

    def __init__(
        self,
        backend="correlation"
    ):

        self.backend = backend

        if backend == "constant":

            self.model = EthanolConstant()

        elif backend == "correlation":

            self.model = EthanolCorrelation()

        elif backend == "coolprop":

            self.model = EthanolCoolProp()

        else:

            raise ValueError(
                "Unknown backend.\n"
                "Use: constant, correlation, coolprop"
            )

    def get_properties(
        self,
        T,
        P
    ):

        return self.model.get_properties(
            T,
            P
        )

    def print_properties(
        self,
        T,
        P
    ):

        props = self.get_properties(
            T,
            P
        )

        print("\n===== COOLANT PROPERTIES =====")

        print(
            f"Backend : {self.backend}"
        )

        print(
            f"T = {T:.1f} K"
        )

        print(
            f"P = {P/1e6:.3f} MPa"
        )

        print(
            f"Density      : {props['rho']:.3f} kg/m³"
        )

        print(
            f"Viscosity    : {props['mu']:.5e} Pa.s"
        )

        print(
            f"Cp           : {props['cp']:.2f} J/kg-K"
        )

        print(
            f"Conductivity : {props['k']:.5f} W/m-K"
        )

        print(
            f"Prandtl      : {props['Pr']:.3f}"
        )
        

