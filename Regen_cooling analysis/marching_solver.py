import pandas as pd


class MarchingSolver:

    def __init__(

        self,

        geometry,

        coolant,

        flow_solver,

        heat_transfer,

        thermal_solver,

        mdot

    ):

        self.geometry = geometry

        self.coolant = coolant

        self.flow = flow_solver

        self.ht = heat_transfer

        self.thermal = thermal_solver

        self.mdot = mdot


    def solve(

        self,

        excel_file,

        Tin,

        Pin

    ):

        df = pd.read_excel(
            excel_file
        )

        Tcool = Tin

        Pcool = Pin

        results = []

        for i in range(len(df)-1):

            row = df.iloc[i]

            next_row = df.iloc[i+1]

            dx = (

                next_row["x (m)"]

                -

                row["x (m)"]

            )

            Taw = row["Taw (K)"]

            hg = row["hg (W/m²K)"]

            # -------------------------
            # Properties
            # -------------------------

            props = self.coolant.get_properties(

                Tcool,

                Pcool

            )

            # -------------------------
            # Flow
            # -------------------------

            flow_data = self.flow.solve_station(

                Tcool,

                Pcool

            )

            # -------------------------
            # HTC
            # -------------------------

            ht_data = self.ht.solve_station(

                Re=flow_data["Re"],

                Pr=props["Pr"],

                mu=props["mu"],

                k=props["k"]

            )

            # -------------------------
            # Thermal
            # -------------------------

            thermal_data = self.thermal.solve_station(

                Taw=Taw,

                Tcool=Tcool,

                hg=hg,

                hc=ht_data["hc"]

            )

            # -------------------------
            # Heat absorbed
            # -------------------------

            A = self.geometry.local_heat_transfer_area(
                dx
            )

            Q = (

                thermal_data["HeatFlux"]

                *

                A

            )

            dT = (

                Q

                /

                (

                    self.mdot

                    *

                    props["cp"]

                )

            )

            # -------------------------
            # Pressure Drop
            # -------------------------

            # temporary estimate

            dP = 1000.0 * dx

            # -------------------------
            # Save
            # -------------------------

            results.append({

                "x": row["x (m)"],

                "Taw": Taw,

                "Tcool": Tcool,

                "Pcool": Pcool,

                "Re": flow_data["Re"],

                "Nu": ht_data["Nu"],

                "hc": ht_data["hc"],

                "HeatFlux":
                thermal_data["HeatFlux"],

                "InnerWallTemp":
                thermal_data["InnerWallTemp"],

                "OuterWallTemp":
                thermal_data["OuterWallTemp"],

                "Status":
                thermal_data["Status"]

            })

            # -------------------------
            # March
            # -------------------------

            Tcool += dT

            Pcool -= dP

        return pd.DataFrame(
            results
        )
