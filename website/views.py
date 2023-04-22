from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup 
from .models import User, Schedule
from . import db
from .lib_scrape import LibraryScraper




views = Blueprint('views', __name__)

@views.route('/run_script', methods=['POST'])
@login_required
def run_script():

    library_ID = request.get_json()['libraryID']
   
    with open('/Users/denizdemirtas/Desktop/CSM_RoomBook/website/slots', 'r') as file:
        dictionary = {}
        for line in file:
            line = line.strip()
            key, value = line.split(': ')
            dictionary[key] = eval(value)

    
    return dictionary[library_ID]

@views.route('/cancel_reservation', methods=['POST']) 
@login_required
def cancel_reservation():

    schedules = Schedule.query.filter_by(user_id=current_user.id).all()

    for schedule in schedules:
        db.session.delete(schedule)

    # commit the changes to the database
    db.session.commit()

    print("DEBUG: cancel called")
    return jsonify({'message': 'Reservation deleted successfully.'}), 200



@views.route('/save_reservation', methods=['POST'])
@login_required
def save_reservation():


    schedule = request.get_json()
    
    library_ID = schedule['libraryID']
    reservation = schedule['reservation']

    new_reservation = Schedule(libraryID=library_ID, reservation=reservation, user_id=current_user.id)
    db.session.add(new_reservation)

    db.session.commit()

    scraper = LibraryScraper()
    scraper.make_reservation(reservation=reservation, library_ID=library_ID, username=current_user.username, password=current_user.password)

    

    return jsonify({'message': 'Reservation saved successfully.'}), 200
    

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    library_name_dictionary = {'s-lc-8862' : "Earth Sciences & Map Library", "s-lc-8863" : "Engineering Library", "s-lc-8864" : "East Asian Library", "s-lc-885" : "Environmental Design Library", "s-lc-8866" : "Institute of Governmental Studies (Moses Hall 111)", "s-lc-8867" : "Gardner Main Stacks Spaces", "s-lc-8868" : "Moffitt Library"}
    schedules = Schedule.query.filter_by(user_id=current_user.id).all()

    for schedule in schedules:

        schedule.libraryID = library_name_dictionary[schedule.libraryID]


    return render_template("new_homebase.html", user=current_user, schedules=schedules)
