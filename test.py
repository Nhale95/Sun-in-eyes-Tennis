from datetime import datetime, timedelta
from Tennis_sun_in_eyes import Court, Courts, get_sun_direction, read_courts_from_file
import pyowm
import cv2
import numpy as np

#latitude = 51.509  # London latitude
#longitude = -0.02  # London longitude
#start_time = datetime.now()
#time = start_time
##time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
#time = time.replace(hour = 12,minute=0, second=0, microsecond=0) 
#sun_azimuth, sun_altitude = get_sun_direction(latitude, longitude, time)
#print("time = {}".format(time))
#print("sun_azimuth = {}".format(sun_azimuth))
#print("sun_altitude = {}".format(print(sun_altitude)))



# Initialize the OWM object with your API key
def get_weather(key,location,time):
    api_key = '4855983cf07bd31b1ecb2f0915937ff9'
    owm = pyowm.OWM(api_key)  # Initialize with API key
    
    # Create a weather manager
    mgr = owm.weather_manager()
    
    try:
        # Fetch weather at a specific place
        observation = mgr.weather_at_place(location + ', UK')  # Add ', UK' to limit the search to the UK
        weather = observation.weather

        # Get weather description
        weather_description = weather.detailed_status  # E.g., "clear sky", "light rain", "few clouds"
        return weather_description
    except pyowm.commons.exceptions.NotFoundError as e:
        return f"Location not found: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

r = get_weather("Lewisham")



def detect_lines(image_path):
    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Edge detection
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    
    # Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    
    if lines is not None:
        longest_line = None
        max_length = 0
        
        # Convert image to color to draw lines
        image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        for rho, theta in lines[:, 0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            
            # Calculate line length
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            if length > max_length:
                max_length = length
                longest_line = (x1, y1, x2, y2)
                angle = np.rad2deg(theta) - 90

        if longest_line is not None:
            # Draw the longest line (for visualization purposes)
            cv2.line(image_color, (longest_line[0], longest_line[1]), (longest_line[2], longest_line[3]), (0, 255, 0), 2)
            cv2.imshow('Longest Line', image_color)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            return angle+90

r = detect_lines("sample.png")
print(r)
r = detect_lines("sample_2.png")
print(r)