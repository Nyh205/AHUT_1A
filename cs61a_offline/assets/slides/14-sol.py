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
        >>> rebecca.followers
        0
        >>> taylor = Artist('Taylor Swift')
        >>> rebecca.follow(taylor)
        >>> len(rebecca.following)
        1
        >>> rebecca.following[0] is taylor
        True
        >>> taylor.followers
        1
        >>> str(rebecca)
        'Rebecca'
        >>> str(taylor)
        'Taylor Swift'
        """
        self.name = name
        self.following = []
        self.followers = 0

        # NOTE: be careful, order matters!
        self.playlists = []
        self.liked_songs = Playlist('Liked Songs', [], self)

    def follow(self, user):
        self.following.append(user)
        user.followers += 1

    def __str__(self):
        return self.name


class Artist(User):
    def __init__(self, name: str):
        """
        >>> taylor = Artist('Taylor Swift')
        >>> taylor.name
        'Taylor Swift'
        >>> taylor.albums
        []
        >>> taylor.following
        []
        >>> taylor.followers
        0
        >>> len(taylor.playlists)
        1
        >>> taylor.liked_songs is taylor.playlists[0]
        True
        """
        super().__init__(name)
        self.albums = []


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
        >>> str(all_too_well)
        'All Too Well by Taylor Swift (5:27)'
        >>> all_too_well.play()
        All Too Well by Taylor Swift (5:27)
        """
        self.name = name
        self.artist = artist
        self.duration_sec = duration_sec

    def __str__(self):
        minutes = self.duration_sec // 60
        seconds = self.duration_sec % 60
        return f'{self.name} by {self.artist} ({minutes}:{seconds})'

    def play(self):
        print(self)


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
        self.name = name
        self.songs = songs
        self.owner = owner
        self.total_duration_sec = sum([song.duration_sec for song in self.songs])
        self.owner.playlists.append(self)

    def play(self):
        for song in self.songs:
            song.play()


class Album(Playlist):
    def __init__(self, name: str, songs: list[Song], artist: Artist):
        """
        >>> taylor = Artist('Taylor Swift')
        >>> all_too_well = Song('All Too Well', taylor, 327)
        >>> trouble = Song('I Knew You Were Trouble', taylor, 217)
        >>> red = Album('Red', [all_too_well, trouble], taylor)
        >>> red.name
        'Red'
        >>> red.owner.name
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
        super().__init__(name, songs, artist)
        self.owner.albums.append(self)
