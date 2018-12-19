'''
Created on Dec 18, 2018

@author: MYHOMEFOLDER
'''
import base_bot

class InstagramBot(base_bot.SocialMediaBot):
    BASE_URL = 'https://www.instagram.com/'
    
    def __init__(self):
        base_bot.SocialMediaBot.__init__(self)
        self.visited_links = set()
    
    def like_post(self):
        #self.driver.find_element_by_link_text("Like").click()
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button').click()
        base_bot.time.sleep(1)
    
    def follow_user(self):
        follow_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/span[2]/span[1]/button')
        if follow_button.text == 'Follow':
            follow_button.click()
        else:
            print(f"Already following user: {self.website.split('/')[3]}")
    
    def unfollow_user(self):
        follow_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/span[2]/span[1]/button')
        if follow_button.text == 'Following':
            follow_button.click()
            self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[3]/button[1]').click()
        else:
            print(f"You are not following user: {self.website.split('/')[3]}")
    
    def comment(self,message):
        comment_input = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/textarea')
        
        actions = base_bot.webdriver.ActionChains(self.driver).move_to_element(comment_input)
        actions.click()
        actions.send_keys(message)
        #comment_input.click()
        #comment_input.text = message
        comment_input.send_keys(message)
        comment_input.send_keys(base_bot.Keys.RETURN)
    
    
        
    def like_post_by_urls(self,urls):
        for url in urls:
            if url not in self.visited_links:
                self.visited_links.add(url)
                self.driver.get(url) # /p/jkhdkjhk
                self.like_post()
                
    
    def get_post_links(self):
        # find all a tags
        self.driver.get(self.BASE_URL+'explore/tags/underarmour/')
        all_a_tags = self.driver.find_elements_by_tag_name('a')
        all_a_tags = [atag.get_attribute('href') for atag in all_a_tags]
        print('href tags',all_a_tags)
        post_links = filter(lambda x: '/p/' in x, all_a_tags)
        return set(post_links)
    # find all links
    
    

if __name__ == '__main__':
    from getpass import getpass

    try:
        #=======================================================================
        # username = input('Enter username or email: ')
        # show_password = input("You are about to enter your password. Would you like to show password? 'Y' or 'N': ")
        # if show_password == 'Y':
        #     password = input("Enter Password: ")
        # else:
        #     password = getpass()
        #=======================================================================
        
        
        username = 'k1ngbachfan'
        password = '3cf48za3CF48ZA'
        insta_bot = InstagramBot()
        insta_bot.navigate_to(InstagramBot.BASE_URL)
        base_bot.time.sleep(3)
        insta_bot.login(username,password,
                    '//a[@href="/accounts/login/?source=auth_switcher"]',
                    '//input[@name="username"]',
                    '//input[@name="password"]')
        
        
        base_bot.time.sleep(2)
        #insta_bot._like_post('https://www.instagram.com/p/BrjDGBflwqx/')
        #links = insta_bot.get_post_links()
        #insta_bot.like_post_by_urls(links)
        insta_bot.navigate_to('https://www.instagram.com/p/Bri5OpblPxv/')
        insta_bot.like_post()
        insta_bot.comment('sample message')
        base_bot.time.sleep(30)
    finally:
        insta_bot.exit()