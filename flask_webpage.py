"""
Weather Prediction ML Webpage
File: flask_webpage.py
Author: John Prah
Class: CMSC 495
Date: 4/7/2022
"""

import time
from flask import Flask, request, render_template
import fairbanks

APP = Flask(__name__)


@APP.route('/')  # Decorator modifies following function
def hello_index():
    """ Returns my_reply when triggered by visit of specified path """
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


@APP.route('/result', methods=["POST", "GET"])
def form_post():
    return render_template('result.html')


APP.run(host='0.0.0.0', port=8080)
