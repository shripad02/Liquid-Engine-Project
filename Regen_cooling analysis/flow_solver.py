import numpy as np
import pandas as pd

class Flow_solver:
    
    def __init__(self, geometry, coolant, mdot):
        self.geometry = geometry
        self.coolant = coolant
        self.mdot = mdot
    
    def Velocity(self, rho):
        A = self.geometry.total_flow_area()
        return self.mdot/(rho*A)
    
    def mass_flux(self):
        A = self.geometry.total_flow_area()
        return self.mdot/A
    
    def reynolds_number(self, rho, mu):
        V = self.Velocity(rho=rho)
        D = self.geometry.hydraullic_diameter()
        return (rho*V*D/mu)
    
    @staticmethod
    def flow_regime(Re):
        if Re < 2300:
            return "Laminar"
        elif Re < 4000:
            return "Transition"
        else:
            return "Turbulent"
    
    def solve_station(self, T, P):
        props = self.coolant.get_properties(T, P)
        rho = props["rho"]
        mu = props["mu"]
        V = self.Velocity(rho=rho)
        G = self.mass_flux()
        Re = self.reynolds_number(rho, mu)
        return {

            "T": T,
            "P": P,

            "rho": rho,
            "mu": mu,

            "Velocity": V,

            "MassFlux": G,

            "Re": Re,

            "FlowRegime":
            self.flow_regime(Re)

        }
        
    def solve_profile(self, temp_array, pressure_array):
        results = []
        for T, P in zip(temp_array, pressure_array):
            results.append(self.solve_station(T, P))
        return pd.DataFrame(results)
            
        
