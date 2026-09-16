from math import sqrt

def film_appearances(movies: dict[tuple[str], list[str]], target_actor: str, target_genre: str) -> int:
    """
    Given a dictionary mapping a tuple of the movie's title and genre
    to a list of the actors in that movie, the name of a target actor,
    and a target genre, return the number of times the target actor appears
    in movies of the target genre.

    >>> movies = {
    ...     ('Star Wars: Episode IV - A New Hope', 'Sci-Fi'): [
    ...         'Mark Hamill',
    ...         'Harrison Ford',
    ...         'Carrie Fisher',
    ...     ],
    ...     ('Blade Runner 2049', 'Sci-Fi'): [
    ...         'Harrison Ford',
    ...         'Ryan Gosling',
    ...         'Ana de Armas',
    ...     ],
    ...     ('No Time to Die', 'Action'): [
    ...         'Daniel Craig',
    ...         'Ana de Armas',
    ...     ],
    ... }
    >>> film_appearances(movies, 'Harrison Ford', 'Sci-Fi')
    2
    >>> film_appearances(movies, 'Ana de Armas', 'Action')
    1
    >>> film_appearances(movies, 'Harrison Ford', 'Romance')
    0
    >>> film_appearances(movies, 'Saoirse Ronan', 'Action')
    0
    """
    "YOUR CODE HERE"


def coordinate(x, y):
    """
    >>> coord1 = coordinate(1, 2)
    >>> coord2 = coordinate(4, 6)
    >>> get_x(coord1)
    1
    >>> get_x(coord2)
    4
    >>> get_y(coord1)
    2
    >>> get_y(coord2)
    6
    >>> distance(coord1, coord2)
    5.0
    """
    "YOUR CODE HERE"

def get_x(coord):
    "YOUR CODE HERE"

def get_y(coord):
    "YOUR CODE HERE"

def distance(a, b):
    "YOUR CODE HERE"
