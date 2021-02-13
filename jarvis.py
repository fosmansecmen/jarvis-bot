import pyttsx3 # pip install pyttsx3
import datetime
import speech_recognition as sr # pip install pyttsx3, pyaudio, portaudio
import wikipedia # pip install wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes # pip install pyjokes
import os
import pyautogui # pip install pyautogui
import random
import json
import requests
from urllib.request import urlopen
import wolframalpha
import time


news_api_key = 'news api key comes here'
wolframalpha_api_key = 'wolframalpha api key comes here'
engine = pyttsx3.init()


def speak(audio):
	engine.say(audio)
	engine.runAndWait()


def time_():
	time = datetime.datetime.now().strftime("%H %M %S") # for 24-h clock
	speak('The current time is:')
	speak(time)


def date_():
	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	day = datetime.datetime.now().day
	speak('The current day is:{} {} {}'.format(year, month, day))


def wishme():
	speak('Welcome back')
	time_()
	date_()

	# greetings
	hour = datetime.datetime.now().hour

	if hour>=6 and hour<=12:
		speak('Good morning')
	elif hour>12 and hour<18:
		speak('Good afternoon')
	elif hour>=18 and hour<24:
		speak('Good evening')
	else:
		speak('Good night')

	speak('Jarvis is at your service. Please tell me how can I help you today?')


def take_command():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print('Listening...')
		r.pause_threshold = 1
		audio = r.listen(source)

	try:
		print('Recognizing...')
		query = r.recognize_google(audio, language='en-US')
		print(query)

	except Exception as e:
		print(e)
		print('Say that again please...')
		return 'None'

	return query

def send_email(receiver, content):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	# for this function, you must enable low security in your gmail which you will use as sender

	sender = 'sender@sender.com'
	password = 'password'
	server.login(sender, password)
	server.sendmail(sender, receiver, content)
	server.close()


def cpu():
	usage = str(psutil.cpu_percent())
	speak('CPU is at ' + usage)

	battery = psutil.sensors_battery()
	speak('Battery is at ' + battery.percent)


def joke():
	speak(pyjokes.get_joke())


def screenshot():
	img = pyautogui.screenshot()
	img.save('/Users/fosman/Desktop/py playground/jarvis AI/ss.png')


def introduction():
    speak("I am JARVIS 1.0 , Personal AI assistant , "
    "I can help you in various regards , "
    "I can search for you on the Internet , "
    "I can also grab definitions for you from wikipedia , "
    "Where you just have to command me , and I will do it for you , ")


def creator():
    speak("There is no Master but the Master")


if __name__ == '__main__':
	wishme()
	while True:
		query = take_command().lower()

		if 'time' in query:
			time_()
		
		elif 'date' in query:
			date_()

		elif 'wikipedia' in query:
			speak('Searching on wikipedia...')
			query = query.replace('wikipedia', '')
			result = wikipedia.summary(query, sentences=1)
			speak('According to wikipedia')
			print(result)
			speak(result)

		elif 'quit' in query:
			speak('see you later')
			quit()

		elif 'send email' in query:
			try:
				speak('What should I send?')
				content = take_command()
				speak('who is the receiver?')
				receiver = input("type receiver's email: ")
				send_email(receiver, content)
				# speak(content)
				speak('Email has been sent.')
			except Exception as e:
				print(e)
				speak('Unable to send email')

		elif 'search chrome' in query:
			speak('what should I search?')
			chromepath = "open -a /Applications/Google\ Chrome.app %s"
			search = take_command().lower()
			wb.get(chromepath).open(search+'.com')

		elif 'search youtube' in query:
			speak('what should I search?')
			search_term = take_command().lower()
			speak('lets go to youtube')
			wb.get(chromepath).open('www.youtube.com/results?search_query='+search_term)

		elif 'search google' in query:
			speak('what should I search?')
			search_term = take_command().lower()
			wb.get(chromepath).open('https://www.google.com/search?q='+Search_term)


		elif 'cpu' in query:
			cpu()

		elif 'joke' in query:
			joke()

		elif 'word' in query:
			speak('Opening MS word')
			ms_word = r'Microsoft Word path'
			os.startfile(ms_word)

		elif 'write a note' in query:
			speak('what should I write, sir?')
			notes = take_command()
			file = open('notes.txt', 'w')
			speak('sir should I include date and time?')
			ans = take_command()
			if 'yes' in ans or 'sure' in ans:
				strTime = datetime.datetime.now().strftime("%H:%M:%S")
				file.write(strTime)
				file.write(":-")
				file.write(notes)
				speak('Done taking notes, SIRI')
			else:
				file.write(notes)
			file.close()

		elif 'show notes' in query:
			speak('showing note')
			file = open('notes.txt', 'r')
			content = file.read()
			print(content)
			speak(content)
			file.close()

		elif 'take screenshot' in query:
			speak('taking screenshot')
			screenshot()

		elif 'play music' in query:
			songs_dir = '/Users/fosman/Downloads/some mp3/'
			music = os.listdir(songs_dir)
			speak('what should I play')
			ans = take_command().lower()
			if 'number' in ans:
				no = int(ans.replace('number', ''))
			
			if 'random' or 'you choose' in ans:
				no = random.randint(1,50)

			music_file = os.path.join(songs_dir, music[no])
			print(music_file)
			os.system('open %s' % music_file)

		elif 'remember that' in query:
			speak('What should I remember?')
			memory = take_command().lower()
			speak('You asked me to remember that ' + memory)
			remember = open('memory.txt', 'w')
			remember.write(memory)
			remember.close()

		elif 'do you remember anything' in query:
			remember = open('memory.txt', 'r')
			speak('Yeah I do remember ' + remember.read())

		elif 'news' in query:
			try:
				# TODO: make it generic news with keywords
				json_object = urlopen('http://newsapi.org/v2/everything?q=tesla&from=2021-01-11&sortBy=publishedAt&apiKey=fd8a7dfc822c47c4a73c656b745e0eca')
				data = json.load(json_object)
				print(data)
				i = 1

				speak('Here are some headlines from tesla news')
				print('====HEADLINES====' + '\n')
				for item in data['articles']:
					print(str(i) + '. ' + item['title'] + '\n')
					print(item['description'] + '\n')
					speak(item['title'])
					i += 1

			except Exception as e:
				print(str(e))

		elif 'where is' in query:
			query = query.replace('where is', '')
			location = query
			speak('You asked to locate ' + location)
			wb.open_new_tab("www.google.com/maps/place/"+location)

		elif 'calculate' in query:
			client = wolframalpha.Client(wolframalpha_api_key)
			index = query.lower().split().index('calculate')
			query = query.split()[index+1:]
			res = client.query(''.join(query))
			answer = next(res.results).text
			print('the answer is '+answer)
			speak('the answer is '+answer)

		elif 'what is' in query or 'who is' in query:
			client = wolframalpha.Client(wolframalpha_api_key)
			res = client.query(query)

			try:
				print(next(res.results).text)
				speak(next(res.results).text)

			except StopIteration:
				print('No results')

		elif 'tell me about yourself' and 'who are you' in query:
            introduction()
        elif 'tell me about mac' and 'creator' in query:
            creator()

		elif 'log out' in query:
			os.system('shutdown -l')

		elif 'restart' in query:
			os.system('shutdown /r /t 1')

		elif 'shutdown' in query:
			os.system('shutdown /s /t 1')


			








