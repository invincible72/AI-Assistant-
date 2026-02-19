import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os
import speech_recognition as sr
import threading
import sys
import math
import re
import pywhatkit
import time
import requests
import json
import subprocess
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from torch.utils.data import DataLoader
import tempfile

engine = pyttsx3.init()
engine.setProperty('rate', 180)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

MODEL_SAVE_DIR = "D:\\SERA\\my_robo_lm"
if not os.path.exists(MODEL_SAVE_DIR):
   raise FileNotFoundError(f"Model folder not found at {MODEL_SAVE_DIR}")

os.environ["TRANSFORMERS_OFFLINE"] ="1"
tokenizer = AutoTokenizer.from_pretrained(MODEL_SAVE_DIR,local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_SAVE_DIR,local_files_only=True)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device="cpu")

def speak(text):
    cleaned_text = re.sub(r'[*_`]', '',text)
    engine.say(cleaned_text)
    engine.runAndWait()

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except:
        return "Could not find information on Wikipedia."
    

def chat_with_small_lm(user_message):
    if generator is None:
        return "Language model not loaded. Please train or load the model first."

    prompt = f"{user_message} →"
    try:
        output = generator(
            prompt,
            max_length=len(tokenizer.encode(prompt)) + 500,  
            do_sample=True,
            top_k=40,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.3
        )[0]['generated_text']

        response = output.replace(prompt, "").strip()

        if response and response.lower() not in ["", "i don't know", "error"]:
            return " ".join(response.split()[:5000]) 

    except Exception as e:
        return f"Error generating response: {e}"

def greeting_message():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning Aaryan! "
    elif 12 <= current_hour < 16:
        greeting = "Good Afternoon Aaryan! "
    elif 16 <= current_hour < 21:
        greeting = "Good Evening Aaryan! "
    else:
        greeting = "Good Night Aaryan! "
    speak(greeting)

