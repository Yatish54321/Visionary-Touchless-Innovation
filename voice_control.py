import pyttsx3
import speech_recognition as sr
import datetime
import pywhatkit as kit
import wikipedia
import webbrowser
import os
import smtplib
import pyjokes
from requests import get
import random

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    """Speak the given audio string."""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Wish the user based on the current time."""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your Assistant Sir. Please tell me how may I help you")

def takeCommand():
    """Listen for a command from the user and return it as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"User said: {command}")
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
        return "none"
    except Exception as e:
        print(f"Error: {e}")
        speak("There was an issue with voice recognition.")
        return "none"

def sendEmail(to, content):
    """Send an email to the specified address with the given content."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry Sir, I am not able to send this email.")

def performWebOperations(query):
    """Handle web-related operations based on the user's command."""
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")

    elif 'open google' in query:
        speak("Sir, what should I search on Google?")
        cm = takeCommand()
        if cm != "none":
            webbrowser.open(f"https://www.google.com/search?q={cm}")

    elif 'open stack overflow' in query:
        webbrowser.open("https://stackoverflow.com/")

    elif 'open facebook' in query:
        webbrowser.open("www.facebook.com")

    elif 'open colab' in query:
        webbrowser.open("https://colab.research.google.com/")

    elif 'open github' in query:
        webbrowser.open("https://github.com/")

    elif "play songs on youtube" in query:
        kit.playonyt("Ordinary Person")

def playMusic():
    """Play a random song from the specified directory."""
    music_dir = 'C:\\Users\\yatis\\Music'
    songs = os.listdir(music_dir)
    if songs:
        os.startfile(os.path.join(music_dir, random.choice(songs)))

def getIPAddress():
    """Fetch and speak the user's IP address."""
    try:
        ip = get('https://api.ipify.org').text
        speak(f"Your IP address is {ip}")
    except Exception as e:
        print(f"Error: {e}")
        speak("Unable to fetch IP address.")

def tellTime():
    """Speak the current time."""
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Sir, the time is {strTime}")

def tellJoke():
    """Fetch and speak a random joke."""
    joke = pyjokes.get_joke()
    speak(joke)

def performBasicTasks(query):
    """Open basic task-related software based on the user's command."""
    if 'open notepad' in query:
        os.system('notepad')
    elif 'open calculator' in query:
        os.system('calc')
    elif 'open command prompt' in query or 'open cmd' in query:
        os.system('start cmd')
    elif 'open wordpad' in query:
        os.system('write')
    elif 'open paint' in query:
        os.system('mspaint')

if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand()

        if query == "none":
            continue

        if 'play music' in query:
            playMusic()
        elif 'time' in query:
            tellTime()
        elif 'joke' in query:
            tellJoke()
        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                if content != "none":
                    to = "example@example.com"
                    sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry Sir, I am not able to send this email")
        elif 'shutdown' in query:
            os.system("shutdown /s /t 5")
        elif 'restart' in query:
            os.system("shutdown /r /t 5")
        elif 'sleep' in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif 'no thanks' in query or 'you can sleep' in query:
            speak("Thanks for using me Sir, have a good day.")
            break
        elif 'open' in query:
            performBasicTasks(query)
        else:
            performWebOperations(query)
