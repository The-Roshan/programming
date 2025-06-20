import speech_recognition as sr
import os
import time
import tkinter as tk
from threading import Thread
import subprocess
import pyautogui
import google.generativeai as genai
from datetime import datetime, timedelta
import webbrowser
import getpass
import smtplib
from email.mime.text import MIMEText
from gtts import gTTS
import pygame
import glob
import re
import psutil
import screen_brightness_control as sbc
from googletrans import Translator
import requests
import pyperclip  # For clipboard operations
import wikipedia  # For Wikipedia searches
import pywhatkit  # For YouTube video playback
import json  # For saving settings/notes
import random  # For random selections

class VoiceAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Surya - Ultimate Voice Assistant")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        
        self.is_listening = False
        self.is_active = False
        self.is_responding = False
        self.is_playing_music = False
        self.alarms = []
        self.timers = []
        self.notes_file = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'surya_notes.json')
        
        pygame.mixer.init()
        
        self.history_text = tk.Text(self.root, height=15, width=60, state="disabled")
        self.history_text.pack(pady=10)
        
        self.api_key = "AIzaSyBPgU1268WDf2r0-nFMOxiRI-eWYIMXekQ"  # Replace with your Gemini API key
        genai.configure(api_key=self.api_key)
        
        self.gemini_model = None
        try:
            self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            self.log_message("Successfully initialized Gemini model")
        except Exception as e:
            self.log_message(f"Error initializing Gemini model: {e}")
        
        self.title_label = tk.Label(self.root, text="Surya - Ultimate Assistant", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=10)
        
        self.time_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f0f0f0")
        self.time_label.pack(pady=5)
        self.update_time()
        
        self.status_label = tk.Label(self.root, text="Click 'Start' to begin", font=("Arial", 12), bg="#f0f0f0")
        self.status_label.pack(pady=10)
        
        self.volume_label = tk.Label(self.root, text="Speech Volume", font=("Arial", 10), bg="#f0f0f0")
        self.volume_label.pack(pady=5)
        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, bg="#f0f0f0", length=200)
        self.volume_scale.set(50)
        self.volume_scale.pack(pady=5)
        
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.button_frame, text="Start Listening", command=self.start_listening, bg="#4CAF50", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(self.button_frame, text="Stop Listening", command=self.stop_listening, bg="#f44336", fg="white", state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_respond_button = tk.Button(self.button_frame, text="Stop Respond", command=self.stop_respond, bg="#FF9800", fg="white", state="disabled")
        self.stop_respond_button.pack(side=tk.LEFT, padx=5)
        
        self.screenshot_button = tk.Button(self.button_frame, text="Take Screenshot", command=self.take_screenshot, bg="#2196F3", fg="white")
        self.screenshot_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_log_button = tk.Button(self.button_frame, text="Clear Log", command=self.clear_log, bg="#9C27B0", fg="white")
        self.clear_log_button.pack(side=tk.LEFT, padx=5)
        
        self.app_protocols = {
            "whatsapp": "whatsapp:",
            "youtube": "https://www.youtube.com",
            "settings": "ms-settings:"
        }
        
        self.app_executables = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "browser": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "chrome": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
            "paint": "mspaint.exe",
            "file explorer": "explorer.exe",
            "explorer": "explorer.exe",
            "terminal": "cmd.exe",
            "cmd": "cmd.exe",
            "whatsapp": r"C:\Users\{}\AppData\Local\WhatsApp\WhatsApp.exe".format(os.getlogin()),
            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "settings": r"C:\Windows\System32\control.exe"
        }
        
        self.websites = {
            "google": "https://www.google.com",
            "wikipedia": "https://www.wikipedia.org",
            "reddit": "https://www.reddit.com",
            "twitter": "https://www.twitter.com",
            "facebook": "https://www.facebook.com"
        }
        
        self.alarm_thread = Thread(target=self.check_alarms, daemon=True)
        self.alarm_thread.start()
        self.timer_thread = Thread(target=self.check_timers, daemon=True)
        self.timer_thread.start()
        
        self.translator = Translator()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def log_message(self, message):
        try:
            if hasattr(self, 'history_text') and self.history_text.winfo_exists():
                self.history_text.config(state="normal")
                self.history_text.insert(tk.END, message + "\n")
                self.history_text.see(tk.END)
                self.history_text.config(state="disabled")
            else:
                print(f"Log (GUI unavailable): {message}")
        except tk.TclError:
            print(f"Log (GUI destroyed): {message}")

    def clear_log(self):
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state="disabled")
        self.log_message("Log cleared")

    def speak(self, text):
        if not self.is_responding:
            self.is_responding = True
            self.stop_respond_button.config(state="normal")
            self.log_message(f"Speaking: {text}")
            try:
                tts = gTTS(text=text, lang='en')
                temp_file = "temp_speech.mp3"
                tts.save(temp_file)
                speech_channel = pygame.mixer.Channel(2)
                speech_channel.set_volume(self.volume_scale.get() / 100.0)
                speech_channel.play(pygame.mixer.Sound(temp_file))
                while speech_channel.get_busy():
                    pygame.time.Clock().tick(10)
                os.remove(temp_file)
            except Exception as e:
                self.log_message(f"Speech error: {e}")
            finally:
                self.is_responding = False
                self.stop_respond_button.config(state="disabled")

    def stop_respond(self):
        if self.is_responding:
            self.log_message("Stopping current response")
            pygame.mixer.Channel(2).stop()
            self.is_responding = False
            self.is_active = False
            self.stop_respond_button.config(state="disabled")
            self.status_label.config(text="Waiting for 'Hey Surya'...", fg="blue")
            self.speak("Response stopped, say Hey Surya to continue")

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
        self.time_label.config(text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_time)

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        try:
            with microphone as source:
                self.log_message("Adjusting for ambient noise...")
                self.speak("Adjusting microphone, please wait")
                recognizer.adjust_for_ambient_noise(source, duration=3)
                self.log_message("Microphone ready - Say 'Hey Surya'")
                self.speak("Microphone ready, say Hey Surya")
                
                while self.is_listening:
                    try:
                        self.status_label.config(text="Waiting for 'Hey Surya'...", fg="blue")
                        audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio, language="en-US").lower()
                        self.log_message(f"Heard: {command}")
                        
                        if "hey surya" in command:
                            self.is_active = True
                            self.status_label.config(text="Listening...", fg="green")
                            self.speak("Yes, how can I assist you?")
                            self.process_command(command.replace("hey surya", "").strip())
                            while self.is_active and self.is_listening:
                                try:
                                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                                    follow_up = recognizer.recognize_google(audio, language="en-US").lower()
                                    self.log_message(f"Heard: {follow_up}")
                                    self.process_command(follow_up)
                                except sr.WaitTimeoutError:
                                    self.log_message("No follow-up detected")
                                    self.speak("No response, waiting for Hey Surya")
                                    self.is_active = False
                                    break
                                except sr.UnknownValueError:
                                    self.speak("Could not understand, please try again")
                    except sr.UnknownValueError:
                        self.log_message("Could not understand audio")
                    except sr.RequestError as e:
                        self.log_message(f"Speech recognition error: {e}")
                        self.speak("Internet error, check your connection")
                        break
                    time.sleep(0.2)
        except Exception as e:
            self.log_message(f"Microphone error: {e}")
            self.speak("Microphone not found")
            self.stop_listening()

    def process_command(self, command):
        if not command:
            return
        
        if self.is_responding:
            pygame.mixer.Channel(2).stop()
            self.is_responding = False
        
        # Existing Commands
        if "open" in command:
            app_name = command.split("open", 1)[1].strip()
            self.launch_application(app_name)
        
        elif "shutdown" in command:
            self.log_message("Initiating shutdown")
            self.speak("Shutting down in 30 seconds. Say cancel to stop.")
            subprocess.Popen("shutdown /s /t 30", shell=True)
        
        elif "cancel shutdown" in command or "cancel" in command:
            self.log_message("Cancelling shutdown")
            self.speak("Shutdown cancelled")
            subprocess.Popen("shutdown /a", shell=True)
        
        elif "restart" in command:
            self.log_message("Initiating restart")
            self.speak("Restarting in 30 seconds. Say cancel to stop.")
            subprocess.Popen("shutdown /r /t 30", shell=True)
        
        elif "sleep" in command:
            self.log_message("Putting computer to sleep")
            self.speak("Going to sleep")
            subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
        
        elif "mute" in command:
            self.log_message("Muting volume")
            self.speak("Volume muted")
            pyautogui.press("volumemute")
        
        elif "volume up" in command:
            self.log_message("Increasing volume")
            self.speak("Volume increased")
            pyautogui.press("volumeup", presses=2)
        
        elif "volume down" in command:
            self.log_message("Decreasing volume")
            self.speak("Volume decreased")
            pyautogui.press("volumedown", presses=2)
        
        elif "increase brightness" in command:
            self.adjust_brightness(increase=True)
        
        elif "decrease brightness" in command:
            self.adjust_brightness(increase=False)
        
        elif "create file" in command:
            self.create_text_file()
        
        elif "open file" in command or "open folder" in command:
            self.open_file_or_folder(command)
        
        elif "take a note" in command:
            self.take_note(command)
        
        elif "search" in command:
            query = command.replace("search", "").strip()
            if query:
                self.web_search(query)
            else:
                self.speak("Please specify what to search for")
        
        elif "open website" in command:
            self.open_website(command)
        
        elif "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}")
        
        elif "date" in command:
            current_date = datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}")
        
        elif "weather" in command:
            location = command.replace("weather", "").replace("in", "").strip() or "current location"
            self.get_weather(location)
        
        elif "screenshot" in command:
            self.take_screenshot()
        
        elif "play music" in command:
            self.play_music()
        
        elif "stop music" in command:
            self.stop_music()
        
        elif "set alarm" in command:
            self.set_alarm(command)
        
        elif "set timer" in command:
            self.set_timer(command)
        
        elif "send email" in command:
            self.send_email(command)
        
        elif "read notifications" in command:
            self.read_notifications()
        
        elif "check battery" in command:
            self.check_battery()
        
        elif "tell a joke" in command:
            self.tell_joke()
        
        elif "translate" in command:
            self.translate_text(command)
        
        elif "stop" in command or "exit" in command:
            self.speak("Stopping the assistant")
            self.stop_listening()
        
        # New Commands
        elif "play video" in command or "play on youtube" in command:
            video_query = command.replace("play video", "").replace("play on youtube", "").strip()
            self.play_youtube_video(video_query)
        
        elif "copy text" in command:
            text = command.replace("copy text", "").strip()
            self.copy_to_clipboard(text)
        
        elif "paste text" in command:
            self.paste_from_clipboard()
        
        elif "wikipedia" in command:
            query = command.replace("wikipedia", "").strip()
            self.search_wikipedia(query)
        
        elif "set reminder" in command:
            self.set_reminder(command)
        
        elif "read notes" in command:
            self.read_notes()
        
        elif "delete note" in command:
            note_id = command.replace("delete note", "").strip()
            self.delete_note(note_id)
        
        elif "check cpu" in command:
            self.check_cpu_usage()
        
        elif "check memory" in command:
            self.check_memory_usage()
        
        elif "lock screen" in command:
            self.lock_screen()
        
        elif "open task manager" in command:
            self.open_task_manager()
        
        elif "random number" in command:
            self.generate_random_number(command)
        
        elif "flip a coin" in command:
            self.flip_coin()
        
        elif "roll a dice" in command:
            self.roll_dice()
        
        elif "set volume" in command:
            self.set_system_volume(command)
        
        elif "open camera" in command:
            self.open_camera()
        
        elif "take selfie" in command:
            self.take_selfie()
        
        else:
            response = self.ask_gemini(command)
            self.speak(response)

    def ask_gemini(self, question):
        if not self.gemini_model:
            return "Gemini model not initialized."
        try:
            response = self.gemini_model.generate_content(question)
            return response.text
        except Exception as e:
            self.log_message(f"Gemini API error: {e}")
            return "Sorry, I couldn't process that."

    def launch_application(self, app_name):
        self.log_message(f"Attempting to launch: {app_name}")
        self.speak(f"Opening {app_name}")
        for alias, protocol in self.app_protocols.items():
            if alias in app_name:
                try:
                    if protocol.startswith("http"):
                        os.startfile(protocol)
                    else:
                        subprocess.run(f'start "" "{protocol}"', shell=True)
                    self.status_label.config(text=f"Opened {app_name}", fg="green")
                    return
                except Exception as e:
                    self.log_message(f"Protocol launch failed: {e}")
        for alias, exe_path in self.app_executables.items():
            if alias in app_name:
                try:
                    if os.path.exists(exe_path):
                        subprocess.Popen(f'"{exe_path}"', shell=True)
                        self.status_label.config(text=f"Opened {app_name}", fg="green")
                        return
                    else:
                        subprocess.Popen(alias, shell=True)
                        self.status_label.config(text=f"Opened {app_name}", fg="green")
                        return
                except Exception as e:
                    self.log_message(f"Executable launch failed: {e}")
        self.speak(f"Could not find {app_name}")
        self.status_label.config(text="App not found", fg="red")

    def create_text_file(self):
        try:
            desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            filename = f"new_file_{int(time.time())}.txt"
            filepath = os.path.join(desktop, filename)
            with open(filepath, 'w') as f:
                f.write("Created by Surya Voice Assistant")
            self.speak(f"Created a new text file on your desktop named {filename}")
        except Exception as e:
            self.log_message(f"Error creating file: {e}")
            self.speak("Sorry, I couldn't create the file")

    def open_file_or_folder(self, command):
        target = command.replace("open file", "").replace("open folder", "").strip()
        if not target:
            self.speak("Please specify a file or folder name")
            return
        desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        target_path = os.path.join(desktop, target)
        try:
            if os.path.exists(target_path):
                os.startfile(target_path)
                self.speak(f"Opened {target}")
            else:
                self.speak(f"Could not find {target} on your desktop")
        except Exception as e:
            self.log_message(f"Error opening file/folder: {e}")
            self.speak("Sorry, I couldn't open that")

    def web_search(self, query):
        try:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            self.speak(f"Searching Google for {query}")
        except Exception as e:
            self.log_message(f"Error performing web search: {e}")
            self.speak("Sorry, I couldn't perform the search")

    def open_website(self, command):
        website_name = command.replace("open website", "").strip()
        if website_name in self.websites:
            url = self.websites[website_name]
            webbrowser.open(url)
            self.speak(f"Opening {website_name}")
        else:
            self.speak(f"Sorry, I don't know the website {website_name}. Try google, wikipedia, or reddit.")

    def get_weather(self, location):
        weather_query = f"What is the weather in {location} today?"
        response = self.ask_gemini(weather_query)
        self.speak(response)

    def take_screenshot(self):
        try:
            desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            filename = f"screenshot_{int(time.time())}.png"
            filepath = os.path.join(desktop, filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            self.speak(f"Screenshot saved as {filename}")
        except Exception as e:
            self.log_message(f"Error taking screenshot: {e}")
            self.speak("Sorry, I couldn't take a screenshot")

    def play_music(self):
        if self.is_playing_music:
            self.speak("Music is already playing")
            return
        self.is_playing_music = True
        music_dir = os.path.join(os.environ['USERPROFILE'], 'Music')
        music_files = glob.glob(os.path.join(music_dir, "*.mp3"))
        if not music_files:
            self.speak("No music files found in your Music directory")
            self.is_playing_music = False
            return
        self.speak("Playing music")
        self.music_channel = pygame.mixer.Channel(0)
        def play_music_thread():
            for music_file in music_files:
                if not self.is_playing_music:
                    break
                try:
                    self.music_channel.play(pygame.mixer.Sound(music_file))
                    while self.music_channel.get_busy() and self.is_playing_music:
                        pygame.time.Clock().tick(10)
                except Exception as e:
                    self.log_message(f"Error playing music: {e}")
            self.is_playing_music = False
        self.music_thread = Thread(target=play_music_thread, daemon=True)
        self.music_thread.start()

    def stop_music(self):
        if self.is_playing_music:
            self.is_playing_music = False
            self.music_channel.stop()
            self.speak("Music stopped")
        else:
            self.speak("No music is playing")

    def set_alarm(self, command):
        try:
            time_str = command.replace("set alarm for", "").strip()
            minutes = int(re.search(r'\d+', time_str).group())
            alarm_time = datetime.now() + timedelta(minutes=minutes)
            self.alarms.append(alarm_time)
            self.speak(f"Alarm set for {minutes} minutes from now")
        except Exception as e:
            self.log_message(f"Error setting alarm: {e}")
            self.speak("Sorry, I couldn't set the alarm. Say set alarm for X minutes.")

    def check_alarms(self):
        while True:
            current_time = datetime.now()
            for alarm in self.alarms[:]:
                if current_time >= alarm:
                    self.speak("Alarm! Time to wake up!")
                    self.alarms.remove(alarm)
            time.sleep(1)

    def set_timer(self, command):
        try:
            time_str = command.replace("set timer for", "").strip()
            minutes = int(re.search(r'\d+', time_str).group())
            timer_end = datetime.now() + timedelta(minutes=minutes)
            self.timers.append((timer_end, minutes))
            self.speak(f"Timer set for {minutes} minutes")
        except Exception as e:
            self.log_message(f"Error setting timer: {e}")
            self.speak("Sorry, I couldn't set the timer. Say set timer for X minutes.")

    def check_timers(self):
        while True:
            current_time = datetime.now()
            for timer in self.timers[:]:
                end_time, minutes = timer
                if current_time >= end_time:
                    self.speak(f"Timer for {minutes} minutes is up!")
                    self.timers.remove(timer)
            time.sleep(1)

    def send_email(self, command):
        try:
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', command)
            if not email_match:
                self.speak("Please specify a valid email address")
                return
            recipient = email_match.group()
            sender_email = "your_email@gmail.com"  # Replace with your email
            sender_password = "your_app_password"  # Replace with your App Password
            subject = "Message from Surya"
            body = "This is a test email from Surya Voice Assistant."
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient, msg.as_string())
            self.speak(f"Email sent to {recipient}")
        except Exception as e:
            self.log_message(f"Error sending email: {e}")
            self.speak("Sorry, I couldn't send the email.")

    def read_notifications(self):
        notifications = ["You have a new email from John", "Meeting at 3 PM", "Missed call from Sarah"]
        if not notifications:
            self.speak("No new notifications")
        else:
            self.speak("Here are your notifications")
            for notif in notifications:
                self.speak(notif)
                time.sleep(1)

    def adjust_brightness(self, increase=True):
        try:
            current_brightness = sbc.get_brightness()[0]
            new_brightness = min(100, current_brightness + 10) if increase else max(0, current_brightness - 10)
            sbc.set_brightness(new_brightness)
            self.speak(f"Brightness {'increased' if increase else 'decreased'} to {new_brightness}%")
        except Exception as e:
            self.log_message(f"Error adjusting brightness: {e}")
            self.speak("Sorry, I couldn't adjust the brightness")

    def take_note(self, command):
        try:
            note_content = command.replace("take a note", "").strip()
            if not note_content:
                self.speak("Please specify the note content")
                return
            notes = self.load_notes()
            note_id = len(notes) + 1
            notes.append({"id": note_id, "content": note_content, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            self.save_notes(notes)
            self.speak(f"Note {note_id} saved: {note_content}")
        except Exception as e:
            self.log_message(f"Error taking note: {e}")
            self.speak("Sorry, I couldn't save the note")

    def check_battery(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "plugged in" if battery.power_plugged else "not plugged in"
                self.speak(f"Battery is at {percent} percent and is {plugged}")
            else:
                self.speak("Battery information not available")
        except Exception as e:
            self.log_message(f"Error checking battery: {e}")
            self.speak("Sorry, I couldn't check the battery")

    def tell_joke(self):
        jokes = [
            "Why don't skeletons fight each other? Because they don't have the guts!",
            "What do you call fake spaghetti? An impasta!",
            "Why was the math book sad? Because it had too many problems!"
        ]
        joke = random.choice(jokes)
        self.speak(joke)

    def translate_text(self, command):
        try:
            parts = command.replace("translate", "").split("to")
            if len(parts) != 2:
                self.speak("Say translate [text] to [language], like translate hello to Spanish")
                return
            text, language = parts[0].strip(), parts[1].strip().lower()
            lang_codes = {"spanish": "es", "french": "fr", "german": "de", "italian": "it", "japanese": "ja", "chinese": "zh-cn"}
            if language not in lang_codes:
                self.speak(f"Sorry, I don't support {language}. Try Spanish, French, German, Italian, Japanese, or Chinese.")
                return
            translated = self.translator.translate(text, dest=lang_codes[language])
            self.speak(f"The translation of {text} to {language} is {translated.text}")
        except Exception as e:
            self.log_message(f"Error translating text: {e}")
            self.speak("Sorry, I couldn't translate that")

    # New Functions
    def play_youtube_video(self, query):
        try:
            if not query:
                self.speak("Please specify a video to play")
                return
            self.speak(f"Playing {query} on YouTube")
            pywhatkit.playonyt(query)
        except Exception as e:
            self.log_message(f"Error playing YouTube video: {e}")
            self.speak("Sorry, I couldn't play the video")

    def copy_to_clipboard(self, text):
        try:
            if not text:
                self.speak("Please specify text to copy")
                return
            pyperclip.copy(text)
            self.speak(f"Copied '{text}' to clipboard")
        except Exception as e:
            self.log_message(f"Error copying to clipboard: {e}")
            self.speak("Sorry, I couldn't copy that")

    def paste_from_clipboard(self):
        try:
            text = pyperclip.paste()
            if text:
                self.speak(f"Pasted from clipboard: {text}")
            else:
                self.speak("Clipboard is empty")
        except Exception as e:
            self.log_message(f"Error pasting from clipboard: {e}")
            self.speak("Sorry, I couldn't paste that")

    def search_wikipedia(self, query):
        try:
            if not query:
                self.speak("Please specify a Wikipedia search term")
                return
            summary = wikipedia.summary(query, sentences=2)
            self.speak(f"According to Wikipedia: {summary}")
        except Exception as e:
            self.log_message(f"Error searching Wikipedia: {e}")
            self.speak("Sorry, I couldn't find that on Wikipedia")

    def set_reminder(self, command):
        try:
            time_str = command.replace("set reminder for", "").strip()
            minutes = int(re.search(r'\d+', time_str).group())
            reminder_time = datetime.now() + timedelta(minutes=minutes)
            self.timers.append((reminder_time, f"Reminder after {minutes} minutes"))
            self.speak(f"Reminder set for {minutes} minutes from now")
        except Exception as e:
            self.log_message(f"Error setting reminder: {e}")
            self.speak("Sorry, I couldn't set the reminder. Say set reminder for X minutes.")

    def load_notes(self):
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.log_message(f"Error loading notes: {e}")
            return []

    def save_notes(self, notes):
        try:
            with open(self.notes_file, 'w') as f:
                json.dump(notes, f)
        except Exception as e:
            self.log_message(f"Error saving notes: {e}")

    def read_notes(self):
        notes = self.load_notes()
        if not notes:
            self.speak("No notes found")
        else:
            self.speak("Here are your notes:")
            for note in notes:
                self.speak(f"Note {note['id']}: {note['content']} - Created on {note['time']}")
                time.sleep(1)

    def delete_note(self, note_id):
        try:
            note_id = int(note_id)
            notes = self.load_notes()
            notes = [note for note in notes if note['id'] != note_id]
            self.save_notes(notes)
            self.speak(f"Note {note_id} deleted")
        except Exception as e:
            self.log_message(f"Error deleting note: {e}")
            self.speak("Sorry, I couldn't delete that note")

    def check_cpu_usage(self):
        try:
            usage = psutil.cpu_percent(interval=1)
            self.speak(f"CPU usage is at {usage} percent")
        except Exception as e:
            self.log_message(f"Error checking CPU: {e}")
            self.speak("Sorry, I couldn't check CPU usage")

    def check_memory_usage(self):
        try:
            memory = psutil.virtual_memory()
            self.speak(f"Memory usage is at {memory.percent} percent. Available memory is {memory.available // (1024 * 1024)} megabytes")
        except Exception as e:
            self.log_message(f"Error checking memory: {e}")
            self.speak("Sorry, I couldn't check memory usage")

    def lock_screen(self):
        try:
            subprocess.Popen("rundll32.exe user32.dll,LockWorkStation")
            self.speak("Screen locked")
        except Exception as e:
            self.log_message(f"Error locking screen: {e}")
            self.speak("Sorry, I couldn't lock the screen")

    def open_task_manager(self):
        try:
            subprocess.Popen("taskmgr")
            self.speak("Opening Task Manager")
        except Exception as e:
            self.log_message(f"Error opening Task Manager: {e}")
            self.speak("Sorry, I couldn't open Task Manager")

    def generate_random_number(self, command):
        try:
            match = re.search(r'between (\d+) and (\d+)', command)
            if match:
                min_num, max_num = int(match.group(1)), int(match.group(2))
                number = random.randint(min_num, max_num)
                self.speak(f"Random number between {min_num} and {max_num} is {number}")
            else:
                number = random.randint(1, 100)
                self.speak(f"Random number is {number}")
        except Exception as e:
            self.log_message(f"Error generating random number: {e}")
            self.speak("Sorry, I couldn't generate a random number")

    def flip_coin(self):
        result = random.choice(["Heads", "Tails"])
        self.speak(f"I flipped a coin and got {result}")

    def roll_dice(self):
        result = random.randint(1, 6)
        self.speak(f"I rolled a dice and got {result}")

    def set_system_volume(self, command):
        try:
            volume = int(re.search(r'\d+', command).group())
            volume = max(0, min(100, volume))
            # Windows-specific volume control using pyautogui (approximation)
            current_volume = self.volume_scale.get()
            steps = (volume - current_volume) // 2
            if steps > 0:
                pyautogui.press("volumeup", presses=steps)
            elif steps < 0:
                pyautogui.press("volumedown", presses=abs(steps))
            self.volume_scale.set(volume)
            self.speak(f"System volume set to {volume} percent")
        except Exception as e:
            self.log_message(f"Error setting volume: {e}")
            self.speak("Sorry, I couldn't set the volume. Say set volume to X percent.")

    def open_camera(self):
        try:
            subprocess.Popen("start microsoft.windows.camera:", shell=True)
            self.speak("Opening camera")
        except Exception as e:
            self.log_message(f"Error opening camera: {e}")
            self.speak("Sorry, I couldn't open the camera")

    def take_selfie(self):
        try:
            subprocess.Popen("start microsoft.windows.camera:", shell=True)
            time.sleep(2)  # Wait for camera to open
            pyautogui.press("space")  # Take photo (default key in Windows Camera)
            self.speak("Selfie taken, check your Pictures folder")
        except Exception as e:
            self.log_message(f"Error taking selfie: {e}")
            self.speak("Sorry, I couldn't take a selfie")

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text="Initializing...", fg="blue")
            self.speak("Surya is starting")
            self.listen_thread = Thread(target=self.recognize_speech, daemon=True)
            self.listen_thread.start()

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.is_active = False
            self.is_responding = False
            pygame.mixer.Channel(2).stop()
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.stop_respond_button.config(state="disabled")
            self.status_label.config(text="Stopped", fg="black")
            self.log_message("Surya stopped")
            self.speak("Listening stopped")

    def on_closing(self):
        self.is_listening = False
        self.is_active = False
        self.is_responding = False
        self.is_playing_music = False
        pygame.mixer.quit()
        self.speak("Surya is shutting down")
        self.root.destroy()

if __name__ == "__main__":
    try:
        VoiceAssistant()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Install required libraries: pip install SpeechRecognition PyAudio pyautogui google-generativeai pygame gTTS psutil screen-brightness-control googletrans requests pyperclip wikipedia pywhatkit")
    except Exception as e:
        print(f"Unexpected error: {e}")

       
### Full List of Voice Commands

# 1. **"Hey Surya, open [app_name]"**
#    - **Description**: Opens a specified application (e.g., notepad, chrome).
#    - **Example**: "Hey Surya, open notepad"

# 2. **"Hey Surya, shutdown"**
#    - **Description**: Initiates a system shutdown in 30 seconds.
#    - **Example**: "Hey Surya, shutdown"

# 3. **"Hey Surya, cancel shutdown"** or **"Hey Surya, cancel"**
#    - **Description**: Cancels a pending shutdown or restart.
#    - **Example**: "Hey Surya, cancel shutdown"

# 4. **"Hey Surya, restart"**
#    - **Description**: Initiates a system restart in 30 seconds.
#    - **Example**: "Hey Surya, restart"

# 5. **"Hey Surya, sleep"**
#    - **Description**: Puts the computer into sleep mode.
#    - **Example**: "Hey Surya, sleep"

# 6. **"Hey Surya, mute"**
#    - **Description**: Mutes the system volume.
#    - **Example**: "Hey Surya, mute"

# 7. **"Hey Surya, volume up"**
#    - **Description**: Increases the system volume by two steps.
#    - **Example**: "Hey Surya, volume up"

# 8. **"Hey Surya, volume down"**
#    - **Description**: Decreases the system volume by two steps.
#    - **Example**: "Hey Surya, volume down"

# 9. **"Hey Surya, increase brightness"**
#    - **Description**: Increases screen brightness by 10%.
#    - **Example**: "Hey Surya, increase brightness"

# 10. **"Hey Surya, decrease brightness"**
#     - **Description**: Decreases screen brightness by 10%.
#     - **Example**: "Hey Surya, decrease brightness"

# 11. **"Hey Surya, create file"**
#     - **Description**: Creates a new text file on the desktop.
#     - **Example**: "Hey Surya, create file"

# 12. **"Hey Surya, open file [name]"** or **"Hey Surya, open folder [name]"**
#     - **Description**: Opens a file or folder from the desktop.
#     - **Example**: "Hey Surya, open file mydocument.txt"

# 13. **"Hey Surya, take a note [content]"**
#     - **Description**: Saves a note with the specified content.
#     - **Example**: "Hey Surya, take a note Buy groceries"

# 14. **"Hey Surya, search [query]"**
#     - **Description**: Performs a Google search for the query.
#     - **Example**: "Hey Surya, search Python tutorial"

# 15. **"Hey Surya, open website [name]"**
#     - **Description**: Opens a predefined website (e.g., google, wikipedia).
#     - **Example**: "Hey Surya, open website google"

# 16. **"Hey Surya, time"**
#     - **Description**: Reports the current time.
#     - **Example**: "Hey Surya, time"

# 17. **"Hey Surya, date"**
#     - **Description**: Reports the current date.
#     - **Example**: "Hey Surya, date"

# 18. **"Hey Surya, weather [location]"**
#     - **Description**: Reports the weather for the specified location (or "current location" if none given).
#     - **Example**: "Hey Surya, weather in London"

# 19. **"Hey Surya, screenshot"**
#     - **Description**: Takes and saves a screenshot to the desktop.
#     - **Example**: "Hey Surya, screenshot"

# 20. **"Hey Surya, play music"**
#     - **Description**: Plays MP3 files from the Music directory.
#     - **Example**: "Hey Surya, play music"

# 21. **"Hey Surya, stop music"**
#     - **Description**: Stops the currently playing music.
#     - **Example**: "Hey Surya, stop music"

# 22. **"Hey Surya, set alarm for [X] minutes"**
#     - **Description**: Sets an alarm for X minutes from now.
#     - **Example**: "Hey Surya, set alarm for 10 minutes"

# 23. **"Hey Surya, set timer for [X] minutes"**
#     - **Description**: Sets a timer for X minutes.
#     - **Example**: "Hey Surya, set timer for 5 minutes"

# 24. **"Hey Surya, send email to [email_address]"**
#     - **Description**: Sends a test email to the specified address.
#     - **Example**: "Hey Surya, send email to test@example.com"

# 25. **"Hey Surya, read notifications"**
#     - **Description**: Reads out a hardcoded list of sample notifications.
#     - **Example**: "Hey Surya, read notifications"

# 26. **"Hey Surya, check battery"**
#     - **Description**: Reports the battery percentage and charging status.
#     - **Example**: "Hey Surya, check battery"

# 27. **"Hey Surya, tell a joke"**
#     - **Description**: Tells a random joke.
#     - **Example**: "Hey Surya, tell a joke"

# 28. **"Hey Surya, translate [text] to [language]"**
#     - **Description**: Translates text to a specified language (e.g., Spanish, French).
#     - **Example**: "Hey Surya, translate hello to Spanish"

# 29. **"Hey Surya, stop"** or **"Hey Surya, exit"**
#     - **Description**: Stops the assistant from listening.
#     - **Example**: "Hey Surya, stop"

# 30. **"Hey Surya, play video [query]"** or **"Hey Surya, play on youtube [query]"**
#     - **Description**: Plays a YouTube video based on the query.
#     - **Example**: "Hey Surya, play video Happy Birthday on YouTube"

# 31. **"Hey Surya, copy text [text]"**
#     - **Description**: Copies the specified text to the clipboard.
#     - **Example**: "Hey Surya, copy text Hello World"

# 32. **"Hey Surya, paste text"**
#     - **Description**: Speaks the current clipboard content.
#     - **Example**: "Hey Surya, paste text"

# 33. **"Hey Surya, wikipedia [query]"**
#     - **Description**: Provides a brief Wikipedia summary for the query.
#     - **Example**: "Hey Surya, wikipedia Python"

# 34. **"Hey Surya, set reminder for [X] minutes"**
#     - **Description**: Sets a reminder for X minutes from now.
#     - **Example**: "Hey Surya, set reminder for 15 minutes"

# 35. **"Hey Surya, read notes"**
#     - **Description**: Reads all saved notes.
#     - **Example**: "Hey Surya, read notes"

# 36. **"Hey Surya, delete note [id]"**
#     - **Description**: Deletes a note by its ID.
#     - **Example**: "Hey Surya, delete note 1"

# 37. **"Hey Surya, check cpu"**
#     - **Description**: Reports the current CPU usage.
#     - **Example**: "Hey Surya, check cpu"

# 38. **"Hey Surya, check memory"**
#     - **Description**: Reports the current memory usage and available memory.
#     - **Example**: "Hey Surya, check memory"

# 39. **"Hey Surya, lock screen"**
#     - **Description**: Locks the Windows screen.
#     - **Example**: "Hey Surya, lock screen"

# 40. **"Hey Surya, open task manager"**
#     - **Description**: Opens the Windows Task Manager.
#     - **Example**: "Hey Surya, open task manager"

# 41. **"Hey Surya, random number"** or **"Hey Surya, random number between [X] and [Y]"**
#     - **Description**: Generates a random number (default 1-100, or within a specified range).
#     - **Example**: "Hey Surya, random number between 1 and 100"

# 42. **"Hey Surya, flip a coin"**
#     - **Description**: Simulates flipping a coin and reports heads or tails.
#     - **Example**: "Hey Surya, flip a coin"

# 43. **"Hey Surya, roll a dice"**
#     - **Description**: Simulates rolling a 6-sided die and reports the result.
#     - **Example**: "Hey Surya, roll a dice"

# 44. **"Hey Surya, set volume to [X] percent"**
#     - **Description**: Sets the system volume to X percent.
#     - **Example**: "Hey Surya, set volume to 50 percent"

# 45. **"Hey Surya, open camera"**
#     - **Description**: Opens the default Windows Camera app.
#     - **Example**: "Hey Surya, open camera"

# 46. **"Hey Surya, take selfie"**
#     - **Description**: Opens the camera and attempts to take a photo.
#     - **Example**: "Hey Surya, take selfie"

# 47. **[Anything else]**
#     - **Description**: For unrecognized commands, Surya queries the Gemini API for a response.
#     - **Example**: "Hey Surya, what is the meaning of life?"

# ---

# ### Total Commands: 47 Specific Commands + General Query
