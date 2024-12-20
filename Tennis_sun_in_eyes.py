from astral import LocationInfo
import astral
from astral.sun import sun
from datetime import datetime
from datetime import datetime, timedelta
import math
from prettytable import PrettyTable
from termcolor import colored



def get_sun_direction(latitude, longitude, date_time):
    location = LocationInfo(latitude=latitude, longitude=longitude)
    azimuth =astral.sun.azimuth(location,dateandtime  = date_time)
    elevation =astral.sun.elevation(location,dateandtime  = date_time)

    return azimuth,elevation #azimuth, altitude

class Court:
    def __init__(self, court_number, start_lat, start_lon, end_lat, end_lon):
        self.court_number = court_number
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.end_lat = end_lat
        self.end_lon = end_lon
        self.bearing = self.calculate_bearing()

    def calculate_bearing(self):
        lat1 = math.radians(self.start_lat)
        lon1 = math.radians(self.start_lon)
        lat2 = math.radians(self.end_lat)
        lon2 = math.radians(self.end_lon)

        dlon = lon2 - lon1
        x = math.sin(dlon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(dlon))
        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        return compass_bearing

    def get_sun_in_eyes_status(self,sun_azimuth,sun_altitude):
        relative_angle = abs(self.bearing-sun_azimuth)
        if relative_angle > 90:
            relative_angle = 180-relative_angle

        
        if relative_angle <= direct_angle_degrees and 0 < sun_altitude<=direct_altitude:
            return ["direct light", "#ffcab0"]

        elif ((direct_angle_degrees <=relative_angle <= peripheral_angle) and (0 <=sun_altitude <= peripheral_altitude)) or ((direct_altitude <=sun_altitude <= peripheral_altitude) and (relative_angle <= peripheral_angle)):
            return ["Peripheral light", "#fdffcd"]
        elif sun_altitude < 0:
            return ["Not enough light", "#53a8b6"]
        else:
            return ["Good conditions", "#e0ffcd"]


class Courts:
    def __init__(self,courts_name,courts_list):
        self.courts_name = courts_name
        self.courts_list = courts_list

    def display_sun_in_eyes_table(self, latitude, longitude):
        now = datetime.now()
        current_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        times = [current_time + timedelta(hours=i) for i in range(5)]
      
        table = PrettyTable()
        table.field_names = ["Court Number"] + [t.strftime("%H:%M") for t in times]
        for court in self.courts_list:
            row = [court.court_number]
            for time in times:
                sun_azimuth, sun_altitude = get_sun_direction(latitude, longitude, time)
                status,colour = court.get_sun_in_eyes_status(sun_azimuth, sun_altitude)
                #print(" time = {}, Sun azimuth = {}, Sun altitude = {}, tennis sun status = {}".format(time.hour,sun_azimuth,sun_altitude,status))
                row.append(colored(status, colour))
            table.add_row(row)
        
        print(table)

def read_courts_from_file(filename):
    courts_ = []
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()
        
        for i,line in enumerate(data.strip().split('\n')):
            
            if i == 0:
                name = line.strip

            else:
                parts = line.split('\t')
                court_number = int(parts[0])
                start_lat = float(parts[1])
                start_lon = float(parts[2])
                end_lat = float(parts[3])
                end_lon = float(parts[4])
                court = Court(court_number, start_lat, start_lon, end_lat, end_lon)
                courts_.append(court)
    return Courts(name,courts_)

direct_angle_radians =math.atan2(5.49, 23.77)
direct_angle_degrees = math.degrees(direct_angle_radians)
direct_altitude = 35
peripheral_altitude = 60
peripheral_angle = 45

## Example usage
latitude = 51.509  # London latitude
longitude = -0.02  # London longitude

#now = datetime.now()
#current_time = now.replace(hour = 18,minute=0, second=0, microsecond=0) + timedelta(hours=1)
#times = [current_time + timedelta(hours=i) for i in range(5)]
    
## Dictionary to hold table data for each location
#all_table_data = {}
#table_data = []
##print("Hackney tennis courts")
#c = read_courts_from_file("data/Hackney/London_fields.txt")
#for court in c.courts_list:
#            row = {'court_number': court.court_number}
#            for time in times:
#                sun_azimuth, sun_altitude = get_sun_direction(latitude, longitude, time)
#                status, colour = court.get_sun_in_eyes_status(sun_azimuth, sun_altitude)
#                print("Time_hour = {}, sun azimuth = {}, sun altitute = {}".format(time.hour,sun_azimuth,sun_altitude))
#                row[time.strftime("%H:%M")] = {'status': status, 'colour': colour}
#            table_data.append(row)

#c.display_sun_in_eyes_table(latitude,longitude)

