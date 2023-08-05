import time

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from . import util


def send_keys(driver, event):
	if wait(driver, event):
		element = util.get_element(driver, event['target'])
		v = event['value'].encode('ascii', 'ignore').decode("utf-8")
		element.send_keys(v)


def submit(driver, event):
	if wait(driver, event):
		element = util.get_element(driver, event['target'])
		element.submit()


def click(driver, event):
	if wait(driver, event):
		element = util.get_element(driver, event['target'])
		action = ActionChains(driver)
		action.move_to_element(element)
		action.click(element)
		action.perform()


def hover(driver, event):
	if wait(driver, event):
		element = util.get_element(driver, event['target'])
		action = ActionChains(driver)
		action.move_to_element(element)
		action.perform()


def get(driver, event):
	driver.get(event['target'])


def wait(driver, event):
	"""
	Wait for an element to appear
	:param driver:
	:param event:
	:return:
	"""
	try:
		if event['type'] == 'click':
			WebDriverWait(driver, 16).until(ec.element_to_be_clickable((By.CSS_SELECTOR, event['target'])))
		else:
			WebDriverWait(driver, 16).until(ec.presence_of_element_located((By.CSS_SELECTOR, event['target'])))
	except TimeoutException as e:
		if 'required' in event and not event['required']:
			return False
		else:
			raise e
	return True


def sleep(driver, event):
	time.sleep(event['value'])


def switch_to(driver, event):
	scroll_to(driver, event)
	element = util.get_element(driver, event['target'])
	driver.switch_to.frame(element)


def scroll_to(driver, event):
	driver.execute_script('arguments[0].scrollIntoView(true);', util.get_element(driver, event['target']))
