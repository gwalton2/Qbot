from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as selexcep
import custom_wait_condition as cw
import time
import push
import json
import os
import sys

options = webdriver.ChromeOptions()

#local location of vpn extension for run machine
options.add_argument(r'load-extension=C:\Users\walto\AppData\Local\Google\Chrome\User Data\Default\Extensions\fgddmllnllkalaagkghckoinaemmogpe\5.0.0.4150_0')

options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--window-size=1920,1080')
#options.add_argument('--headless')
driver = webdriver.Chrome(r'chromedriver_win32\chromedriver.exe', chrome_options=options)

MAIN_URL = "https://www.quora.com"
USERNAME = ""
PASSWORD = ""

PUSH_ID = '9h2innb8u3w4it0ufcn6tk87e0iq6wnfc0d03ul7cl5tsns3qf1gajjmvcs3w441'

ASKED_QUESTIONS = 0
FAILED_QUESTIONS = 0
FAILED_RECOMMENDATIONS = 0
FAILED_TOPICS = 0
QUESTIONS = []
FALIED_Q = []

def post(filename, num):
	global QUESTIONS

	QUESTIONS = open(filename, "r", encoding="utf-8").readlines()
	start = time.time()

	for q in QUESTIONS[:num]:
		try:
			ask_question(q)
			update_json()

		except Exception as e:
			print(e)
			print(f'Major error encountered on question: "{q}"\n')
			time.sleep(10)

	end = time.time()

	save(num, filename)

	push.send(f"{USERNAME}: {FAILED_QUESTIONS} failed qs, {FAILED_TOPICS} failed ts, {FAILED_RECOMMENDATIONS} failed rs", PUSH_ID)
	push.send(f"{USERNAME}: Completed in {end - start}", PUSH_ID)
	#push.send(f"{USERNAME}: Earnings", PUSH_ID, body=get_earnings())

def ask_question(question):
	global ASKED_QUESTIONS
	global FAILED_QUESTIONS
	global FAILED_RECOMMENDATIONS
	global FAILED_TOPICS

	driver.get(MAIN_URL)
	try:
		ask(question)
		ASKED_QUESTIONS += 1

	except Exception as e:
		print(e)
		print(f'Failed question: "{question}"\n')
		FAILED_QUESTIONS += 1

		failed_question(question)
		return

	try:
		topics()

	except Exception as e:
		print(e)
		print(f'Problem with topics for question: "{question}"\n')
		FAILED_TOPICS += 1
		return
		
	try:
		recommendations()

	except Exception as e:
		print(e)
		print(f'Problem with recommendations for question: "{question}"\n')
		FAILED_RECOMMENDATIONS += 1

def failed_question(question):
	global QUESTIONS
	global FALIED_Q

	failed_ind = QUESTIONS.index(question)
	FALIED_Q.append(QUESTIONS.pop(failed_ind))

def ask(question):
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'puppeteer_test_add_question_button'))).click() #clicks Add Question or Link button
	WebDriverWait(driver, 5).until(cw.unhidden_element_located((By.TAG_NAME, 'textarea'))).send_keys(question) #types question into text box
	try:
		add_button = WebDriverWait(driver, 5).until(cw.unhidden_element_located((By.CLASS_NAME, 'puppeteer_test_modal_submit'))).click() #clicks Add Question button
	except selexcep.ElementClickInterceptedException as e:  #catches weird error where it tries to click on disabled submit button but still clicks on right button. Hopefully doesnt end up passing on important webdriverexception errors
		print('Passed on ElementClickInterceptedException')
		pass

	timeout = time.time() + 10
	while time.time() < timeout:
		try:
			#topics located
			WebDriverWait(driver, 1).until(cw.unhidden_element_located((By.XPATH, "//*[text()='Edit Topics']")))
			return
		except Exception as e:
			pass

		try:
			#ignore edit
			WebDriverWait(driver, 1).until(cw.unhidden_element_located((By.XPATH, "//*[text()='Double-check your question']")))
			WebDriverWait(driver, 1).until(cw.unhidden_element_located((By.CLASS_NAME, 'puppeteer_test_modal_cancel'))).click()
		except Exception as e:
			pass

		try:
			#question duplicate override
			WebDriverWait(driver, 1).until(cw.unhidden_element_located((By.XPATH, "//*[text()='Was your question already asked?']")))
			WebDriverWait(driver, 1).until(cw.unhidden_element_located((By.CLASS_NAME, 'puppeteer_test_modal_submit'))).click()
		except Exception as e:
			pass

	raise Exception

