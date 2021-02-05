import speech_recognition as sr
import time
import playsound # to play saved mp3 file
from gtts import gTTS # google text to speech
import os
from src.draw_on_canvas import draw_star
from src.job_scraper import create_job_list_from_naukri
from src.read_articles import read_article
from src.read_news import read_news
from src.sudoku_player import play_sudoku
from src.youtube_scraper import open_video_from_youtube

'''
This method will be accepting user input via microphone and
will recognize the same using speech_recognize package methods
and return the recognized string.
Note: This will raise an exception if recognize_google method with 
english language encoding is not able to recognize the user input.
'''
def talk():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')

    except Exception as e:
        print("Couldn't recognize what you said, speak once more.")
        return None
    return query

'''
This method will provide the response back to user based on the parameter 
output (response text). Google text to speech library is used here. The text 
to be responded will be converted to a temp .mp3 file and using the playsound 
library we are playing back the response. After the response is played back the
temp file will be deleted from the system.
'''
def respond(output):
    num = 0
    print(output)
    num += 1
    response = gTTS(text=output, lang='en')
    file = str(num) + ".mp3"
    response.save(file)

    playsound.playsound(file, True)
    os.remove(file)


if __name__ == '__main__':
    respond("Hi Dimpy, I am your personal assistant.")

    while (1):
        respond("How can I help you?")
        text = talk().lower()
        time.sleep(4)

        if text == 0:
            continue

        if "stop" in str(text) or "exit" in str(text) or "bye" in str(text):
            respond("Ok bye and take care")
            break

        elif 'sudoku' in text:
            play_sudoku()
            respond('Hope you liked the Game.')
            break
        elif 'news' in text:
            news_list = read_news()
            respond('Here is the local top news headlines for you.')
            count = 0
            for news in news_list:
                if count == 5:
                    break
                else:
                    respond(news)
                    count += 1
                time.sleep(1)
            respond('Thats all the news update for today.')
        elif 'video' in text:
            open_video_from_youtube()
            respond('Hope you liked the video.')
            break

        elif 'job' in text:
            create_job_list_from_naukri()
            respond('Jobs information csv file created in your local drive. Please check.')
            break
        elif 'draw' in text or 'canvas' in text:
            draw_star()
            respond('Hope you enjoyed drawing in the HTML canvas.')
            break;
        elif 'clean' in text or 'article' in text:
            link = read_article()
            respond('Hope you liked the reading experience')
            break
        else:
            respond("Application not available")