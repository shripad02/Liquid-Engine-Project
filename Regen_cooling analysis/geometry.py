import numpy as np

class RegencoolingGeo:
    def __init__(self, n_channels, width, height, rib_thickness, wall_thickness):
        self.n_channels = n_channels
        self.width = width
        self.height = height
        self.rib_thickness = rib_thickness
        self.wall_thickness = wall_thickness
    
    def channel_area(self):
        return self.width * self.height
    
    def total_flow_area(self):
        return self.n_channels*self.channel_area()
    
    def wetted_perimeter(self):
        return 2*(self.width + self.height)
    
    def hydraullic_diameter(self):
        A = self.channel_area()
        P = self.wetted_perimeter()
        return 4*A/P
    
    def coolant_volume(self, lenght):
        return self.total_flow_area()*lenght
    
    def heat_transfer_area(self, lenght):
        return ( self.wetted_perimeter*self.n_channels*lenght)
    
    def summary(self, length):

        print("\n===== GEOMETRY SUMMARY =====")

        print(
            f"Channels              : {self.n_channels}"
        )

        print(
            f"Channel Area          : {self.channel_area():.6e} m²"
        )

        print(
            f"Total Flow Area       : {self.total_flow_area():.6e} m²"
        )

        print(
            f"Hydraulic Diameter    : {self.hydraulic_diameter()*1000:.3f} mm"
        )

        print(
            f"Wetted Perimeter      : {self.wetted_perimeter()*1000:.3f} mm"
        )
        
        print(
            f"Heat Transfer Area    : {self.heat_transfer_area(length):.6f} m²"
        )

        print(
            f"Coolant Volume        : {self.coolant_volume(length):.6e} m³"
        )