def topics():
	topics = WebDriverWait(driver, 5).until(cw.unhidden_elements_located((By.XPATH, "//input[@type='checkbox']"))) #unchecked topics

	for t in topics:
		if(t.get_attribute('checked') != 'true'):
			t.location_once_scrolled_into_view
			ActionChains(driver).click(t).perform()

	WebDriverWait(driver, 5).until(cw.unhidden_element_located((By.CLASS_NAME, 'puppeteer_test_modal_submit'))).click() #clicks Done button

def recommendations():
	elements = WebDriverWait(driver, 5).until(cw.unhidden_elements_located((By.XPATH, "//span[@name='CirclePlus']")))

	for elem in elements[:5]:
		try:
			elem.location_once_scrolled_into_view
			ActionChains(driver).click(elem).perform()
		except Exception as e:
			print(e)

	WebDriverWait(driver, 5).until(cw.unhidden_element_located((By.CLASS_NAME, 'puppeteer_test_modal_submit'))).click()

def open_quora():
	driver.get(MAIN_URL)

	login_forms = WebDriverWait(driver, 5).until(cw.unhidden_elements_located((By.CLASS_NAME, 'q-input')))
	login_forms[0].send_keys(USERNAME)
	login_forms[1].send_keys(PASSWORD)

	login_button = WebDriverWait(driver, 5).until(cw.unhidden_elements_located((By.XPATH, "//button")))
	login_button[1].click()

def get_earnings():
	"""
	driver.get(MAIN_URL)
	time.sleep(5)
	driver.get(MAIN_URL + '/partners')

	earnings = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'earnings_section')))
	labels = earnings.find_elements_by_class_name('label')
	data = earnings.find_elements_by_class_name('data')

	message = ''
	for l, d in zip(labels, data):
		message += f'{l.text}: {d.text}\n'

	return message
	"""
	return "get_earnings under development"

def save(num, q_filename):
	new_q = QUESTIONS[num:]
	new_a = QUESTIONS[:num]

	q_file = open(q_filename, "w", encoding = "utf-8")
	a_file = open('used_files/asked.txt', "a", encoding = "utf-8")
	f_file = open('used_files/failed.txt', "a", encoding = "utf-8")

	for q in new_q:
		q_file.write(q)

	for a in new_a:
		a_file.write(a)

	for f in FALIED_Q:
		f_file.write(f)

	q_file.close()
	a_file.close()
	f_file.close()

def initiate_json():
	data = {'AQ': 0, 'FQ': 0, 'FT': 0, 'FR': 0}

	with open(USERNAME + '.json', 'w', encoding='utf-8') as file:
		json.dump(data, file, indent=4)

def finish_json():
	with open(USERNAME + '.json', 'r', encoding = 'utf-8') as file:
		data = json.load(file)

		data['AQ'] = '/'
		data['FQ'] = '/'
		data['FT'] = '/'
		data['FR'] = '/'

	with open(USERNAME + '.json', 'w', encoding = 'utf-8') as file:
		json.dump(data, file, indent=4)


def update_json():
	with open(USERNAME + '.json', 'r', encoding = 'utf-8') as file:
		data = json.load(file)

		data['AQ'] = ASKED_QUESTIONS
		data['FQ'] = FAILED_QUESTIONS
		data['FT'] = FAILED_TOPICS
		data['FR'] = FAILED_RECOMMENDATIONS

	with open(USERNAME + '.json', 'w', encoding = 'utf-8') as file:
		json.dump(data, file, indent=4)

def sync(last_ques):
	last_ques = last_ques + '\n'

	ques_list = open('answers_ordered.txt', 'r', encoding = 'utf-8').readlines()
	ind = ques_list.index(last_ques)
	print(ind)

	save(ques_list, ind + 1, 'answers_ordered.txt', 'asked.txt')


if __name__ == '__main__':
	USERNAME = sys.argv[1]
	PASSWORD = sys.argv[2]

	filename = sys.argv[3]
	ques_num = sys.argv[4]

	initiate_json()
	open_quora()
	time.sleep(5)
	
	post('ques_files/' + filename, int(ques_num))
	finish_json()
	