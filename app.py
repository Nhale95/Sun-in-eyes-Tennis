from flask import Flask, render_template, request
from datetime import datetime, timedelta
from Tennis_sun_in_eyes import Court, Courts, get_sun_direction, read_courts_from_file

app = Flask(__name__)

# Dictionary to hold court locations for different boroughs
court_locations = {
    "hackney": [
        {"name": "London Fields", "file_path": "data/Hackney/London_fields.txt"},
        {"name": "Clissold Park", "file_path": "data/Hackney/Clissold_park.txt"},
        {"name": "Hackney Downs Park", "file_path": "data/Hackney/Hackney_downs_park.txt"},
    ],
    "lewisham": [
        # Example placeholders for Lewisham data
        {"name": "Catford Bridge", "file_path": "data/Lewisham/Catford_bridge.txt"},
        {"name": "Chinbrook Meadows", "file_path": "data/Lewisham/Chinbrook_meadows.txt"},
        {"name": "Hilly Fields", "file_path": "data/Lewisham/Hilly_fields.txt"},
        {"name": "Ladywell Fields", "file_path": "data/Lewisham/Ladywell_fields.txt"},
        {"name": "Manor House Gardens", "file_path": "data/Lewisham/Manor_house_gardens.txt"},
        {"name": "Mayow Park", "file_path": "data/Lewisham/Mayow_park.txt"},
    ]
    # Add more boroughs and their respective court locations here
}

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/<borough>', methods=['GET', 'POST'])
def index(borough):
    latitude = 51.509  # London latitude
    longitude = -0.02  # London longitude

    if borough.lower() not in court_locations:
        return "Borough not found", 404

    # Get court locations for the specified borough
    locations = court_locations[borough.lower()]

    if request.method == 'POST':
        start_time_str = request.form['start_time']
        start_time = datetime.fromisoformat(start_time_str)
    else:
        start_time = datetime.now()

    times = [start_time + timedelta(hours=i) for i in range(5)]
    all_table_data = {}

    for location in locations:
        courts = Courts(location["name"], read_courts_from_file(location["file_path"]).courts_list)
        table_data = []

        for court in courts.courts_list:
            row = {'court_number': court.court_number, 'bearing': court.bearing}
            for time in times:
                sun_azimuth, sun_altitude = get_sun_direction(latitude, longitude, time)
                status, colour = court.get_sun_in_eyes_status(sun_azimuth, sun_altitude)
                row[time.strftime("%H:%M")] = {'status': status, 'colour': colour}
            table_data.append(row)

        all_table_data[location["name"]] = table_data

    # Pass the borough name to the template
    return render_template('index.html', borough=borough, all_table_data=all_table_data, times=times)

@app.route('/court_detail')
def court_detail():
    location = request.args.get('location')
    court_number = request.args.get('court_number')
    time_str = request.args.get('time')
    time = datetime.strptime(time_str, "%H:%M")
    bearing = request.args.get('bearing')
    latitude = 51.509  # London latitude
    longitude = -0.02  # London longitude

    sun_azimuth, sun_altitude = get_sun_direction(latitude, longitude, time)

    return render_template('court_detail.html', location=location, court_number=court_number, time=time_str, sun_azimuth=sun_azimuth, bearing=bearing, sun_altitude=sun_altitude)

if __name__ == '__main__':
    app.run(debug=True)
