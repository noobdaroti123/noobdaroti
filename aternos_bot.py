import discord
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

# Aternos credentials (log in manually at least once to avoid CAPTCHA)
ATERNOS_EMAIL = 'reyonbiju2011@gmail.com'
ATERNOS_PASSWORD = 'lifestealserver@gonnabehard'

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Function to start the server using Selenium
def start_aternos_server():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run headlessly to avoid opening a browser window
    driver = webdriver.Chrome(options=options)

    driver.get('https://aternos.org/login/')
    sleep(2)  # Wait for the page to load

    driver.find_element(By.ID, 'login-email').send_keys(ATERNOS_EMAIL)
    driver.find_element(By.ID, 'login-password').send_keys(ATERNOS_PASSWORD)
    driver.find_element(By.CLASS_NAME, 'login-submit').click()

    sleep(5)  # Wait for login to complete

    driver.get('https://aternos.org/servers/LifesStealsSmp.aternos.me')  # Replace with your server's URL
    sleep(5)

    start_button = driver.find_element(By.XPATH, '//*[text()="Start"]')  # Adjust XPath if needed
    start_button.click()

    sleep(2)
    driver.quit()

# Function to check if the server is online
def check_aternos_server_status():
    try:
        response = requests.get('https://aternos.org/server-status/')  # Adjust to check server status
        if 'offline' in response.text.lower():
            return False
        else:
            return True
    except Exception as e:
        print(f"Error checking status: {e}")
        return False

# Event to trigger when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    while True:
        if not check_aternos_server_status():
            print("Server is offline. Starting it...")
            start_aternos_server()
        sleep(60)  # Check every minute

# Run the bot
bot.run('your_discord_bot_token')
