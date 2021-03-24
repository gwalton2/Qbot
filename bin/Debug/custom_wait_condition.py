import selenium.common.exceptions as selexcep

class unhidden_element_located(object):
	#custom wait condition for question textbox. Works by waiting until the unhidden version is visible and returns it.
	#The unhidden version is detected by the x coordinate not being returned as 0

	def __init__(self, locator):
		self.locator = locator

	def __call__(self, driver):
		elements = driver.find_elements(*self.locator)

		for elem in elements:
			if elem.location['x'] != 0:
				return elem
				
		return False


class unhidden_elements_located(object):
	#custom wait condition. Works by waiting until the unhidden version is visible and returns it.
	#The unhidden version is detected by the x coordinate not being returned as 0

	def __init__(self, locator):
		self.locator = locator

	def __call__(self, driver):
		elements = driver.find_elements(*self.locator)

		for elem in elements:
			if elem.location['x'] == 0:
				elements.remove(elem)
		
		if len(elements) > 0:
			return elements
		return False

class interactable_elements_located(object): #NEEDS FIXING
	#custom wait conditionWorks by waiting until it finds a fresh element(not stale) and returns it.
	#The unhidden version is detected by using a try/catch block to weed out stale element references.

	def __init__(self, locator):
		self.locator = locator

	def __call__(self, driver):
		elements = driver.find_elements(*self.locator)

		for elem in elements[10:]:
			try:
				elem.click() #Test to trigger stale element exception or any other problems with interacting

			except Exception as e:
				elements.remove(elem)
		
		if len(elements) > 0:
			return elements
		return False
