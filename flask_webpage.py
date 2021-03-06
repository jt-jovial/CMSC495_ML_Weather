"""
Weather Prediction ML Webpage
File: flask_webpage.py
Author: John Prah
Class: CMSC 495
Date: 4/7/2022
"""

import time
from flask import Flask, request, render_template
from fairbanks import season_predict, temperature, daylight_hours, snowfall, northern_lights
import month_content

APP = Flask(__name__)


@APP.route('/')  # Decorator modifies following function
def hello_index():
    """ Returns my_reply (main webpage) when triggered by visit of specified path """

    my_reply = """
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href='/static/main.css' />
    <title>Visiting Fairbanks, Alaska</title>
</head>
<header>
    <img src="/static/Header.jpg" alt="Visiting Fairbanks, AK" style="width:624px;height:195px;">
</header>
<body>
    <script type="text/javascript" src="static/scripts.js"></script>
    <p id="prime">
        <label for="prime-factor">What is the most important factor for you when visiting Fairbanks, Alaska?</label><br>
        <select name="prime-factor" id="prime-factor" onchange="select(this)"> //may need form ak-form to pull
            <option value=""></option>
            <option value="temp">Temperature</option>
            <option value="daylight">Daylight Hours</option>
            <option value="snowfall">Snowfall</option>
            <option value="northernlights">Northern Lights</option>
        </select>
    </p>
    <p id="dynamic-form"></p>
    <p id="daylight-form"></p>
    <p id="execute-button"></p>
</body>
<footer>
    <h3> Thank you for visiting! </h3>
    <!-- Calls the python internal time module for current time/date -->
    The current time and date (in UTC) are: """ + time.ctime() + """
</footer>
</html>
"""
    return my_reply


@APP.route('/result', methods=["POST"])
def form_post(result=None):
    """
    Received the form as posted from the main webpage and returns results

    Data is extracted from the request.form dictionary, and the correct ML
    algorithm is selected by determining the presence of particular keys
    as specified in the JavaScript.

    Result month from ML method is passed through to the results.html page
    and dynamic content is inserted based on the month.

    Post is handled through the request.form object with the following valid keys:
        day-check
        daylight
        day_submit
        light_submit
        snow
        snow_submit
        temp
        temp_submit

    Returns:
        results.html with pass-through dynamic content
    """

    yt_dict = {  # Video IDs for results page per month
        '1': '4a9ReaUJKRM',
        '2': 'Z5lE1yBAUcM',
        '3': 'KFUQ25DlbzM',
        '4': 'NumGlgKQ0WU',
        '5': 'DMIuymECl1U',
        '6': 'Qsw6f62wH34',
        '7': 'MHYTma3HcHs',
        '8': '2dApeKmzL6M',
        '9': 'jpR7eRKUpI8',
        '10': 'YBUVvbXi9vM',
        '11': 'vOJS_-S9C5c',
        '12': 'vqSn-PXY4Y8'
    }

    month_map = {  # Maps month name to number
        '1': 'January',
        '2': 'February',
        '3': 'March',
        '4': 'April',
        '5': 'May',
        '6': 'June',
        '7': 'July',
        '8': 'August',
        '9': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
    }

    if request.method == 'POST':

        if 'day-check' in request.form:
            if request.form['day-check'] == 'true':
                daylight = 1
                hours = float(request.form['daylight'])
            else:
                daylight = 2
                hours = None
        if "temp_submit" in request.form:
            # temperature(temp, season, daylight, hours=None)
            season = season_predict(request.form['temp'])
            result = temperature(request.form['temp'], season, daylight, hours)
        elif "day_submit" in request.form:
            # daylight_hours(hours, choice=3)
            hours = float(request.form['daylight'])
            result = daylight_hours(hours)
        elif "snow_submit" in request.form:
            # snowfall(snow, daylight, hours=None)
            result = snowfall(request.form['snow'], daylight, hours)
        elif "light_submit" in request.form:
            # northern_lights(daylight, snowfall_pref, hours=None, snow=None)
            result = northern_lights(daylight, 2, hours)
            # need to verify snowfall_pref and snow are redundant
        for i in request.form:
            print(i, request.form[i])

        print("Result is " + str(result))
        result = int(result)
    return render_template('result.html',
                           month=month_map[str(result)],
                           yt=yt_dict[str(result)],
                           content=month_content.CONTENT[str(result)])


APP.run(host='0.0.0.0', port=8080)
