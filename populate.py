#!/usr/bin/python
"""
A script for populating the Scareflix database with data from OpenMovieAPI.
"""

import json
import sqlite3
import sys
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


    # Put entries into the database
    cursor.executemany("INSERT INTO Movie VALUES (?, ?, ?, ?, ?)", movie_entries)
    cursor.executemany("INSERT INTO ActedIn VALUES (?, ?)", acted_in_entries)
    cursor.executemany("INSERT INTO MovieTypes VALUES (?, ?)", movie_types_entries)

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
    for url in movie_urls:
        movie_string = urllib2.urlopen(url)
        movies_data = movies_data + [json.load(movie_string)]

    return movies_data

# Run the main method of the program
if __name__ == '__main__':
    main()
