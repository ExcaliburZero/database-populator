#!/usr/bin/python
"""
A script for populating the Scareflix database with data from OpenMovieAPI.
"""

import json
import socket
import sqlite3
import sys
import time
import urllib2

def main():
    """
    Takes in cli arguments and populates the database.
    """
    # Make sure that the database and data files have been given.
    if len(sys.argv) < 3:
        print "Database file and movies files needed."
    else:
        database = sys.argv[1]
        movie_file = sys.argv[2]

        # Parse out the movie names from the movies file
        movie_names = [line.rstrip('\n') for line in open(movie_file)]

        # Populate the database with the movie info
        populate(database, movie_names)

def populate(database, movie_names):
    """
    Populates the given database with the information on the given movies.
    """
    # Get the movie data
    movies_data = get_movies(movie_names)

    # Connect to the database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Get the table entries from the movie data
    movie_entries = []
    acted_in_entries = []
    movie_types_entries = []
    for movie in movies_data:
        try:
            # Make sure movie data is good
            if not movie["imdbRating"].replace(".", "").isdigit() or movie["Actors"] == "N/A" or movie["Genre"] == "N/A" or not movie["Year"].isdigit():
                raise KeyError

            # Gather movies
            movie_id = movie["imdbID"]
            movie_entries = movie_entries + [(
                movie_id, movie["Title"], movie["Director"],
                movie["Year"], movie["imdbRating"]
                )]

            # Gather actors
            actors = [name.strip() for name in movie["Actors"].split(',')]
            for actor in actors:
                acted_in_entries = acted_in_entries + [(
                    actor, movie_id
                    )]

            # Gather genres
            genres = [name.strip() for name in movie["Genre"].split(',')]
            for genre in genres:
                movie_types_entries = movie_types_entries + [(
                    movie_id, genre
                    )]
        except urllib2.HTTPError:
            pass
        except KeyError:
            print "Invalid movie"


    # Put entries into the database
    for entry in movie_entries:
        try:
            cursor.execute("INSERT INTO Movie VALUES (?, ?, ?, ?, ?)", entry)
        except sqlite3.IntegrityError:
            pass
    for entry in acted_in_entries:
        try:
            cursor.execute("INSERT INTO ActedIn VALUES (?, ?)", entry)
        except sqlite3.IntegrityError:
            pass
    for entry in movie_types_entries:
        try:
            cursor.execute("INSERT INTO MovieTypes VALUES (?, ?)", entry)
        except sqlite3.IntegrityError:
            pass

    # Close the database
    conn.commit()
    conn.close()

def get_movies(movie_names):
    """
    Gets the json data for all of the given movies.
    """
    # Construct the api urls to request
    movie_urls = []
    for name in movie_names:
        movie_urls = movie_urls + ["http://www.omdbapi.com/?t=" + name + "&y=&plot=short&r=json"]

    # Get the movie data from the api urls
    movies_data = []
    counter = 0
    total = len(movie_urls)
    for url in movie_urls:
        #print url
        try:
            movie_string = urllib2.urlopen(url).read()

            # Check that the movie was found
            if len(movie_string) > 50:
                try:
                    movies_data = movies_data + [json.loads(movie_string)]
                    counter = counter + 1
                    print str(counter) + " / " + str(total)
                except ValueError:
                    print "Err:"
                    print len(movie_string)
                    print movie_string
            else:
                print url

            time.sleep(0.5)

        except socket.error:
            print "Connection reset"


    return movies_data

# Run the main method of the program
if __name__ == '__main__':
    main()
