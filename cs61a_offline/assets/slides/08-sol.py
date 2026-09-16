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
    total = 0
    for (title, genre), cast in movies.items():
        if genre == target_genre and target_actor in cast:
            total += 1
    return total


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
    def select(attribute):
        if attribute == "x":
            return x
        elif attribute == "y":
            return y
    return select

def get_x(coord):
    return coord("x")

def get_y(coord):
    return coord("y")

def distance(a, b):
    ax, ay = get_x(a), get_y(a)
    bx, by = get_x(b), get_y(b)
    return sqrt((ax - bx) ** 2 + (ay - by) ** 2)
