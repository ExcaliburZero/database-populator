#!/usr/bin/python
"""
A script for populating the Scareflix database with data from OpenMovieAPI.
"""

import json
import sys
import urllib2

def main():
    """
    Takes in cli arguments and populates the database.
    """
    if len(sys.argv) < 3:
        print "Database file and movies files needed."
    else:
        database = sys.argv[1]
        movie_file = sys.argv[2]
        movie_names = [line.rstrip('\n') for line in open(movie_file)]
        populate(database, movie_names)

def populate(database, movie_names):
    """
    Populates the given database with the information on the given movies.
    """
    movies_data = get_movies(movie_names)
    print database
    print movies_data

def get_movies(movie_names):
    """
    Gets the json data for all of the given movies.
    """
    movie_urls = []
    for name in movie_names:
        movie_urls = movie_urls + ["http://www.omdbapi.com/?t=" + name + "&y=&plot=short&r=json"]
    movies_data = []
    for url in movie_urls:
        movie_string = urllib2.urlopen(url)
        movies_data = movies_data + [json.load(movie_string)]
    return movies_data

# Run the main method of the program
if __name__ == '__main__':
    main()
