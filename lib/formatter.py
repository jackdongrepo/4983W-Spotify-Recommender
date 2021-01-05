# Convert json data file into dataframe
class Playlist:
    def __init__(self):
        self.name = 0
        self.collaborative = 0
        self.pid = 0
        self.num_tracks = 0
        self.modified_at = 0
        self.tracks = []
        self.num_albums = 0
        self.num_followers = 0
        self.num_edits = 0
        self.duration_s = 0
        self.num_artists = 0

class Song:
    def __init__(self):
        self.pos = 0
        self.artist_name = 0
        self.track_name = 0
        self.track_uri = 0
        self.artist_uri = 0
        self.album_uri = 0
        self.duration_s = 0
        self.album_name = 0

##############################################################################

def import_to_json(filename):
    plist = open(filename,'r',encoding="utf-8")

    # if line has info for playlist or song
    # if 1 then playlist, 2 then song
    status = 0
    playlist_list = [] # list of playlists
    song_list = [] # list of tracks, each playlist

    playlist = Playlist()
    song = Song()

    for lines in plist:
        line = lines.strip()

        if "{" in line and status == 0: # new playlist info
            status = 1
            playlist = Playlist()
            song_list = []
        elif "[" in line: # start of songs list
            status = 2
        elif "{" in line and status == 2: # new song info
            song = Song()
        elif "]" in line: # end of songs list
            status = 1
        elif "}" in line and status == 2: # end of new song
            song_list.append(vars(song))
        elif "}" in line and status == 1: # end of playlist
            playlist_list.append(vars(playlist))
            status = 0
            playlist.tracks = song_list

        # getting playlist information into class
        if "\"name\":" in line:
            name = line[9:-2]
            playlist.name = name.strip()
        elif "\"pid\":" in line.strip():
            pid = line[7:-1]
            playlist.pid = int(pid.strip())
        elif "\"collaborative\":" in line.strip():
            collaborative = line[18:-2]
            playlist.collaborative = collaborative.strip()
        elif "\"num_tracks\":" in line.strip():
            num_tracks = int(line[14:-1].strip())
            playlist.num_tracks = num_tracks
        elif "\"num_albums\":" in line.strip():
            num_albums = int(line[14:-1])
            playlist.num_albums = num_albums
        elif "\"num_followers\":" in line.strip():
            num_followers = int(float(line[17:-1]))
            playlist.num_followers = num_followers
        elif "\"num_edits\":" in line.strip():
            num_edits = int(line[13:-1])
            playlist.num_edits = num_edits
        elif "\"modified_at\":" in line.strip():
            modified_at = int(line[15:-1])
            playlist.modified_at = modified_at
        elif "\"duration_ms\":" in line.strip() and status == 1:
            duration_s = 0
            try:
                duration_s = round(int(line[15:])/1000,1)
            except:
                duration_s = round(int(line[15:-1])/1000,1)
            finally:
                playlist.duration_s = duration_s
        elif "\"num_artists\":" in line.strip():
            num_artists = 0
            try:
                num_artists = int(line[15:])
            except:
                num_artists = int(line[15:-1])
            finally:
                playlist.num_artists = num_artists

        ## getting song info into class
        if "\"pos\":" in line.strip():
            pos = int(line[7:-1])
            song.pos = pos
            song.pid = int(pid)
        elif "\"artist_name\":" in line.strip():
            artist_name = line[16:-2].strip()
            song.artist_name = artist_name
        elif "\"track_uri\":" in line.strip():
            track_uri = line[14:-2].strip()
            song.track_uri = track_uri
        elif "\"artist_uri\":" in line.strip():
            artist_uri = line[15:-2].strip()
            song.artist_uri = artist_uri
        elif "\"album_uri\":" in line.strip():
            album_uri = line[14:-2].strip()
            song.album_uri = album_uri
        elif "\"track_name\":" in line.strip():
            track_name = line[15:-2].strip()
            song.track_name = track_name
        elif "\"duration_ms\":" in line.strip() and status == 2:
            duration_s = round(int(line[15:-1])/1000,1)
            song.duration_s = duration_s
        elif "\"album_name\":" in line.strip():
            album_name = line[15:-1].strip()
            song.album_name = album_name
    plist.close()
    return playlist_list

def unique_list(l):
    temp_str = ""
    for genres in l:
        temp_str += genres+" "
    temp_str = temp_str.split()
    return(" ".join(sorted(set(temp_str), key=temp_str.index)))
