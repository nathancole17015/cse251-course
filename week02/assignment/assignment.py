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
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0

# Threaded class definition
class RequestThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        global call_count
        response = requests.get(self.url)
        call_count += 1
        if response.status_code == 200:
            self.response = response.json()
        else:
            print("Response = ", response.status_code)

# Retrieve top URLs
def retrieve_top_urls():
    top_response = requests.get(TOP_API_URL)
    if top_response.status_code == 200:
        return top_response.json()

# Retrieve details of film
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

    top_urls = retrieve_top_urls()
    if top_urls:
        film_url = top_urls.get("films")
        film_thread = RequestThread(film_url + "6/")
        film_thread.start()
        film_thread.join()
        film_details = film_thread.response
        if film_details:
            print()
            print("Film 6 Details:")
            print("Title:", film_details.get("title"))
            print("Director:", film_details.get("director"))
            print("Producer:", film_details.get("producer"))
            print()

            people_list = film_details.get("characters", [])
            print()
            print("Number of Characters:", len(people_list))
            print("Characters:")
            threads = []
            for person_url in people_list:
                person_thread = RequestThread(person_url)
                threads.append(person_thread)
                person_thread.start()
            for thread in threads:
                thread.join()
                person_details = thread.response
                if person_details:
                    print(person_details.get("name"), end=', ')
            print()

            planets_list = film_details.get("planets", [])
            print()
            print("Number of Planets:", len(planets_list))
            print("Planets:")
            threads = []
            for planets_url in planets_list:
                planets_thread = RequestThread(planets_url)
                threads.append(planets_thread)
                planets_thread.start()
            for thread in threads:
                thread.join()
                planets_details = thread.response
                if planets_details:
                    print(planets_details.get("name"), end=', ')
            print()

            starships_list = film_details.get("starships", [])
            print()
            print("Number of Starships:", len(starships_list))
            print("Starships:")
            threads = []
            for starship_url in starships_list:
                starship_thread = RequestThread(starship_url)
                threads.append(starship_thread)
                starship_thread.start()
            for thread in threads:
                thread.join()
                starship_details = thread.response
                if starship_details:
                    print(starship_details.get("name"), end=', ')
            print()

            # Retrieve details of species
            species_list = film_details.get("species", [])
            print()
            print("Number of Species:", len(species_list))
            print("Species:")
            threads = []
            for species_url in species_list:
                species_thread = RequestThread(species_url)
                threads.append(species_thread)
                species_thread.start()
            for thread in threads:
                thread.join()
                species_details = thread.response
                if species_details:
                    print(species_details.get("name"), end=', ')
            print()
    print()
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    print()

if __name__ == "__main__":
    main()