def respond(command):
    command = command.lower()

    if "open notepad" in command:
        try:
            subprocess.Popen(["notepad.exe"])
            return "Opening Notepad."
        except FileNotFoundError:
             return "Notepad not found. This command is for Windows."
    elif "open chrome" in command:
        try:
            webbrowser.open("https://www.google.com")
            return "Opening Google Chrome."
        except Exception as e:
            return f"Could not open Chrome: {e}"
    elif "what is time" in command:
        return datetime.datetime.now().strftime("It's %I:%M %p now.")
    
    elif "play song" in command:
        pywhatkit.playonyt("one of the girl tonight by the weekend")
        return "Playing song."
    
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."
    
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    
    elif "shutdown system" in command:
        os.system("shutdown /s /t 1")
        return "Bye Bye Master."
    elif "open chrome" in command:
        os.system("start chrome")
        return "Opening Google Chrome."
    elif "what is time" in command:
        return datetime.datetime.now().strftime("It's %I:%M %p now.")
    elif "play song" in command:
        pywhatkit.playonyt("one of the girl tonight by the weeknd")
        return "Playing song."
    elif "i want to download movie" in command:
        webbrowser.open("http://www.9xflix.me")
        return "Sir, now you can download your favorite movie."
    elif "play movie" in command:
        webbrowser.open("https://youtu.be/uoGCXFuDiQo?si=JIeJiy67MPgzlzkc")
        return "Playing movie."
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    elif "shut down system" in command:
        os.system("shutdown /s /t 1")
        return "Bye Bye Master."
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp."
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        return "Opening Instagram."
    elif "open myntra" in command:
        webbrowser.open("https://www.myntra.com")
        return "Opening Myntra."
    elif "open music player" in command:
        webbrowser.open("https://music.youtube.com")
        return "Opening music player."
    elif "open github" in command:
        webbrowser.open("https://github.com/")
        return "Opening GitHub."
    elif "open hotstar" in command:
        webbrowser.open("https://www.hotstar.com/")
        return "Opening Hotstar."
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
        return "Opening Facebook."
    elif "i am tired" in command:
        webbrowser.open("https://www.crazygames.com/")
        return "Here your games sir."
    elif "play cartoon" in command:
        webbrowser.open("https://youtu.be/Y1y8794duDA?si=YLMy3ScEMnO4s21O")
        return "Here your cartoon sir."
    elif "open terminal" in command:
        os.system("start cmd")
        return "Opening terminal."
    elif "weather information" in command:
        webbrowser.open("https://www.accuweather.com/")
        return "weather information of your area"
    elif "open chatgpt" in command:
        webbrowser.open("https://www.chatgpt.com")
        return "Opening ChatGPT."
    elif "open flipkart" in command:
        webbrowser.open("https://www.flipkart.com")
        return "Opening Flipkart."
    elif "open calculator" in command:
        os.system("calc")
        return "opening calculator"
    elif "open camera" in command:
        os.system("start microsoft.windows.camera:")
        return "opening camera"
    elif "open paint" in command:
        os.system("mspaint")
        return "opening paint"
    elif "system status" in command:
        os.system("taskmgr")
        return "displaying system status "
    elif "open system setting" in command:
        os.system("start ms-settings:")
        return "setting initilazied"
    elif "open udemy" in command:
        webbrowser.open("https://in.udemy.com/")
        return "Opening udemy."  
    elif "open grock" in command:
        webbrowser.open("https://x.ai/grok")
        return "Opening grock."  
    elif "open firefly" in command:
        webbrowser.open("https://www.adobe.com/")
        return "Opening firefly"
    elif "open blackbox" in command:
        webbrowser.open("https://blackbox.ai/")
        return "Opening blackbox"
    elif "i want to create presentation" in command:
        webbrowser.open("https://gamma.app/")
        return "Go for it sir."
    elif "open e-mail" in command:
        webbrowser.open("https://mail.google.com/mail/u/0/")
        return "Here is your workspace sir."
    elif "open ms edge" in command:
        os.system("start msedge")
        return "microsoft edge"
    elif "who created you " in command:
        return "i am creation of aryan"
    elif " name " in command:
        return " i am JARVIS"
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp."
    
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        return "Opening Instagram."
    
    elif "open myntra" in command:
        webbrowser.open("https://www.myntra.com")
        return "Opening Myntra."
    
    elif "open music player" in command:
        webbrowser.open("https://music.youtube.com")
        return "Opening music player."
    
    elif "open github" in command:
        webbrowser.open("https://github.com/")
        return "Opening GitHub."
    
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
        return "Opening Facebook."
    
    elif "i am tired" in command:
        webbrowser.open("https://www.crazygames.com/")
        return "Here your games sir."
    
    elif "open terminal" in command:
        os.system("start cmd")
        return "Opening terminal."
    
    elif "open chatgpt" in command:
        webbrowser.open("https://www.chatgpt.com")
        return "Opening ChatGPT."
    
    elif "open flipkart" in command:
        webbrowser.open("https://www.flipkart.com")
        return "Opening Flipkart."
    
    elif "open calculator" in command:
        os.system("calc")
        return "opening calculator"
    
    elif "open camera" in command:
        os.system("start microsoft.windows.camera:")
        return "opening camera"
    
    elif "system status" in command:
        os.system("taskmgr")
        return "displaying system status "
    
    elif "open system setting" in command:
        os.system("start ms-settings:")
        return "setting initilazied"
    
    elif "open udemy" in command:
        webbrowser.open("https://in.udemy.com/")
        return "Opening udemy." 
     
    elif "open robo store" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=3a4ed4aabcca2385edd3fabf4868241ca88fa31fb975b0b634fe7010127085b0JmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=robu.ai&u=a1aHR0cHM6Ly9yb2J1LmluLw")
        return "buy part dear"
    
    elif "open grock" in command:
        webbrowser.open("https://x.ai/grok")
        return "Opening grock." 
     
    elif "open research papers section" in command:
        webbrowser.open("https://roboticsbiz.com/500-recent-research-papers-and-projects-in-robotics-free-download/")
        return "search for your paper "
    
    elif "open research paper on robotic navigation" in command:
        webbrowser.open("https://iris.polito.it/retrieve/handle/11583/2638899/102665/MMSP_submitted.pdf")
        return "here is your desired paper"
    
    elif "open research paper on sensor for navigation" in command:
        webbrowser.open("http://article.ijbse.org/pdf/10.11648.j.ijbse.20180601.11.pdf")
        return "here is your desired paper"
    
    elif "open research paper on motion control of a three active wheeled mobile robot" in command:
        webbrowser.open("http://www.iaeng.org/publication/IMECS2016/IMECS2016_pp248-253.pdf")
        return "here is your desired paper"
    
    elif "open research paper on robot vision based navigation system" in command:
        webbrowser.open("https://www.ijsr.net/archive/v5i2/NOV161279.pdf")
        return "here is your desired paper"
    
    elif "open research paper on application of ant colony optimization for finding the navigational path of mobile robot" in command:
        webbrowser.open("http://ijiset.com/vol3/v3s2/IJISET_V3_I2_28.pdf")
        return "here is your desired paper"
    
    elif "open research paper on robot navigation using a brain-computer interface" in command:
        webbrowser.open("https://www.researchgate.net/profile/Y-C_Yu2/publication/301201620_Robot_Navigation_Using_a_Brain-Computer_Interface/links/570bf14208ae8883a1ffdfe4.pdf")
        return "here is your desired paper"
    elif "open research paper on Path Generation for Robot Navigation using a Single Ceiling Mounted Camera" in command:
        webbrowser.open("http://ijseas.com/volume2/v2i1/ijseas20160137.pdf")
        return "here is your desired paper"
    
    elif "open research paper on exact robot navigation using power diagrams" in command:
        webbrowser.open("http://kodlab.seas.upenn.edu/uploads/Main/arslan_kod_ICRA2016B.pdf")
        return "here is your desired paper"
    
    elif "open research paper on bayesian inverse reinforcement learning" in command:
        webbrowser.open("http://spencer.eu/papers/okalICRA16.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Neural Network Controller" in command:
        webbrowser.open("https://www.researchgate.net/profile/Najmuddin_Aamer/publication/292132830_Pipelined_High_Speed_Low_Power_Neural_Network_Controller_for_Autonomous_Mobile_Robot_Navigation_Using_FPGA/links/56a92b7f08ae2df821650e45.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Proxemics model" in command:
        webbrowser.open("https://hal.archives-ouvertes.fr/hal-01082517/file/WSIROS_Barnaud.pdf")
        return "here is your desired paper"
    
    elif "open research paper on aerial robotics" in command:
        webbrowser.open("https://www.researchgate.net/profile/Martin_Saska/publication/301292252_Aerial_Robotics_Compact_groups_of_cooperating_micro_aerial_vehicles_in_clustered_GPS_denied_environment/links/570fea1408ae19b186938643.pdf")
        return "here is your desired paper"
    
    elif "open research paper on multi destination path planning" in command:
        webbrowser.open("http://downloads.hindawi.com/journals/jece/aip/3620895.pdf")
        return "here is your desired paper"
    
    elif "open research paper on integrating modeling" in command:
        webbrowser.open("http://icaps17.icaps-conference.org/workshops/KEPS/proceedingsKEPS.pdf#page=21")
        return "here is your desired paper"
    
    elif "open research paper on robot motion planning for pouring liquids" in command:
        webbrowser.open("http://gamma.cs.unc.edu/FluidMotion/icaps.pdf")
        return "here is your desired paper"
    
    elif "open research paper on motion planning for multi robot system" in command:
        webbrowser.open("http://www.eecs.berkeley.edu/~sseshia/pubdir/iccps16-implan.pdf")
        return "here is your desired paper"
    
    elif "open research paper on motion planning of humanoid climbing robot" in command:
        webbrowser.open("http://www.sic.shibaura-it.ac.jp/~ashimada/research/theses/2016_3_8_SAMCON2016_ashimada_IS4-1.pdf")
        return "here is your desired paper"
    
    elif "open research paper on POMDP" in command:
        webbrowser.open("https://pdfs.semanticscholar.org/6b71/550045abeb716b12afbe15bf6814c660ed91.pdf")
        return "here is your desired paper"
    elif "open research paper on planning aware communication for multi robot coordination" in command:
        webbrowser.open("https://www.researchgate.net/profile/Graeme_Best/publication/323336123_Planning-Aware_Communication_for_Decentralised_Multi-Robot_Coordination/links/5a8e5630aca272c56bc41b92/Planning-Aware-Communication-for-Decentralised-Multi-Robot-Coordination.pdf")
        return "here is your desired paper"
    
    elif "open research paper on four degree of freedom" in command:
        webbrowser.open("http://mechanismsrobotics.asmedigitalcollection.asme.org/data/Journals/JMROA6/935288/jmr_008_05_051016.pdf")
        return "here is your desired paper"
    
    elif "open research paper on robotics in ovarian transposition" in command:
        webbrowser.open("http://www.ejmanager.com/mnstemps/6/6-1365862014.pdf?t=1366051922")
        return "here is your desired paper"
    
    elif "open research paper on OpenWoZ" in command:
        webbrowser.open("http://guyhoffman.com/publications/HoffmanAAAISS16.pdf")
        return "here is your desired paper"
    
    elif "open research paper on privacy in human robot interaction" in command:
        webbrowser.open("http://robots.law.miami.edu/2016/wp-content/uploads/2015/07/Rueben_Smart_PrivacyInHRI_WeRobot2016.pdf")
        return "here is your desired paper"
    
    elif "open research paper on state representation learning in robotics" in command:
        webbrowser.open("http://www.robotics.tu-berlin.de/fileadmin/fg170/Publikationen_pdf/Jonschkowski-14-RSS.pdf")
        return "here is your desired paper"
    
    elif "open research paper on eliciting conversation in robotics vehicle interactions" in command:
        webbrowser.open("http://www.wendyju.com/publications/sirkin_aaai16.pdf")
        return "here is your desired paper"
    
    elif "open research paper on exercising with baxter" in command:
        webbrowser.open("https://aiweb.techfak.uni-bielefeld.de/hri2018_workshop_robot_coach/paper/PREC2018_paper_3.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Computational Analysis of Affect, Personality, and Engagement in HumanRobot Interactions" in command:
        webbrowser.open("https://www.cl.cam.ac.uk/~hg410/CeliktutanEtAl-AR-Chapter-2017.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Human-robot interactions" in command:
        webbrowser.open("https://www.researchgate.net/profile/Sandeep_Nagar/publication/296677175_Human_Robot_Interaction_-_A_Psychological_Perspective/links/56d7f7d208aebe4638af2595.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Gait of Quadruped Robot and Interaction Based on Gesture Recognition" in command:
        webbrowser.open("https://www.researchgate.net/profile/Tuyen_Nguyen24/publication/283187478_Gait_of_Quadruped_Robot_and_Interaction_Based_on_Gesture_Recognition/links/5637813208ae9d3e0347c39d.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Interactive Robotics Workshop" in command:
        webbrowser.open("http://www.terecop.eu/TRTWR-RIE2014/files/00_WFr1/00_WFr1_08.pdf")
        return "here is your desired paper"
    elif "open research paper on Activating Robotics Manipulator using Eye Movements" in command:
        webbrowser.open("http://www.ijeit.com/Vol%204/Issue%203/IJEIT1412201409_18.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Gesture Controlled Robot using LabVIEW" in command:
        webbrowser.open("http://ijireeice.com/upload/2016/may-16/IJIREEICE%2050.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Low Cost Obstacle Avoidance Robot with Logic Gates and Gate Delay Calculations" in command:
        webbrowser.open("http://article.acisjournal.org/pdf/10.11648.j.acis.20180601.11.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Advanced Fuzzy Potential Field Method for Mobile Robot Obstacle Avoidance" in command:
        webbrowser.open("http://downloads.hindawi.com/journals/cin/aip/176034.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Controlling Obstacle Avoiding And Live Streaming Robot Using Chronos Watch" in command:
        webbrowser.open("http://ijeir.org/administrator/components/com_jresearch/files/publications/IJEIR_2021_Final.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Movement Of The Space Robot Manipulator In Environment With Obstacles" in command:
        webbrowser.open("http://nanomat.spbu.ru/sites/default/files/Sbornik_Polyakh.pdf#page=254")
        return "here is your desired paper"
    
    elif "open research paper on Assis-Cicerone Robot With Visual Obstacle Avoidance Using a Stack of Odometric Data." in command:
        webbrowser.open("http://www.iaeng.org/IJCS/issues_v45/issue_1/IJCS_45_1_26.pdf")
        return "here is your desired paper"
    
    elif "open research paper on  Obstacle detection and avoidance methods for autonomous mobile robot" in command:
        webbrowser.open("http://www.ijsr.net/archive/v5i1/NOV152937.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Moving Domestic Robotics Control Method Based on Creating and Sharing Maps with Shortest Path Findings and Obstacle Avoidance" in command:
        webbrowser.open("http://www.thesai.org/Downloads/IJARAI/Volume2No2/Paper_4-Moving_Domestic_Robotics_Control_Method_Based_on_Creating_and_Sharing_Maps_with_Shortest_Path_Findings_and_Obstacle_Avoidance.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Control of the Differentially-driven Mobile Robot in the Environment with a Non-Convex Star-Shape Obstacle: Simulation and Experiments" in command:
        webbrowser.open("http://www.uni-obuda.hu/journal/Kowalczyk_Kozlowski_65.pdf")
        return "here is your desired paper"
    
    elif "open research paper on A survey of typical machine learning based motion planning algorithms for robotics" in command:
        webbrowser.open("https://www.researchgate.net/profile/Chengmin_Zhou/publication/338454195_A_survey_of_typical_machine_learning_based_motion_planning_algorithms_for_robotics/links/5e15d2aca6fdcc2837620049/A-survey-of-typical-machine-learning-based-motion-planning-algorithms-for-robotics.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Linear Algebra for Computer Vision, Robotics , and Machine Learning" in command:
        webbrowser.open("https://www.seas.upenn.edu/~cis515/linalg-I.pdf")
        return "here is your desired paper"
    
    elif "open research paper on Applying Radical Constructivism to Machine Learning: A Pilot Study in Assistive Robotics" in command:
        webbrowser.open("http://elib.dlr.de/119365/1/article.2018.Nowak.RC%20and%20iML.ConstrFound.pdf")
        return "here is your desired paper"
    
    elif "open research paper on AI in robotics" in command:
        webbrowser.open("https://www.researchgate.net/publication/372589771_ARTIFICIAL_INTELLIGENCE_IN_ROBOTICS_FROM_AUTOMATION_TO_AUTONOMOUS_SYSTEMS")
        return "here is your desired paper"
    
    elif "open research paper on computer vision in robotics" in command:
        webbrowser.open("https://www.academia.edu/Documents/in/Computer_Vision_and_Robotics")
        return "here is your desired paper"
    
    elif "open research paper on robotics" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=3a5d4703c421f4d0e753e62453aa1f274af2da75597cb86afee91070cc7dce62JmltdHM9MTc1NzM3NjAwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=research+paper+on+types+of+robotics+&u=a1aHR0cHM6Ly9pam1yZS5pbi91cGxvYWRzL3YxL0ElMjBDb21wcmVoZW5zaXZlJTIwU3R1ZHklMjBvbiUyMFJvYm90aWNzLnBkZg")
        return "here is your desired paper"
      
    elif "e-book on history of robotics" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=e29dbb4102e436d33b3e89e30e6bfcd49eb2f9807c5fda27d0795d1503e33f77JmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=pdf+on+history+of+robotics+&u=a1aHR0cHM6Ly93d3cuYmhhcmF0aHVuaXYuYWMuaW4vcGFnZV9pbWFnZXMvcGRmL2NvdXJzZXdhcmVfZWVlL05vdGVzL05FMS9CRUUwMDklMjBST0JPVC5wZGY")
        return "here is your desired book"
    
    elif "e-book on introduction of robotics" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=332f3f2936c5567593db832baaa7105078c7b94d84b1cdd81605720c1d9c6f0cJmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=pdf+on+introduction+of+robotics+&u=a1aHR0cHM6Ly9zaXN0LnNhdGh5YWJhbWEuYWMuaW4vc2lzdF9jb3Vyc2VtYXRlcmlhbC91cGxvYWRzL1NDU0ExNDA2LnBkZg")
        return "here is your desired book"
    
    elif "e-book on AI in robotics" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=f92b2adef1e9b2cffe5ca8e16ec9c905cb36c08104aa5c523d8194ccbab1a610JmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=pdf+on+ai+ml++robotics+&u=a1aHR0cHM6Ly93d3cucmVzZWFyY2hnYXRlLm5ldC9wdWJsaWNhdGlvbi8zNzI1ODk3NzFfQVJUSUZJQ0lBTF9JTlRFTExJR0VOQ0VfSU5fUk9CT1RJQ1NfRlJPTV9BVVRPTUFUSU9OX1RPX0FVVE9OT01PVVNfU1lTVEVNUw")
        return "here is your desired book"
    
    elif "e-book on robotics software" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=56ec6aac243243514acc28101161a089867dc7f9524c8c851b54d274f14e298bJmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=pdf+on+software+of+robotics+&u=a1aHR0cHM6Ly93d3cucmVzZWFyY2hnYXRlLm5ldC9wdWJsaWNhdGlvbi8zNDk2MjA4NzRfU29mdHdhcmVfRW5naW5lZXJpbmdfZm9yX1JvYm90aWNfU3lzdGVtc2Ffc3lzdGVtYXRpY19tYXBwaW5nX3N0dWR5")
        return "here is your desired book"
    
    elif "e-book on robotics hardware" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=4d19519c1a345b8a7f7e4405d98583501209616f17397027f3b1c8e2b6eb4f21JmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=pdf+on+robotics+hardware&u=a1aHR0cHM6Ly93d3cuZW5nLnlhbGUuZWR1L2dyYWJsYWIvcHVicy9QYXRlbF9SQU0yMDIzLnBkZg")
        return "here is your desired book"
    
    elif "e-book on robots types" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=6fc3b751309b31032689a6cda2b0926348f42355e93d2484051bae0d1889e99eJmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=pdf+on+types+of+robots&u=a1aHR0cHM6Ly93d3cuaW50ZWxsc3BvdC5jb20vdHlwZXMtb2Ytcm9ib3RzLw")
        return "here is your desired book"
    
    elif "e-book on python programming" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=7dd57701faa301c089aba56dddf0c013d429edf6e69617b67a5585a6a3e701afJmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=pdf+on+python+programming+language&u=a1aHR0cDovL3d3dy5paW1jaHlkZXJhYmFkLmNvbS9NYXRlcmlhbC9pbnRyb2R1Y3Rpb24tdG8tcHl0aG9uLXByb2dyYW1taW5nLnBkZg")
        return "here is your desired book"
    
    elif "e-book on future trends of robotics" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=60ecb5863c39a515155876d8018c8d6477ad452d1bffefc3f4a54c09a1a51decJmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=pdf+on+future+trend+in+robotics&u=a1aHR0cHM6Ly93d3cuc3ZiLmNvbS9jb250ZW50YXNzZXRzL2VmN2Q0NDc5OTIxMDQzYzJhOWQxOGE1OTI2NDljNjU5L2Z1dHVyZS1vZi1yb2JvdGljc19zdmItc2VjdG9yLXJlcG9ydC0yMDIwLnBkZj9zdHJlYW09ZnV0dXJl")
        return "here is your desired book"
    
    elif "e-book on application of robotics" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=2cf822be4eb64d5c7633001575a335cef6d4b96d0f2777493a89f769ba308559JmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=pdf+on+applications+of+robotics&u=a1aHR0cHM6Ly92YXJkaGFtYW4ub3JnL3dwLWNvbnRlbnQvdXBsb2Fkcy8yMDIxLzAzL1JPQk9USUNTLnBkZg")
        return "here is your desired book"
    
    elif "e-book on robotic os" in command:
        webbrowser.open("https://www.bing.com/ck/a?!&&p=05baf546f5295008e4b41aaa620d1e3093b2ee140814fb72036b28edc82dcabdJmltdHM9MTc1NzcyMTYwMA&ptn=3&ver=2&hsh=4&fclid=3a7610be-6a1b-6fe6-1423-06e26b1d6eb3&psq=pdf+on++ros&u=a1aHR0cHM6Ly9zY2V3ZWIuc2NlLnVoY2wuZWR1L2hhcm1hbi9DRU5HNTQzN19Nb2JpbGVSb2JvdHMvV2ViaXRlbXMyMDIwL1JPU19ST0JPVElDU19CWV9FWEFNUExFX1NFQ09ORF9FRElUSU9OLnBkZg")
        return "here is your desired book"
    
    elif "i want to buy book on robotics" in command:
        webbrowser.open("https://www.amazon.com/dp/1107156300")
        return "here you can buy your desired book"
    
    elif "i want to buy book on introduction of robotics" in command:
        webbrowser.open("https://www.amazon.com/dp/3319325507")
        return "here you can buy your desired book"
    
    elif "i want to buy book on control system" in command:
        webbrowser.open("https://www.amazon.com/dp/0471649902")
        return "here you can buy your desired book"
    
    elif "i want to buy book on mobile robots" in command:
        webbrowser.open("https://www.amazon.com/dp/0262015358")
        return "here you can buy your desired book"
    
    elif "i want to buy book on mechanics" in command:
        webbrowser.open("https://www.amazon.com/dp/0201543613")
        return "here you can buy your desired book"
    
    elif "i want to buy book on probabilistic robotics" in command:
        webbrowser.open("https://www.amazon.com/dp/0262201623")
        return "here you can buy your desired book"
    
    elif "i want to buy book on robotics vision" in command:
        webbrowser.open("https://www.amazon.com/dp/3642201431")
        return "here you can buy your desired book"
    
    elif "i want to buy book on robotics MPC" in command:
        webbrowser.open("https://www.amazon.com/dp/1846286417")
        return "here you can buy your desired book"
    
    elif "i want to buy book on robotics algorithms" in command:
        webbrowser.open("https://www.amazon.com/dp/0387743146")
        return "here you can buy your desired book"
    
    elif "i want to buy book on robotics numeric study" in command:
        webbrowser.open("https://www.amazon.com/dp/0849379814")
        return "here you can buy your desired book"
    
    elif "i want to buy book on convex optimization" in command:
        webbrowser.open("https://www.amazon.com/dp/0521833787")
        return "here you can buy your desired book"
    
    elif "i want to buy book on numerical optimization" in command:
        webbrowser.open("https://www.amazon.com/dp/0387303030")
        return "here you can buy your desired book"
    
    elif "i want to buy book on optimization algorithm" in command:
        webbrowser.open("https://www.amazon.com/dp/0691132984")
        return "here you can buy your desired book"
    
    elif "i want to buy book on planning algorithm" in command:
        webbrowser.open("https://www.amazon.com/dp/0521862051")
        return "here you can buy your desired book"
    
    elif "i want to buy book on robot motion" in command:
        webbrowser.open("https://www.amazon.com/dp/0262033275")
        return "here you can buy your desired book"
    
    elif "i want to buy book on spot" in command:
        webbrowser.open("https://www.amazon.com/dp/1852331739")
        return "here you can buy your desired book"
    
    elif "i want to buy book on ROS" in command:
        webbrowser.open("https://www.amazon.com/dp/1783551798")
        return "here you can buy your desired book"
    
    elif "i want to buy book on robotics projects" in command:
        webbrowser.open("https://www.amazon.com/dp/1788835441")
        return "here you can buy your desired book"
    
    elif "i want to buy book on fundamentals of robotics" in command:
        webbrowser.open("https://www.amazon.com/Geometric-Fundamentals-Robotics-Monographs-Computer/dp/0387208747?utm_source=chatgpt.com")
        return "here you can buy your desired book"
    
    elif "i want to buy book on multibody dynamics" in command:
        webbrowser.open("https://www.amazon.com/dp/1441972668")
        return "here you can buy your desired book"
    
    elif "i want to buy book on foundation of robotics" in command:
        webbrowser.open("https://www.amazon.com/dp/9811919828")
        return "here you can buy your desired book"
    
    elif "i want to buy book on robotics prim" in command:
        webbrowser.open("https://www.amazon.com/Robotics-Primer-Intelligent-Autonomous-Agents/dp/026263354X")
        return "here you can buy your desired book"
    
    elif "i want to buy book on AI robotics" in command:
        webbrowser.open("https://www.amazon.com/Introduction-Robotics-Intelligent-Autonomous-Agents/dp/B00EKYKO1W")
        return "here you can buy your desired book"
    
    elif "i want to buy book on mobile microbotics" in command:
        webbrowser.open("https://www.amazon.com/Mobile-Microrobotics-Intelligent-Robotics-Autonomous/dp/0262036436")
        return "here you can buy your desired book"
    
    elif "i want to buy book on robot to human" in command:
        webbrowser.open("https://www.amazon.com/Almost-Human-Making-Robots-Think/dp/0393336840")
        return "here you can buy your desired book"
    
    elif "i want to buy book on cybersecurity for robots" in command:
        webbrowser.open("https://www.amazon.com/dp/1680838601")
        return "here you can buy your desired book"
    
    elif "i want to buy book on ros beginners" in command:
        webbrowser.open("https://www.amazon.com/dp/1484234049")
        return "here you can buy your desired book"
    
    elif "open firefly" in command:
        webbrowser.open("https://www.adobe.com/")
        return "Opening firefly"
    
    elif "open blackbox" in command:
        webbrowser.open("https://blackbox.ai/")
        return "Opening blackbox"
    
    elif "i want to create presentation" in command:
        webbrowser.open("https://gamma.app/")
        return "Go for it sir."
    
    elif "open e-mail" in command:
        webbrowser.open("https://mail.google.com/mail/u/0/")
        return "Here is your workspace sir."
    
    elif "open microsoft edge" in command:
        os.system("start msedge")
        return "microsoft edge initialized"
    
    elif "i want to download movie" in command:
        webbrowser.open("http://www.9xflix.me")
        return "Sir, now you can download your favorite movie."
    
    elif "play movie" in command:
        webbrowser.open("https://youtu.be/uoGCXFuDiQo?si=JIeJiy67MPgzlzkc")
        return "Playing movie."
    
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."
    
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    
    elif "shut down system" in command:
        return "System shutdown commands are disabled for safety."
    
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp."
    
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        return "Opening Instagram."
    
    elif "open myntra" in command:
        webbrowser.open("https://www.myntra.com")
        return "Opening Myntra."
    
    elif "open music player" in command:
        webbrowser.open("https://music.youtube.com")
        return "Opening music player."
    
    elif "open github" in command:
        webbrowser.open("https://github.com/")
        return "Opening GitHub."
    
    elif "open hotstar" in command:
        webbrowser.open("https://www.hotstar.com/")
        return "Opening Hotstar."
    
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
        return "Opening Facebook."
    
    elif "i am tired" in command:
        webbrowser.open("https://www.crazygames.com/")
        return "Here your games sir."
    
    elif "play cartoon" in command:
        webbrowser.open("https://youtu.be/Y1y8794duDA?si=YLMy3ScEMnO4s21O")
        return "Here your cartoon sir."
    
    elif "open terminal" in command:
        try:
             if os.name == 'nt': 
                 subprocess.Popen(["cmd"])
             elif os.name == 'posix': 
                  subprocess.Popen(["x-terminal-emulator"]) 
             return "Opening terminal."
        except FileNotFoundError:
            return "Terminal not found or command not adapted for your OS."
        
    elif "weather information" in command:
        webbrowser.open("https://www.accuweather.com/")
        return "weather information of your area"
    
    elif "open chatgpt" in command:
        webbrowser.open("https://www.chatgpt.com")
        return "Opening ChatGPT."
    
    elif "open flipkart" in command:
        webbrowser.open("https://www.flipkart.com")
        return "Opening Flipkart."
    
    elif "open calculator" in command:
        try:
            subprocess.Popen(["calc.exe"]) 
            return "opening calculator"
        except FileNotFoundError:
            return "Calculator not found. This command is for Windows."
    
    elif "open paint" in command:
        try:
            subprocess.Popen(["mspaint"]) 
            return "opening paint"
        except FileNotFoundError:
             return "Paint not found. This command is for Windows."
        
    elif "system status" in command:
        try:
            if os.name == 'nt': 
                subprocess.Popen(["taskmgr"])
                return "displaying system status "
            else:
                return "System status command not adapted for your OS."
        except FileNotFoundError:
             return "Task manager not found. This command is for Windows."
        
    elif "open system setting" in command:
        return "System setting commands are OS-dependent and not implemented."
    
    elif "open udemy" in command:
        webbrowser.open("https://in.udemy.com/")
        return "Opening udemy."
    
    elif "open grock" in command:
        webbrowser.open("https://x.ai/grok")
        return "Opening grock."
    
    elif "open firefly" in command:
        webbrowser.open("https://www.adobe.com/")
        return "Opening firefly"
    
    elif "open blackbox" in command:
        webbrowser.open("https://blackbox.ai/")
        return "Opening blackbox"
    
    elif "i want to create presentation" in command:
        webbrowser.open("https://gamma.app/")
        return "Go for it sir."
    
    elif "open e-mail" in command:
        webbrowser.open("https://mail.google.com/mail/u/0/")
        return "Here is your workspace sir."
    
    elif "open ms edge" in command:
        try:
            subprocess.Popen(["msedge"]) 
            return "microsoft edge"
        except FileNotFoundError:
            return "Microsoft Edge not found. This command is for Windows."
        
    elif "wikipedia" in command:
        return search_wikipedia(command.replace("wikipedia", ""))
    
    elif "close" in command or "exit" in command:
        stop_assistant()

    else:
        return chat_with_small_lm(command)

def stop_assistant():
    speak("Bye Bye Sir and have a good day.")
    root.quit() 

def listen_voice():
    if generator is None:
        speak("Language model not loaded. Cannot process voice input.")
        return

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        status_label.config(text="SERA (Listening...)")
        root.update()
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

        except sr.WaitTimeoutError:
            status_label.config(text="SERA (Timeout)")
            return
        
        except Exception as e:
            status_label.config(text=f"SERA (Mic Error: {e})")
            return


    status_label.config(text="SERA (Recognizing...)")
    try:
        command = recognizer.recognize_google(audio)
        status_label.config(text=f"\n You-{command}")

        reply = respond(command)
        response_box.config(state='normal')
        response_box.insert(tk.END,f"\nRequest....\n{command}\n","you")
        response_box.insert(tk.END, f"Response....\n{reply}\n\n", "sera")
        response_box.config(state='disabled')
        response_box.see(tk.END)
        speak(reply)

    except sr.UnknownValueError:
        status_label.config(text="SERA (Could not understand audio)")
        speak("Sorry, I could not understand that.")

    except sr.RequestError as e:
        status_label.config(text=f"SERA (Speech recognition service error: {e})")
        speak("Sorry, my speech recognition service is not available.")

    except Exception as e:
        status_label.config(text=f"SERA (Error: {e})")
        speak("An error occurred while processing your request.")


def start_listening():
    threading.Thread(target=listen_voice).start()

def on_enter():
    user_input = entry.get()
    if user_input.strip() == "":
        return

    response_box.config(state='normal')
    response_box.insert(tk.END, f"\nRequest....\n{user_input}\n","you")
    response_box.config(state='disabled')
    response_box.see(tk.END)
    response = respond(user_input)
    response_box.config(state='normal')
    response_box.insert(tk.END, f"Response....\n{response}\n\n", "sera")
    response_box.config(state='disabled')
    response_box.see(tk.END)

    speak(response)
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("Smart & Expert Robotics Assistant")
root.state("zoomed")
root.configure(bg="black")
root.resizable(True, False)

canvas = tk.Canvas(root, width=700, height=300, bg="black", highlightthickness=0)
canvas.pack()

status_label = tk.Label(root, text="SERA", fg="white", bg="black", font=("Segoe UI", 18))
status_label.pack(pady=(10, 0))

angle = 0
def draw_ring():
    global angle
    canvas.delete("all")
    center_x, center_y = 350, 150
    radius = 100 + 20 * math.sin(math.radians(angle))

    for i in range(10):
        r = radius + i * 5
        intensity = 255 - i * 20
        color = f'#0000{hex(intensity)[2:].zfill(2)}'
        canvas.create_oval(center_x - r, center_y - r, center_x + r, center_y + r, outline=color, width=2)

    for i in range(100):
        a = math.radians(i * 3.6)
        x = center_x + 40 * math.cos(a)
        y = center_y + 40 * math.sin(a)
        canvas.create_oval(x, y, x + 2, y + 2, fill="#00f", outline="")

    angle = (angle + 4) % 360

draw_ring()

response_frame = tk.Frame(root, bg="black")
response_frame.pack(pady=(10, 5))

response_box = tk.Text(response_frame, wrap=tk.WORD, width=90, height=12, font=("Segoe UI", 14), bg="black", fg="white", relief="flat", borderwidth=0, highlightthickness=0)
response_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
response_box.tag_configure("you", foreground="#0853F5")
response_box.tag_configure("sera",foreground="#F8F9FF")

scrollbar = tk.Scrollbar(response_frame, command=response_box.yview)
response_box.configure(yscrollcommand=scrollbar.set)
scrollbar.pack_forget()

response_box.tag_configure("justify", justify='right')
response_box.insert(tk.END, " \n", "justify")
response_box.config(state='disabled')

def on_mousewheel(event):
    response_box.yview_scroll(int(-1 * (event.delta / 120)), "units")

response_box.bind("<MouseWheel>", on_mousewheel)
response_box.bind("<Button-4>", lambda e: response_box.yview_scroll(-1, "units"))
response_box.bind("<Button-5>", lambda e: response_box.yview_scroll(1, "units"))

frame = tk.Frame(root, bg="black")
frame.pack(pady=5)

entry = tk.Entry(frame, width=40, font=("Segoe UI", 13), bg="#1a1a1a", fg="white", insertbackground="white", relief="flat")
entry.grid(row=0, column=0, padx=10, ipady=6)

mic_btn = tk.Button(frame, text="🎤", bg="#1a1a1a", fg="white", borderwidth=0, font=("Segoe UI", 13), command=start_listening)
mic_btn.grid(row=0, column=1, padx=5)

send_btn = tk.Button(frame, text="🔎", bg="#1a1a1a", fg="white", borderwidth=0, font=("Segoe UI", 13), command=on_enter)
send_btn.grid(row=0, column=2, padx=5)

root.bind('<Return>', lambda event: on_enter())

greeting_message()

speak("Sera is ready to assist you")
root.mainloop()
