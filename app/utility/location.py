import math
#haversine formula use garen distance calculate garna ko lagi
class LocationUtility:
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):#distance calculation garen formula 6371 earth ko radius 

     dlat = math.radians(lat2 - lat1)
     dlon = math.radians(lon2 - lon1)
     a=math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
     c=2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
     return 6371 * c # distance in kilometers hunxa 
