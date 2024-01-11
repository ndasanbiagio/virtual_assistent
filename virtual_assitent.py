import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# listen to our microphone and return the audio as text
def transform_audio_in_text():
    # store and recognize in a variable
    r = sr.Recognizer()

    # configure the microphone
    with sr.Microphone() as source:
        # wait time
        r.pause_threshold = 0.8

        # inform that recording has started
        print("You can speak now")

        # save what you hear as audio
        audio = r.listen(source)

        try:
            # search in Google
            order = r.recognize_google_cloud(audio, language="en-US")

            # proof that you were able to understand
            print("You said: " + order)

            # return the order
            return order

        # in case the audio is not understood
        except sr.UnknownValueError:
            # proof that the audio was not understood
            print("Oops, I didn't understand")

            # return error
            return "I'm still waiting"

        # in case of not being able to process the order
        except sr.RequestError:
            # proof that there was an error in processing the audio
            print("Oops, there was an error processing the audio")

            # return error
            return "I'm still waiting"

        # unexpected error
        except Exception as e:
            # proof that an unexpected error occurred
            print("Oops, something went wrong:", str(e))

            # return error
            return "I'm still waiting"


# function so that the assistant can be heard
def speak(message):
    # turn on pyttsx3 engine
    engine = pyttsx3.init()

    # pronounce the message
    engine.say(message)
    engine.runAndWait()


speak("Hello World")

# inform the day of the week
def ask_day():
    current_day = datetime.date.today()
    print(current_day)

    # calender
    day_week = current_day.weekday()
    print(day_week)

    # set of days
    calender = {0: 'Monday',
                1: 'Tuesday',
                2: 'Wednesday',
                3: 'Thursday',
                4: 'Friday',
                5: 'Saturday',
                6: 'Sunday'}

    # speak of the day of the week
    speak(f'Today is: {calender[day_week]}')


# report the time
def report_time():
    # create a timestamp
    current_time = datetime.datetime.now()
    current_time_str = f'At this moment, it is {current_time.hour} hours, {current_time.minute} minutes, and {current_time.second} seconds'
    print(current_time_str)

    speak(current_time_str)


# initial greeting
def initial_greeting():
    # initial speak
    current_hour = datetime.datetime.now().hour

    if current_hour < 6 or current_hour > 20:
        moment = 'Good Morning'
    elif 6 <= current_hour < 12:
        moment = 'Good Day'
    else:
        moment = 'Good Night'

    # speak initial greeting
    speak(f'Hello, {moment}. How can I help you?')


# function main
def ask_information():
    # activate initial greeting
    initial_greeting()

    start = True

    while start:
        order = transform_audio_in_text().lower()

        if 'open youtube' in order:
            speak('Starting YouTube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'open browser' in order:
            speak('Of course')
        elif 'what day is today' in order:
            ask_day()
            continue
        elif 'what time is it' in order:
            report_time()
            continue
        elif 'search in wikipedia' in order:
            speak('Searching in Wikipedia')
            order = order.replace('wikipedia', '')
            wikipedia.set_lang('en')
            result = wikipedia.summary(order, sentences=1)
            speak('Wikipedia says:')
            speak(result)
            continue
        elif 'search in internet' in order:
            speak('Searching...')
            speak('Searching on the internet')
            pywhatkit.search(order)
            speak('This is the result')
            continue
        elif 'reproduce' in order:
            speak('Good idea, starting')
            pywhatkit.playonyt(order)
            continue
        elif 'joke' in order:
            speak(pyjokes.get_joke('en'))
            continue
        elif 'price of actions' in order:
            actions = order.split('of')[-1].strip()
            wallet = {'apple': 'AAPL',
                      'amazon': 'AMZN',
                      'google': 'GOOGL'}
            try:
                action_search = wallet[actions]
                action_search = yf.Ticker(action_search)
                price_today = action_search.info['regularMarketPrice']
                speak(f'The price of {actions} is {price_today}')
                continue
            except:
                speak("Sorry, but I didn't find it ")
                continue
        elif 'bye' in order:
            speak("Goodbye! See you later...")
            break

ask_information()
