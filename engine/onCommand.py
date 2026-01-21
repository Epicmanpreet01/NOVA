from typing import Optional
import pyttsx3
import speech_recognition as sr
import eel
from time import sleep

#text to speech
def Speech(text):
    from engine.audio_engine.tts import tts_kokoro_blocking

    text = str(text)
    eel.DisplayMessage(text)

    tts_kokoro_blocking(text)

    eel.receiverText(text)
    eel.commandFinished()



#speech to text
@eel.expose
def takeCommand():
    from engine.audio_engine.asr import listen_once_whisper

    eel.DisplayMessage("listening...")

    text = listen_once_whisper()
    if not text:
        return ""

    eel.DisplayMessage(text)
    return text.lower().strip()





#to take allcommands and verify how to handle them
@eel.expose
def allCommands(message: Optional[str] = None):

    query = takeCommand() if message is None else message
    eel.senderText(query)
    print(f"Processing query:{query}")

    try:
        #for opening videos on youtube
        if "on youtube" in query or "search" in query:
            if "search" in query:
                from engine.functionality import createYtSearchTerm,searchYoutube
                search_term = createYtSearchTerm(query)
                searchYoutube(search_term)
            else:
                from engine.functionality import OpenYoutube
                OpenYoutube(query)
        #for whatsapp purposes
        elif "message" in query or "call" in query or "video call" in query:
            from engine.functionality import searchContact,whatsApp
            operation = ""
            contactNo, name = searchContact(query)
            if(contactNo != 0):
                if "message" in query:
                    operation = 'message'
                    Speech("what message to send")
                    query = takeCommand()
                elif "video call" in query:
                    operation = "video call"
                else:
                    operation = "call"
                whatsApp(contactNo,query,operation,name)
        #for spotify
        elif "on spotify" in query:
            from engine.functionality import searchSong
            searchSong(query)
        #opening a website or software
        elif "open" in query:
            from engine.functionality import openCommand
            openCommand(query)
        elif 'play' in query or 'pause' in query:
            if 'next' in query or 'previous' in query:
                from engine.functionality import nextPrev
                nextPrev(query)
            else:
                from engine.functionality import playPause
                playPause()
                
        elif "nova stop" in query:
            eel.commandFinished()
            return
        elif "clip that" in query:
            from engine.functionality import CLIPPING
            CLIPPING()
        elif "turn that shut up" in query:
            from engine.functionality import turningShitUp
            turningShitUp()
        #chatbot
        else:
            from engine.functionality import chatBot
            chatBot(query)
    except Exception as e:
        print(f"Error processing command: {e}")
        return f"Sorry, I encountered an error: {str(e)}"
    finally:
        eel.commandFinished()