from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser


    
class MusicPlayer() :
    def __init__(self,SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_URI):
        self.sp = Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_URI,
            scope="user-modify-playback-state user-read-playback-state"
        ))
        webbrowser.open_new('https://open.spotify.com/')

        
    
    def current_timer(self):
        time = self.sp.current_user_playing_track()
        timer = time['progress_ms'] / 1000
        return timer  
        
    def skip(self):

        self.sp.next_track()

    def play(self,title):
        music_title = [title[0]['music'][i]['title'] for i in range(len(title[0]))]
        play_track = [self.sp.search(i,limit=1,type='track')['tracks']['items'][0]['uri'] for i in music_title]    
        recommend_data = self.sp.recommendations(seed_tracks=play_track,limit=10)
        play_tracks = [recommend_data['tracks'][i]['external_urls']['spotify'] for i in range(len(recommend_data['tracks']))]
        for i in play_tracks:
            play_track.append(i)           
        devices = self.sp.devices()
        devices_id = devices['devices'][0]['id']
        

        self.sp.start_playback(device_id=devices_id,uris = play_track,offset={'position':0})
    def replay(self):
        current = self.sp.current_user_playing_track()
        if current != None:
            if current['is_playing'] == False:
                self.sp.start_playback()
    def previous(self):
        try:
            self.sp.previous_track()
        except:
            pass
    def stop(self):
        current = self.sp.current_user_playing_track()
        if current != None:
            if current['is_playing'] == True:
                self.sp.pause_playback()
        else:
            pass

    def volume(self,ctrl):
        volumn = self.sp.devices()['devices'][0]['volume_percent']
        if ctrl == 'up':
            self.sp.volume(volume_percent=volumn+20)
        elif ctrl == 'down':
            self.sp.volume(volume_percent=volumn-20)
        else:
            pass
    