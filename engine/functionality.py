from pipes import quote
import subprocess
import pyautogui as autogui
from groq import Groq
import winsound
import pyautogui
import pywhatkit as pkit
from engine.helper import removeWords, yt_term_extraction
from engine.onCommand import *
from engine.config import ASSISTANT_NAME,USER_NAME,SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECRET,GROQ_API_KEY
import webbrowser
import sqlite3
import os
import eel
import spotipy

#connecting nova db
dataobj = sqlite3.connect("nova.db")
cursor = dataobj.cursor()

#startup sound
@eel.expose
def playSound():
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        sound_path = os.path.join(
            base_dir,
            "static", "assets", "audio", "start_sound.wav"
        )

        winsound.PlaySound(
            sound_path,
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )

    except Exception as e:
        print(f"Startup sound error: {e}")

#handles the opening of softwares or websites
@eel.expose
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open","")
    query.lower()

    app_name = query.strip()

    if app_name !="":
        
        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,)
            )
            results = cursor.fetchall()
            if len(results) !=0:
                Speech("Opening "+query)
                os.startfile(results[0][0])
            elif len(results) == 0:
                cursor.execute(
                    'SELECT path FROM web_command WHERE name IN (?)', (app_name,)
                )
                results = cursor.fetchall()

                if len(results) != 0:
                    Speech("Opening "+query)
                    webbrowser.open(results[0][0])
                else:
                    Speech("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        Speech("not found")
        except:
            Speech("some thing went wrong")

#opening youtube
def OpenYoutube(query):
    search_term = yt_term_extraction(query)
    Speech("Playing "+search_term+" on youtube")
    pkit.playonyt(search_term)

def createYtSearchTerm(query):
    query = query.strip().lower()

    wordsToRemove = [ASSISTANT_NAME, 'search','on','youtube','for']

    query = removeWords(query,wordsToRemove)
    
    return query

def searchYoutube(query):
    result = ""
    query = query.split(" ")
    for i, word in enumerate(query):
        if i < len(query) - 1:
            result += word + '+'
        else:
            result += word
    print(result)
    webbrowser.open(f"https://www.youtube.com/results?search_query={result}")
    Speech(f"Searching for {query}")


#searching the given command for contact name and returning the contact info
def searchContact(query):

    wordsToRemove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']

    query = removeWords(query,wordsToRemove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))

        results = cursor.fetchall()
        print(results[0][0])
        mobileNumberStr = str(results[0][0])
        if not mobileNumberStr.startswith('+91'):
            mobileNumberStr = '+91' + mobileNumberStr
        
        return mobileNumberStr, query
    except:
        Speech('Does not exist in contacts')
        return 0,0


#takes the valid contact info and performs operations like sending a message, calling or video calling
def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        AI_message = "message sent successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        AI_message = "calling "+name

    else:
        target_tab = 6
        message = ''
        AI_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    Speech(AI_message)


#searches song name from command and returns it
def searchSong(query):
    query = query.strip().lower()
    wordstoremove = [ASSISTANT_NAME, 'play', 'on', 'spotify', 'by']
    query = removeWords(query,wordstoremove)
    callSpotify(query)


#opens spotify and plays the given song
def callSpotify(song_name):
    if song_name != "":

        username = 'Your_user_name'
        clientID = SPOTIFY_CLIENT_ID
        clientSecret = SPOTIFY_CLIENT_SECRET
        redirect_uri = 'http://localhost:8000/index.html'
        scope = "user-modify-playback-state"
        oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri, scope) 
        token_dict = oauth_object.get_cached_token() 
        token = token_dict['access_token'] 
        spotifyObject = spotipy.Spotify(auth=token) 
        user_name = spotifyObject.current_user() 

        print(song_name)
        searchResults = spotifyObject.search(song_name, 1, 0, "track")
        songsDict = searchResults['tracks']
        songsItems = songsDict['items']
        song = songsItems[0]['external_urls']['spotify']
        from engine.helper import is_window_open
        if is_window_open("Spotify"):
            print("spotify already open")
            webbrowser.open(song)
            sleep(2)
            autogui.hotkey("ctrl","r")
        else:
            print("spotify opened now")
            webbrowser.open(song)
        
        print("Opening "+ song_name)
        Speech("Playing "+ song_name)
    else:
        print("I am sorry but i could not detect what song you wish to play, please try again")
        Speech("I am sorry but i could not detect what song you wish to play, please try again")


#play/pause any media
def playPause():
    Speech("Understood")
    autogui.press("playpause")

def nextPrev(query):
    if 'next' in query:
        Speech("Playing next track")
        autogui.press("nexttrack")
    else:
        Speech("Playing previous track")
        autogui.press("prevtrack")
        sleep(1)
        autogui.press("prevtrack")
    
#chatbot
def chatBot(query):
    client = Groq(
        api_key=GROQ_API_KEY,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f". You are {USER_NAME}'s virtual assistant, you can use pronouns instead of using {USER_NAME} more frequently. You can also open applications, play/pause songs, and many more things. If user aks what you are or who you are, reply that you are a virtual assistant designed to be able to perform tasks for {USER_NAME} like opening applications, websites, playing music or searching on youtube and many more things, your name is NOVA. If {USER_NAME} asks for any information or question like, what is AI, or who is elon musk make the answer under 100 words, only make it larger if {USER_NAME} aks for a larger explaination"
            },
            {
                "role": "user",
                "content": query,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None
    )
    response = ''
    for chunk in chat_completion:
        response += chunk.choices[0].delta.content or ''
    print(response)
    Speech(response)


#MOST IMPORTANT FUNCTIONS

#FOR CLIPPING
def CLIPPING():
    Speech("Clipping that thang")
    autogui.hotkey("win","prtsc")

#FOR TURNING SHIT UP
def turningShitUp():
    autogui.press("volumeup",presses=80)
