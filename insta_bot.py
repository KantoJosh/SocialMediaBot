'''
Created on Dec 18, 2018

@author: MYHOMEFOLDER
'''
import base_bot
from collections import namedtuple

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
        try:
            # public profile
            follow_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/span[2]/span[1]/button')
            message = f"Already following user: {self.website.split('/')[3]}"
        except:
            # private profile
            try:
                follow_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/button')
                message = f"Already requested follow from user: {self.website.split('/')[3]} , waiting for confirmation."
            except:
                print(f'Could not follow user: {self.website.split("/")[3]}')
                return
        
        #print('text',follow_button.text)
        if follow_button.text == 'Follow':
            follow_button.click()
            print(f'You have followed user: {self.website.split("/")[3]}')
        else:
            print(message)

    
    def unfollow_user(self):
        try:
            follow_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/span[2]/span[1]/button')
        except:
            try:
                follow_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/button')
            except:
                print(f'Could not unfollow user: {self.website.split("/")[3]} ')
                return
        
        print('text',follow_button.text)
        if follow_button.text == 'Following' or follow_button.text == 'Requested':
            follow_button.click()
            self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[3]/button[1]').click()
            print(f'Unfollowed user: {self.website.split("/")[3]}')
        else:
            print(f"You are already not following user: {self.website.split('/')[3]}")
    
    
    def comment(self,message):
        comment_input = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/textarea')
        
        actions = base_bot.webdriver.ActionChains(self.driver).move_to_element(comment_input)
        #actions.click()
        actions.send_keys(message)
        #comment_input.click()
        #comment_input.text = message
        #comment_input.send_keys(message)
        comment_input.send_keys(base_bot.Keys.RETURN)
    
    def get_post_count(self):
        count = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text
        print(f'{self.website.split("/")[3]} has {count} posts')
        return count
    
    def get_follower_count(self):
        count = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/span/span').text
        print(f'{self.website.split("/")[3]} has {count} followers')    
        return count                                                    
    
    def get_following_count(self):
        count = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/span/span').text
        print(f'{self.website.split("/")[3]} is following {count} other users')
        return count    
    
    def get_user_stats(self):
        count = self.driver.find_elements_by_class_name('Y8-fY')
        print('-'*20)
        print(f'User info for {self.website.split("/")[3]}:')
        print(count[0].text)
        print(count[1].text) ### 37.7m followers. to get 37.7, int(count[1].text.split()[0][:-1])
        print(count[2].text)
        print('-'*20)
        #print(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title'))
        
        User = namedtuple('User', 'post_count follower_count following_count')
        return User(post_count = int(count[0].text.split()[0].replace(',','')),
                    follower_count = int(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title').replace(',','')),
                    following_count = int(count[2].text.split()[0].replace(',',''))
                    )

    def get_suggested_users(self):
        suggested_users = self.driver.find_elements_by_class_name('nOA-W _2dbep qNELH kIKUG')
        return [elem.get_attribute('href') for elem in suggested_users]
    
    def get_suggested_users_all(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/span[2]/span[2]').click() # press down button
        base_bot.time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/div[1]/a').click()
        base_bot.time.sleep(3)
        
        n = 1
        #suggested_user = self.driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/div/div/div[{n}]/div[2]/div[1]/div/a")
        
        links = set()
        try:
            while True:
                suggested_user = self.driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/div/div/div[{n}]/div[2]/div[1]/div/a")
                links.add(suggested_user.get_attribute('href').split('/')[3])
                n+=1
                #suggested_user = self.driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/div/div/div[{n}]/div[2]/div[1]/div/a")
        except:
            return links
    
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
        
        
        username = 'testb0t123'
        password = 'testb0t1234'
        insta_bot = InstagramBot()
        insta_bot.navigate_to(InstagramBot.BASE_URL)
        base_bot.time.sleep(3)
        insta_bot.login(username,password,
                    '//a[@href="/accounts/login/?source=auth_switcher"]',
                    '//input[@name="username"]',
                    '//input[@name="password"]')
        
        
        base_bot.time.sleep(2)

        insta_bot.navigate_to('https://www.instagram.com/iamcardib/')
        
        x = insta_bot.get_user_stats()
        print(x.post_count,'/',x.follower_count,'/',x.following_count)
        print(insta_bot.get_suggested_users_all())
        
        #base_bot.time.sleep(5)
        #insta_bot.follow_user()
        #base_bot.time.sleep(5)
        #insta_bot.unfollow_user()
        #base_bot.time.sleep(5)

    finally:
        insta_bot.exit()