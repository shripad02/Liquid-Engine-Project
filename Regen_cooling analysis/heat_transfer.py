import numpy as np

class HeatTransfer:
    def __init__(self, geometry):
        self.geometry = geometry
    
    #dittus_boelter equation
    @staticmethod
    def dittus_boelter(Re, Pr):
        return (0.023*Re**0.8*Pr**0.4)
    
    #Sieder-Tate equation
    @staticmethod
    def sieder_tate(Re, Pr, mu, mu_wall):
        return (0.027*
                Re**0.8*
                Pr**(1/3)*
                (mu/mu_wall)**0.14)
    
    def htc(self, Nu, k):
        Dh = self.geometry.hydraullic_diameter()
        return ( Nu*k/Dh)
    
    def solve_station(self, Re, Pr, k, mu ,mu_wall=None,):
        if mu_wall ==None:
            mu_wall = mu
            Nu = self.sieder_tate(Re, Pr, mu, mu_wall)
        
        hc = self.htc(Nu, k)
        return {"Nu": Nu, "hc": hc}
    
