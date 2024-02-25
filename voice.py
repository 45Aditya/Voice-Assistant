import random
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import pyjokes
from datetime import datetime, date, time
from bs4 import BeautifulSoup
import requests
import urllib.request

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

errors = ["Sorry, I didn't catch that. Pleaase try again.",
          "Kindly speak clearly",
          "I didn't understand , can you speak it again"]

greet = {
    'hello' : 'Hello sir, how can I assist you ?' ,
    'hi lotus' : 'Hey There! What can I do for you' ,
    'Hey there!' : 'Listening...'
}

def speak(text):
    engine.say(text)
    engine.runAndWait()


def wish_me():
    # Get the current date and time
    current = datetime.now()  #instance of the 'datetime' module
    time = int(current.hour)

    if time >= 0 and time < 12:
        speak("Good Morning Sir")
        print("\nLotus: Good Morning Sir!")

    elif time >= 12 and time < 16:
        speak("Good Afternoon Sir")
        print("\nLotus: Good Afternoon Sir!")

    else:
        speak("Good Evening Sir")
        print("\nLotus: Good Evening Sir!")

    speak("I'm Lotus. Ready to take your command")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"\nYou said: {query}\n")

    except:
        speak(random.choice(errors))
        return "None"

    return query


def quit(command):
    if command.upper() == 'I' :
        speak("Listening")

    elif command.upper() == 'Q' :
        print("\nLotus : Goodbye sir. See you soon. Have a Nice Day\n")
        speak("Goodbye sir. See you soon. Have a Nice Day")
        exit()

    else:
        print("\nLotus : Kindly look at your keyboard and then type a valid option")
        speak("Kindly look at your keyboard and then type a valid option")
        promt = input("\nPress 'I' to interact or 'Q' to quit : ")
        quit(promt)



def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    para = {
        'q' : city,
        'appid' : api_key,
        'units' : 'metric'
    }

    response = requests.get(base_url, params=para)

    if response.status_code == 200:
        weather_data = response.json()
        main_info = weather_data['main']
        temperature = main_info['temp']
        humidity = main_info['humidity']
        description = weather_data['weather'][0]['description']

        speak("Displaying weather details!")
        print(f"Weather in {city}:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Description: {description}")
    else:
        print("Lotus: Sorry, Unable to fetch the data for this location right now")
        speak("Sorry, Unable to fetch the data for this location right now")


def get_top_headlines():
    print("Lotus: Here are some top headlines of the day I found on the web.")
    speak("Here are some top headlines of the day I found on the web.")

    url = 'https://timesofindia.indiatimes.com/'
    try:
        res = requests.get(url)
        res.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        speak(f"Sorry, there was an error fetching the headlines. {e}")
        return

    soup = BeautifulSoup(res.text, 'html.parser')
    news_box = soup.find('div', {'class': 'view-content'})

    if not news_box:
        speak("I couldn't find any headlines at the moment.")
        return

    all_news = news_box.find_all('a')

    for news in all_news:
        headline = news.text.strip()
        if headline:
            print(headline)
            speak(headline)


if __name__ == "__main__":
    wish_me()

    while True:

        query = take_command().lower()
        for greets in greet.keys():
            if query == greets:
                print("Lotus : " + greet[greets])
                speak(greet[greets])

                interact = input("\nPress 'I' to interact or 'Q' to quit : ")
                quit(interact)

        if 'tell a joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

            interact = input("\nPress 'I' to interact or 'Q' to quit : ")
            quit(interact)

        elif 'open youtube' in query:
            print("Lotus : Command Confirmed !")
            speak("command confirmed !")
            webbrowser.open("https://www.youtube.com/")

            interact = input("\nPress 'I' to interact or 'Q' to quit : ")
            quit(interact)

        elif 'open google' in query:
            print("Lotus : Command Confirmed !")
            speak("command confirmed !")
            webbrowser.open("https://www.google.com")

            interact = input("\nPress 'I' to interact or 'Q' to quit : ")
            quit(interact)


        elif "search for" in query:
            query = query.replace('search for', "")
            print("Lotus : Directing to google...")
            speak('Directing to Google...')
            webbrowser.open(f'https://www.google.com/search?&q={query}')

            interact = input("\nPress 'I' to interact or 'Q' to quit : ")
            quit(interact)

        elif "where is " in query:  # For Maps and Locations
            query = query.replace('where is', "")
            print(f"Lotus : Hold on . I will show you where is {query}.")
            speak(f'Hold on . I will show you where is  {query}.')
            webbrowser.open(f'https://www.google.nl/maps/place/{query}/')
            # Interaction Through Keyboard
            interact = input("\nPress 'I' to interact or 'Q' to quit : ")
            quit(interact)

        elif 'show me the weather in ' in query:
            query = query.replace("show me the weather in" , "")
            api_key = "1cee14f881975ecfe6f3c0e1c3ead421"
            city = query
            print(f"Lotus : Hold on . I will show you the weather in {query}.")
            speak(f'Hold on . I will show you the weather in  {query}.')
            get_weather(api_key, city)

            interact = input("\nPress 'I' to interact or 'Q' to quit : ")
            quit(interact)
