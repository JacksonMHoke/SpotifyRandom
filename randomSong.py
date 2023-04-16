import spotipy
import json
from random import randrange
from spotipy.oauth2 import SpotifyOAuth
import PySimpleGUI as sg

def randomizePlaylist(choice):
    scope = ["user-library-read", "user-modify-playback-state", "playlist-read-private", "playlist-read-collaborative"]
    f = open('id.json')
    ids=json.load(f)[0]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ids['client_id'], client_secret=ids['client_secret'], redirect_uri='http://localhost:3000', scope=scope))

    results = sp.current_user_saved_tracks()
    playlists=sp.current_user_playlists()
    for idx, item in enumerate(playlists['items']):
        if item['name']==choice:
            playlist=item
        
    playlistItems=sp.playlist_items(playlist['id'])
    print(len(playlistItems['items']))

    tracks=playlistItems['items']

    while(playlistItems['next']): #iterate over all playlist pages
        playlistItems=sp.next(playlistItems)
        tracks.extend(playlistItems['items'])
    s=""
    for i in reversed(range(1, len(tracks))):
        rand=randrange(start=0, stop=i, step=1)
        if not tracks[rand]['is_local']:
            sp.add_to_queue(tracks[rand]['track']['id'])
            s=tracks[rand]['track']['name']+'\n'+s
        window['-TOUT-'].update(s)
        window.Refresh()
        tracks[rand], tracks[i] = tracks[i], tracks[rand]
    window['-TOUT-'].update("DONE ADDING PLAYLIST TO QUEUE\n*NOTE THAT ONLY FIRST 81 SONGS OF QUEUE DISPLAY\n"+s)
    window.Refresh()

scope = ["user-library-read", "user-modify-playback-state", "playlist-read-private", "playlist-read-collaborative"]
f = open('id.json')
ids=json.load(f)[0]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ids['client_id'], client_secret=ids['client_secret'], redirect_uri='http://localhost:3000', scope=scope))

results = sp.current_user_saved_tracks()
playlists=sp.current_user_playlists()
playlistsNames=[x['name'] for x in playlists['items']]

# Create the window
file_list_column = [
    [
        sg.Button("Randomize")
    ],
    [
        sg.Listbox(
            values=playlistsNames, enable_events=True, size=(40, 20), key="-PLAYLIST LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Songs Being Added to Queue")],
    [sg.Multiline(size=(40, 20), key="-TOUT-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Playlist Randomizer", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Randomize":
        randomizePlaylist(values['-PLAYLIST LIST-'][0])

window.close()