from geometry import RegencoolingGeo
from flow_solver import Flow_solver
from heat_transfer import HeatTransfer
from thermal_solver import ThermalSolver
from material import SS308L
from marching_solver import MarchingSolver

from coolant import Coolant
from filmcooling import FilmCooling

geometry = RegencoolingGeo(16, 0.0008, 0.0008, 0.0008, 0.001)
coolant = Coolant("coolprop")
flow_s = Flow_solver(geometry, coolant, 0.2)
material = SS308L()
thermal_s = ThermalSolver(geometry, material)
heat_s = HeatTransfer(geometry)
film_cooling = FilmCooling(0.3, 0.15, 400)

excel = "Regen_cooling analysis\heatanalysis.xlsx"

ms = MarchingSolver(geometry, coolant, flow_s, heat_s, thermal_s, film_cooling, 0.2)
re = ms.solve(excel, 300, 2.6e06)
print(re.iloc[22])
