from datetime import datetime
from Tennis_sun_in_eyes import get_sun_direction
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import cv2
from matplotlib.patches import Rectangle
from PIL import Image
# Parameters
latitude = 51.509  # London latitude
longitude = -0.02  # London longitude
start_time = datetime.now()
time = start_time.replace(hour=12, minute=0, second=0, microsecond=0) 
sun_azimuth, sun_altitude = get_sun_direction(latitude, longitude, time)

print("time = {}".format(time))
print("sun_azimuth = {}".format(sun_azimuth))
print("sun_altitude = {}".format(sun_altitude))

# Angle to rotate (e.g., 45 degrees)
rotation_angle = -18

# Create the figure and axis
fig1, ax1 = plt.subplots(1, figsize=(20, 12), dpi=300, facecolor='white')
ax1.axis("off")

geometry_0 = [0.4, 0.1, 0.7, 0.7]
ax0=fig1.add_axes(geometry_0)

sun_day_image_path = 'static/images/sun_day.png'
img_sun_day = Image.open(sun_day_image_path)
extent = [0.45, 0.55, 0.9, 1]
ax0.imshow(img_sun_day, extent=extent, transform=ax0.transAxes)


geometry_1 = [0.5, 0.2, 0.5, 0.5]
ax1=fig1.add_axes(geometry_1)
# Load and rotate the image using Pillow
image_path = 'static/images/tennis_court.png'
img = Image.open(image_path)

# Define the angle of rotation
angle = -10  # Rotation angle in degrees
rotated_img = img.rotate(angle, expand=True)

# Convert rotated image to numpy array
rotated_img_np = np.array(rotated_img)

ax1.imshow(rotated_img_np)



geometry_2= [0.2, 0.1, 0.25, 0.25]
ax2=fig1.add_axes(geometry_2)
## Load and resize the compass image
compass_image_path = 'static/images/compass.png'  # Path to your compass image
compass_img = mpimg.imread(compass_image_path)

ax2.imshow(compass_img)



# Save the figure
fig1.savefig("tennis_with_compass.png", dpi=300, facecolor=fig1.get_facecolor())



