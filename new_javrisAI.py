import speech_recognition as sr
import win32com.client
import webbrowser
import google.generativeai as genai
import os
# import openai  
# import time

def say(text):
    speaker.speak(text)


# def chat_with_ai(prompt):
#     openai.api_key = "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"  # Replace with your OpenAI API key
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response["choices"][0]["message"]["content"]


# def chat_with_ai(prompt):
#     openai.api_key = "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"  
#     time.sleep(1) 
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "system", "content": "You are a helpful AI assistant."},
#                   {"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message["content"]


# Configure Google Gemini API
genai.configure(api_key="my_gemini_API_key") 
model = genai.GenerativeModel("gemini-1.5-pro")


def chat_with_ai(prompt):
    try:
        short_prompt = f"Answer in a short and concise way: {prompt}"  # Force short response
        response = model.generate_content(short_prompt)  # Gemini AI response
        return response.text
    except Exception as e:
        print("Error while communicating with Gemini API:", str(e))
        return "I am unable to respond at the moment."




def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        print("listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.6
        audio = r.listen(source)

        try:
            print("recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
            # say(query)
        except sr.UnknownValueError:
            say("Sorry, I did not understand that.")
            print("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return "None"
        except Exception as e:
            print("Error occurred!!")
        return query.lower()

if __name__ == '__main__':
    speaker = win32com.client.Dispatch("SAPI.SpVoice")  # Initialize speech engine
    print("Welcome to JARVIS AI.")
    speaker.speak("Hello, I am Jarvis AI")

    sites = [["youtube", "http://youtube.com"], ["wikipedia", "http://wikipedia.com"], 
             ["google", "http://google.com"], ["instagram", "http://instagram.com"]]

    while True:
        text = takeCommand()

        for site in sites:
            if f"open {site[0]}" in text:
                print(f"Opening {site[0]} sir...")
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if text == "None":
            print("Thanks for using. Bye!")
            say("Thanks for using")
            break
        
        # if "talk to me" in text:
        #     say("Great idea, let's talk!")
        #     while True:
        #         text = takeCommand()
        #         if "stop jarvis" in text:
        #             say("Okay, nice to talk to you. Bye!")
        #             break
        #         else:
        #             response = chat_with_ai(text)  # AI-generated response
        #             say(response)

        # AI conversation mode
        if "talk to me" in text:
            say("Great idea, let's talk!")
            while True:
                text = takeCommand()
                if "stop jarvis" in text:
                    say("Okay, nice to talk to you. Bye!")
                    break
                else:
                    response = chat_with_ai(text)  # AI-generated response
                    print("JARVIS:", response)
                    say(response)
