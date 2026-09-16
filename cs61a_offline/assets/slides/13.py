class Artist:
    def __init__(self, name: str):
        """
        >>> taylor = Artist('Taylor Swift')
        >>> taylor.name
        'Taylor Swift'
        >>> taylor.albums
        []
        >>> taylor.followers
        0
        """
        "YOUR CODE HERE"


class User:
    def __init__(self, name: str):
        """
        >>> rebecca = User('Rebecca')
        >>> rebecca.name
        'Rebecca'
        >>> rebecca.liked_songs is rebecca.playlists[0]
        True
        >>> len(rebecca.playlists)
        1
        >>> rebecca.following
        []
        >>> taylor = Artist('Taylor Swift')
        >>> rebecca.follow(taylor)
        >>> len(rebecca.following)
        1
        >>> rebecca.following[0] is taylor
        True
        >>> taylor.followers
        1
        """
        "YOUR CODE HERE"

        # This code is correct, no need to edit it
        self.playlists = []
        self.liked_songs = Playlist('Liked Songs', [], self)

    def follow(self, artist: Artist):
        "YOUR CODE HERE"


class Song:
    def __init__(self, name: str, artist: Artist, duration_sec: int):
        """
        >>> taylor = Artist('Taylor Swift')
        >>> all_too_well = Song('All Too Well', taylor, 327)
        >>> all_too_well.name
        'All Too Well'
        >>> all_too_well.artist.name
        'Taylor Swift'
        >>> all_too_well.duration_sec
        327
        >>> all_too_well.play()
        All Too Well by Taylor Swift (5:27)
        """
        "YOUR CODE HERE"

    def play(self):
        """Prints the song title, artist name, and duration (M:SS) following the format above"""
        "YOUR CODE HERE"


class Playlist:
    def __init__(self, name: str, songs: list[Song], owner: User):
        """
        >>> rebecca = User('Rebecca')
        >>> taylor = Artist('Taylor Swift')
        >>> ed = Artist('Ed Sheeran')
        >>> all_too_well = Song('All Too Well', taylor, 327)
        >>> trouble = Song('I Knew You Were Trouble', taylor, 217)
        >>> azizam = Song('Azizam', ed, 162)
        >>> love_songs = Playlist('Love Songs', [all_too_well, trouble, azizam], rebecca)
        >>> love_songs.name
        'Love Songs'
        >>> love_songs.owner is rebecca
        True
        >>> love_songs.total_duration_sec
        706
        >>> love_songs.play()
        All Too Well by Taylor Swift (5:27)
        I Knew You Were Trouble by Taylor Swift (3:37)
        Azizam by Ed Sheeran (2:42)
        >>> len(rebecca.playlists)  # liked songs and love songs playlist
        2
        >>> rebecca.playlists[1] is love_songs
        True
        """
        "YOUR CODE HERE"

    def play(self):
        "YOUR CODE HERE"


class Album:
    def __init__(self, name: str, songs: list[Song], artist: Artist):
        """
        >>> taylor = Artist('Taylor Swift')
        >>> all_too_well = Song('All Too Well', taylor, 327)
        >>> trouble = Song('I Knew You Were Trouble', taylor, 217)
        >>> red = Album('Red', [all_too_well, trouble], taylor)
        >>> red.name
        'Red'
        >>> red.artist.name
        'Taylor Swift'
        >>> red.total_duration_sec
        544
        >>> red.play()
        All Too Well by Taylor Swift (5:27)
        I Knew You Were Trouble by Taylor Swift (3:37)
        >>> len(taylor.albums)
        1
        >>> red is taylor.albums[0]
        True
        """
        "YOUR CODE HERE"

    def play(self):
        "YOUR CODE HERE"
