"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT
"""

import os

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

courses = pd.read_csv('./data/olin-courses-16-17.csv')

icons = {
    "AHSE": "paint-brush",
    "CIE": "laptop",
    "ENGR": "cogs",
    "MTH": "area-chart",
    "OIE": "book",
    "OIP": "briefcase",
    "SCI": "flask",
    "SEM": "users",
    "SUST": "leaf"
}

@app.route('/health')
def health():
    return 'ok'

@app.route('/')
def home_page():
    return render_template('index.html', 
        areas=set(courses.course_area), 
        contacts=set(courses.course_contact.dropna()),
        icons=icons)

@app.route('/area/<course_area>')
def area_page(course_area):
    return render_template('course_area.html',
        area=course_area,
        courses=courses[courses.course_area == course_area].iterrows(),
        icons=icons)

@app.route('/instructor/<course_instructor>')
def instructor_page(course_instructor):
    return render_template('course_instructor.html',
        instructor=course_instructor,
        courses=courses[courses.course_contact == course_instructor].iterrows(),
        icons=icons)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
