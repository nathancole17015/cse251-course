"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class request_thread(threading.Thread):
  
  def __init__(self,url):
    threading.Thread.__init__(self)
    self.url = url
    self.response = {}

  def run(self):
    response  = requests.get(self.url)
    if response.status_code == 200:
       self.response = response.json()
    else:
       print("Response = ", response.status_code)   



# TODO Add any functions you need here

def retrieve_top_urls():
    top_response = requests.get(TOP_API_URL)
    if top_response.status_code == 200:
        return top_response.json()


# Function to retrieve details of film 6
def retrieve_film_details(film_url):
    film_response = requests.get(film_url)
    if film_response.status_code == 200:
        return film_response.json()
    else:
        print("Failed to retrieve film details")
        return None
    
def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # Retrieve Top API urls
    top_urls = retrieve_top_urls()
    if top_urls:
        # Extract film URL
        film_url = top_urls.get("films")
        # Retrieve film details
        film_thread = request_thread(film_url + "6/")
        film_thread.start()
        film_thread.join()
        film_details = film_thread.response
        if film_details:
            # Display film details
            print("Film 6 Details:")
            print("Title:", film_details.get("title"))
            print("Director:", film_details.get("director"))
            print("Producer:", film_details.get("producer"))
            print()
            print("Characters:")
            people_list = film_details.get("characters", [])
            for person_url in people_list:
                person_thread = request_thread(person_url)
                person_thread.start()
                person_thread.join()
                person_details = person_thread.response
                if person_details:
                    print("-", person_details.get("name", "N/A"))
                    
            print()
            print("Planets:")
            planets_list = film_details.get("planets", [])
            for planets_url in planets_list:
                planets_thread = request_thread(planets_url)
                planets_thread.start()
                planets_thread.join()
                planets_details = planets_thread.response
                if planets_details:
                    print("-", planets_details.get("name", "N/A"))
            
            print()

            print("Starships:")
            starships_list = film_details.get("starships", [])
            for starship_url in starships_list:
                starship_thread = request_thread(starship_url)
                starship_thread.start()
                starship_thread.join()
                starship_details = starship_thread.response
                if starship_details:
                    print("-", starship_details.get("name", "N/A"))

            print()

            print("Species:")
            species_list = film_details.get("species", [])
            for species_url in species_list:
                species_thread = request_thread(species_url)
                species_thread.start()
                species_thread.join()
                species_details = species_thread.response
                if species_details:
                    species_list.append( species_details.get("name"))
            print()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')

if __name__ == "__main__":
    main()
