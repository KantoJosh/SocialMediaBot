from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class SocialMediaBot():
    # functionality limited to Chrome currently
    def __init__(self):
        ''' Initiate Chrome WebDriver'''
        self.driver = webdriver.Chrome()
        
    def navigate_to(self,url):
        '''Go to URL. Easier to read than get method'''
        self.driver.get(url)
        self.website = url
        
    def login(self,email,password,login_location,email_xpath,pw_xpath):
        '''Finds login button, logs user in with given information after finding email and password
            fields to fill in'''
                                
        login_init = self.driver.find_element_by_xpath(login_location)
        login_init.click()
        time.sleep(3)
        email_input = self.driver.find_element_by_xpath(email_xpath)
        password_input = self.driver.find_element_by_xpath(pw_xpath)
        
        email_input.send_keys(email)
        password_input.send_keys(password)
        
        password_input.send_keys(Keys.RETURN)
    
    def exit(self):
        '''Closes current browser then closes entire session'''
        # closes current browser
        self.driver.close()
        # closes entire session
        self.driver.quit()
        
            