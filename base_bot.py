from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# future ideas
#----------------
#   1.Plot graph of my followers over time. Write the date and my follower count to a text file and 
#       make a graph from it
#   2.


class SocialMediaBot():
    # functionality limited to Chrome currently
    def __init__(self):
        ''' Initiate Chrome WebDriver'''
        # run headless
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(chrome_options=options)
        #self.driver.maximize_window()
        

    def navigate_to(self,url):
        
        if url != None and url != self.driver.current_url:
            self.website = url
            self.driver.get(url)
            time.sleep(1)
        else:
            print(f"Already at {self.driver.current_url}")


    def login(self,email,password,login_location,email_xpath,pw_xpath):
        """Finds login button, logs user in with given information after finding email and password
            fields to fill in"""
                                
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
        
            