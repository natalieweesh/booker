import config
import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

'''
This is a python script you can run a couple minutes before 12pm a week before the impossible-to-book-classpass-class you want so that you have a fighting chance to book it. It will ask for the studio you want and the start time of the class you want. Start the script a minute or two before 12pm so it has time to log in and load the studio page before clicking reserve.
'''

#the most impossible to book studios
STUDIOS = {"cityrow": "cityrow-new-york", 
					 "tonehouse": "tone-house-new-york",
					 "brooklynbodyburn": "brooklyn-bodyburn-cobble-hill",
					 "modo": "modo-yoga-nyc-west-village-new-york",
					 "mkc": "mkc-new-york",
					 "throwback": "throwback-fitness-new-york",
					 "uplift": "uplift-studios-new-york",
					 "swerve": "swerve-fitness-flatiron-new-york",
					 "peloton": "peloton-chelsea-new-york"}

def nao(): #what time is it?
	return datetime.datetime.now()

def timestamp(text): #print with timestamp
	print text + " {}".format(nao())

print "Which studio do you want to book?"
print "studio suggestions: {}".format(STUDIOS.keys())
selectedStudio = raw_input("Which one?\n")
selectedStudioUrl = STUDIOS[selectedStudio]
selectedTime = raw_input("What start time? (e.g. \"9:30 am\" or \"12:00 pm\")\n")
print "Okay"

driver = webdriver.Firefox()
driver.set_window_size(1080, 1920)

#login
driver.get("http://classpass.com/login")
timestamp("Loaded classpass.com")
usernameInput = driver.find_element_by_id("email_field")
usernameInput.send_keys(config.credentials["username"])
passwordInput = driver.find_element_by_id("password_field")
passwordInput.send_keys(config.credentials["password"])
passwordInput.submit()

try:
	#wait until dashboard loads
	WebDriverWait(driver, 30).until(EC.title_contains("ClassPass | Dashboard"))
	timestamp("Logged in")
except:
	timestamp("Failed to login")

#load studio page
driver.get("http://classpass.com/studios/{}".format(selectedStudioUrl))

#wait until 12pm
t = datetime.datetime.now()
while t.hour < 12:
	time.sleep(1)
	t = datetime.datetime.now()
	timestamp("Wait for it...")

#might have to refresh before clicking the next button...not sure yet

#click next week button
nextWeekButton = driver.find_element_by_css_selector("li.next-week a")
nextWeekButton.click()
#make sure it loaded the next week
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.prev-week a")))

theCorrectButtonSelector = "li[data-start-time='{}'] a.reserve".format(selectedTime)
driver.execute_script("$(\"{}\").click();".format(theCorrectButtonSelector))
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#submit")))
driver.execute_script("$('input#submit').click()")
#donezo

driver.quit
