# The GaganBot
"""This is a cool playlist convertor and downloader Bot built by Gagan G Saralaya"""
#Build start on 19-7-25 Completed 20-7-25 Time 3:11 am Fuck it's late and I have an exam tomorrow.
import os 
import time
from pytube import Playlist
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Correct paths for WSL environment
chrome_path = "/mnt/c/Users/gagan/chrome-linux64/chrome"
driver_path = "/mnt/c/Users/gagan/chromedriver-linux64/chromedriver"
download_dir="/mnt/c/Users/gagan/Downloads" #songs get downloaded here
chrome_prefs={ "download.default_directory":download_dir,
              "download.prompt_for_download": False,
              "directory_upgrade": True,
              "safebrowsing.enabled": True
}

chrome_options = Options()
chrome_options.binary_location = chrome_path
chrome_options.add_experimental_option("prefs",chrome_prefs)

chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless=new")  # Use GUI? → comment this line

# Start driver
service =Service(executable_path=driver_path)
driver= webdriver.Chrome(service=service, options=chrome_options)
wait=WebDriverWait(driver, 60)  # Wait up to 60 seconds

# Inputs
playlist_url=input("Enter the url of the cool playlist:")
#notepad_name = input("Enter the output text file name (e.g., 'videos.txt'): ").strip()
loveyou="love you"
iloveyou="i love you playlist"
aboutgg="about"
if loveyou in playlist_url or iloveyou in playlist_url:
    time.sleep(0.5)
    print("Awww I love you too my User")
    time.sleep(0.5)
    print("Now type the correct URL:")
    playlist_url=input("Enter the url of the cool playlist:")
elif aboutgg in playlist_url:
    time.sleep(0.5)
    print("The GaganBot\nThis is a cool playlist convertor and downloader Bot built by Gagan G Saralaya\nBuild start on 19-7-25 Completed 20-7-25 Time 3:11 am Fuck it's late and I have an exam tomorrow.")
    time.sleep(0.5)
    print("Now type the correct URL:")
    playlist_url=input("Enter the url of the cool playlist:")


notepad_name = input("Enter the output text file name (e.g., 'videos.txt'): ").strip()
og="og"
if og in notepad_name:
    notepad_name="og.txt"

second_website = "https://amp3.cc/"

if not notepad_name.endswith(".txt"):
    notepad_name += ".txt"
output_path = notepad_name

# Step 1: Extract video URLs
try:
    pl = Playlist(playlist_url)
    urls = pl.video_urls

    if not urls:
        print("✘ No videos found in the playlist.")
    else:
        with open(output_path, 'w') as f:
            for url in urls:
                f.write(url + '\n\n')
        print(f"✓ URLs saved to {output_path}")
except Exception as e:
    print(f"✘ Error extracting playlist: {type(e).__name__}: {e}")
    exit()

# Step 2: Automate Chrome
try:
    with open(output_path, 'r') as f:
        for line in f:
            video_url = line.strip()
            if not video_url:
                continue

            driver.get(second_website)
            print(f"Opened: {second_website}")
            time.sleep(2)

            try:
                # Paste URL
                input_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "input-url"))
                )
                input_box.clear()
                input_box.send_keys(video_url)
                print(f"Pasted URL: {video_url}")

                # Click Convert button
                convert_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "convert-button"))
                )
                time.sleep(1)
                driver.execute_script("arguments[0].click();", convert_button)
                print("Clicked convert button")

                # Wait for progress to complete or convert-another button to appear
                while True:
                    try:
                        converting_visible = "Converting" in driver.page_source
                        percent_text = driver.find_element(By.CLASS_NAME, "progress-percent").text.strip().replace('%', '')
                        if converting_visible and int(percent_text) < 99:
                            time.sleep(1)
                            continue
                    except:
                        pass

                    try:
                        another_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.ID, "convert-another-button"))
                        )
                        another_button.click()
                        print("Clicked 'Convert Another' button\n")
                        break  # Proceed to next URL
                    except TimeoutException:
                        time.sleep(1)  # Retry
            except Exception as inner_e:
                print(f"✘ Error processing URL: {inner_e}")

    driver.quit()
except Exception as e:
    print(f"✘ Selenium Error: {type(e).__name__}: {e}")

