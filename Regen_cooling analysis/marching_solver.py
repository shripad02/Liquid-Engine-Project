mport pandas as pd
import numpy as np

class MarchingSolver:
    def __init__(self, geometry, coolant, flow_solver, heat_transfer, thermal_solver, filmcooling, mdot):
        self.geometry = geometry
        self.coolant = coolant
        self.flow_solver = flow_solver
        self.heat_transfer = heat_transfer
        self.thermal_solver = thermal_solver
        self.film_cooling = filmcooling
        self.mdot = mdot
    
    def read_rpa_file(self, excel_file):
        df = pd.read_excel(excel_file)
        df.columns = [str(col).strip() for col in df.columns]
        return df
    
    #Darcy pressure loss equation
    def pressure_drop(self, Re, rho, velocity, dx):
        Dh = self.geometry.hydraullic_diameter()
        f = 0.316*Re**(-0.25)
        dP = (f*dx/Dh*rho*velocity**2/2)
        return dP
    
    #Main marching solver
    def solve(self, excel_file, Tin, Pin):
        df = self.read_rpa_file(excel_file)
        Tcool = Tin
        Pcool = Pin
        
        results = []
        
        for i in range(len(df)-1, 0, -1):
            
            row = df.iloc[i]
            next_row = df.iloc[i+1]
            
            x = row["x(mm)"]/1000 # in m
            x_next = next_row["x(mm)"]/1000 # in m
            radius = row["Radius, mm"]/1000
            
            dx = x_next - x
            
            hg = (row["Conv. heat coeff., kW/m^2-K"]*1000)
            Twg = row["Twg, K"]
            
            film_result = (
                self.film_cooling.corrected_temperature(
                    x=x,
                    Twg=Twg
                )
            )
            Thot = film_result["CorrectedTemperature"]
            
            props = self.coolant.get_properties(T=Tcool, P=Pcool)
            
            rho = props["rho"]
            mu = props["mu"]
            cp = props["cp"]
            Pr = props["Pr"]
            k = props["k"]
            
            print(f"Tcool = {Tcool:.2f}")
            print(f"Pcool={Pcool/1e6:.3f}")
            
            flow = self.flow_solver.solve_station(T=Tcool, P=Pcool)
            velocity = flow["Velocity"]
            Re = flow["Re"]
            
            print(
                f"Velocity={velocity:.3f} m/s |" f"Re={Re:1f}"
            )
            
            ht = self.heat_transfer.solve_station(Re = Re, Pr = Pr, mu = mu, mu_wall = mu, k = k)
            hc = ht["hc"]
            
            thermal = self.thermal_solver.solve_station(Thot = Thot, Tcool = Tcool, hg = hg, hc=hc)
            q_flux = thermal["HeatFlux"]
            
            A_heat = (2*np.pi*radius*dx)
            
            Q = q_flux*A_heat
            
            dT = (Q/(self.mdot*cp))
            
            dP = self.pressure_drop(Re, rho, velocity, dx)
            Dh = self.geometry.hydraullic_diameter()
            
            print(f"Dh={Dh:.6e} m " f"dP={dP:.2f} Pa")
            print(f"HeatFlux={q_flux:.3e} W/m^2")
            print(f"Pressure Before = {Pcool:.2f} Pa")
            print(f"Pressure Drop = {dP:.2f} Pa")
            print(f"Pressure After = {Pcool-dP:.2f} Pa")
            
            results.append({
                "x_m": x,
                "Radius_m": radius,
                "Coolant_Temp_K": Tcool,
                "CoolantPressure_Mpa": Pcool/1e6,
                "Velocity_mps": velocity,
                "Re" : Re,
                "Nu" : ht["Nu"],
                "hc_Wm2K": hc,
                "HeatFlux_Wm2": q_flux,
                "HeatAdded_W": Q,
                "dT_K": dT,
                "dP_Pa":dP,
                "InnerWallTemp_K":thermal["InnerWallTemp"],
                "CoolantSideWallTemp_K":thermal["CoolantSideWallTemp"],
                "TotalResistance": thermal["TotalResistance"],
                "OuterMargin":thermal["OuterMargin"],
                "FilmEffectiveness":film_result["FilmEffectiveness"],
                "Status": ",".join(thermal["Status"])
            })
            
            Tcool += dT
            Pcool -= dP
            
            if Pcool <=0:
                raise ValueError(
                    f"Pressure became negative at x={x:.6f} m "
                )
            if Tcool > 1500:
                raise ValueError(
                        f"Coolant temperature runaway at x={x:.6f} m"
                    )
        return pd.DataFrame(results)
    
