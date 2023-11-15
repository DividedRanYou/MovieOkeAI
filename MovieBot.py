# Import libs
import os
import platform
import webbrowser
import time as MovieDelay

# Create a clear function.
def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Create an installer function
def installer():
    try:
        if platform.system() == "Windows":
            os.system("py -m ensurepip --upgrade")
            os.system("py get-pip.py")
        else:
            os.system("python3 -m ensurepip --upgrade")
            os.system("pip install --upgrade pip")
            os.system("pip3 install --upgrade pip")
        os.system("pip uninstall -r Requirements.txt") # this is so when it pip installs it will install the latest version
        os.system("pip3 uninstall -r Requirements.txt") # in case pip itself doesn't work it will try pip3
        os.system("pip install -r Requirements.txt") # now it installs
        os.system("pip3 install -r Requirements.txt") # if attempt one fails it tries it with pip3
        clear() # now it cleans up the screen
    except Exception as e:
        print("Hmm something went wrong, you either have no internet or a security setting is blocking me ):")

# Create a function to download the latest mode and check which mode we're on.
def CheckMode():
    pass

# Now import EVERYTHING
try:
    import requests
    import openai
except ImportError:
    installer()

# Define the API stuff
# API requests still seem to work, i think the site is still being used and is up just all content gone.
API_URL = ""
API_KEY = ""
HEADERS = {
    ""
}

# Define the user agent for MovieBot
user_agent = '''
MovieBot/1 CFNetwork/1402.0.8 Darwin/22.2.0
'''

# OpenAI stuff
model = "text-davinci-002" # GPT 3.5
OPENAI_API_KEY = ""

# Unity stuff
UNITY_API_URL = ""
UNITY_API_KEY = ""

# Eleven Labs stuff
ELEVEN_LABS_API_KEY = ""

# Appetize stuff
APPETIZE_API_VERSION = "v2"
APPETIZE_API_URL = f"" # don't think this is needed...
APPETIZE_API_KEY = ""

# Create a function to check the API stats of MovieBot.
def CheckStatus():
    user_agent = "MovieBot/1 CFNetwork/1402.0.8 Darwin/22.2.0"
    API_URL = "https://static.movieoke.app/app/features.json"
    API_KEY = ""
    
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    response = requests.get(API_URL, API_KEY, headers=HEADERS)
    if response.status_code == 200:
        print("Connection to the MovieBot API was successful.\nStatus code: 200")
    else:
        print(f"Failed to connect to the MovieBot API.\nStatus code: {response.status_code}")

# Create a function to check if the storage backend is up.
def CheckModels():
    response = requests.get("https://example.com")
    if response.status_code == 200:
        print("Backend storage is up and running!")
    else:
        print("Backend storage is currently down.\nPlease try again later.")

# Create a function that checks EVERYTHING.
# This will check the MovieBot stats, API stats for each service used, and validate if each API key, URL and anything else is valid.
def CheckEverything():
    pass

# Create a function to open the API URL.
def OpenURL():
    webbrowser.open_new_tab("https://static.movieoke.app/app/features.json")

# Create a function to print API URLs.
def PrintAPIURLs():
    print('''
          https://static.movieoke.app/app/features.json (primary one)
          https://static.movieoke.app/app/ (access to this url is private)
          https://moviebot.io/ (this is just the old website for moviebot but it was used to make some api requests with the app)
          ''')

# Create a function to generate an animation via the MovieBot API, if we can rebuild it.
def GenerateAnimation():
    pass

# Create a function to sync a mouth, voice, using GPT-4 and DALLE.
def SyncVoice():
    pass

# Create a function to exit.
def ExitHandler():
    MovieDelay.sleep(1)
    clear()
    exit()

# this python file is pretty much just made for Oke.py to define a bunch of shit like functions and classes and variables
if __name__ == "__main__":
    ExitHandler()
