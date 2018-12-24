from base_bot import SocialMediaBot
from collections import namedtuple
import time

class InstagramBot(SocialMediaBot):
    BASE_URL = 'https://www.instagram.com/'
    
    def __init__(self) -> None:
        '''Inherit methods from SocialMediaBot, creates set of visited links, and goes to
        https://www.instagram.com/ '''
        SocialMediaBot.__init__(self)
        self.visited_links = set()
        self.navigate_to(InstagramBot.BASE_URL)
    
        
    def navigate_by_hashtag(self,hashtag: str) -> None:
        '''Goes to Instagram URL given a hashtag '''
        self.navigate_to(InstagramBot.BASE_URL+'explore/tags/'+hashtag)
    
    def navigate_by_username(self,username: str) -> None:
        '''Goes to user's Instagram profile given a username '''
        self.navigate_to(InstagramBot.BASE_URL+username)


    def like_post(self) -> None:
        '''Tries to like post. If it has already been liked, looks for the liked button and notifies user that it has;
            otheriwse, clicks the like button.'''
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button').click()
        try:
            self.driver.find_element_by_xpath('//span[@class="glyphsSpriteHeart__outline__24__grey_9 u-__7"]').click()
        except:
            # like has already been clicked
            self.driver.find_element_by_xpath('//span[@class="glyphsSpriteHeart__filled__24__red_5 u-__7"]')
            print("Picture has already been liked")
        
        
    def unlike_post(self) -> None:
        '''Tries to remove like from post. If it hasn't been liked yet, it notifies the user; otherwise, it clicks the like button to remove it'''
        try:
            self.driver.find_element_by_xpath('//span[@class="glyphsSpriteHeart__filled__24__red_5 u-__7"]').click()
        except:
            self.driver.find_element_by_xpath('//span[@class="glyphsSpriteHeart__outline__24__grey_9 u-__7"]')
            print("Picture already is not liked")
    
    
    def bookmark_post_toggle(self):
        '''Clicks bookmark regardless of bookmark status.FUTURE implementation: add and remove bookmark'''
        self.driver.find_element_by_xpath('//span[@class="wmtNn"]').click()
        
    
    def block_user_toggle(self,profile_url):
        '''Blocks user regardless of block status. FUTURE implemenation: add and remove blocked users '''
        self.navigate_to(profile_url)
        self.driver.find_element_by_xpath('//span[@class="glyphsSpriteMore_horizontal__outline__24__grey_9 u-__7"]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('(//button[@class="aOOlW   HoLwm "])[position()=2]').click()
        time.sleep(4)
        self.driver.find_element_by_xpath('(//button[@class="aOOlW  bIiDR  "])[position()=1]').click()
    
    
    def follow_user(self,url = None) -> None:
        '''Navigates to given URL of Instagram profile then finds follow button and lets the user know of their current follow status.
            If they have yet to follow the user, the follow button is clicked so user at specified URL is followed'''
        
        self.navigate_to(url)
        follow_button = self.driver.find_element_by_xpath(f'//button[text()="{self.following_user_status(url)}"]')
        
        if follow_button.text == 'Follow':
            follow_button.click()
            print(f'You have followed user: {self.website.split("/")[3]}')
        elif follow_button.text == 'Following':
            print(f"Already following user: {self.website.split('/')[3]}")
        elif follow_button.text == 'Requested':
            print(f"Already requested follow from user: {self.website.split('/')[3]} , waiting for confirmation.")

    
    def unfollow_user(self,url=None) -> None:   
        """Navigates to specified URL of Instagram profile then finds follow button and lets the user know of their current follow status.
            If they are following the user the follow button is clicked so that the user a the specified URL is NO LONGER followed """     
        
        self.navigate_to(url)
        follow_button = self.driver.find_element_by_xpath(f'//button[text()="{self.following_user_status(url)}"]')
        
        if follow_button.text == 'Following':
            follow_button.click()
            print(f'You have un-followed user: {self.website.split("/")[3]}')
        elif follow_button.text == 'Requested':
            print(f'You have removed your follow request from user: {self.website.split("/")[3]}')
        elif follow_button.text == 'Follow':
            print(f'You are already not following user: {self.website.split("/")[3]}')
            

    def following_user_status(self,url = None) -> str:
        '''Navigates to URL of user's Instagram profile and detects your follow status of the user (whether you are following or have
            requested a follow. If no status is detected, it raises an AssertionError notifying you that it couldn't get the follow status'''
        self.navigate_to(url)
                
        statuses = ['Requested','Follow','Following']
        for status in statuses:
            try:
                button_text = self.driver.find_element_by_xpath(f'//button[text()="{status}"]').text
            except:
                pass
            else:
                return button_text
        raise AssertionError("Could not get following status for user.")            

    # works
    def comment(self,message,post_url = None) -> None:
        '''Given the URL to an Instagram post, assuming you have permission to access the post, it will
            post your message into the comments'''
        self.navigate_to(post_url)
        time.sleep(1)
        self.driver.find_element_by_xpath('//textarea').click()
        time.sleep(1)
        comment_input = self.driver.find_element_by_xpath('//textarea')
        comment_input.send_keys(message)
        comment_input.send_keys(u'\ue007')
    
                  
    def get_user_stats(self,url = None) -> namedtuple:
        '''Gets user stats of Instagram profile and returns it as a namedtuple, including
            username,post count,follower count, and following count, which can be accessed by their respective names with underscores
            separating words'''
        self.navigate_to(url)
        count = self.driver.find_elements_by_class_name('Y8-fY')

        try:
            # if follower count is exact
            follower_count = int(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title').replace(',',''))
        except:
            follower_count = count[1].text.split()
            follower_count = int(follower_count[0])
        
        User = namedtuple('User', 'username post_count follower_count following_count')
        return User(username = self.website.split("/")[3],
                    post_count = int(count[0].text.split()[0].replace(',','')),
                    follower_count = int(self.driver.find_element_by_xpath('(//span[@class="g47SY "])[position()=2]').text),
                    following_count = int(count[2].text.split()[0].replace(',',''))
                    )
        
    
    def get_suggested_users_all(self) -> None:
        '''Work in progress. Grabs about 10 users Instagram profile URLs from suggested users list. If it can't access the suggested users
            (user may not have one), it prints a message.
            -----------------------------------------------------------------------------------------------------------------------------
            This doesn't raise an error since many Instagram users usually do not have a suggested users list,
            and would be a source of constant errors during scraping of hundreds/thousands of profiles '''
        try:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/span[2]/span[2]').click() # press down button
            time.sleep(3)
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/div[1]/a').click()
            time.sleep(3)
        except:
            print("Could not get suggested users")
            return False
      
        #suggested_user = self.driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/div/div/div[{n}]/div[2]/div[1]/div/a")
        n = 1
        links = set()
        try:
            while True:
                suggested_user = self.driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/div/div/div[{n}]/div[2]/div[1]/div/a")
                links.add(suggested_user.get_attribute('href').split('/')[3])
                n+=1
                #suggested_user = self.driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/div/div/div[{n}]/div[2]/div[1]/div/a")
        except:
            return links
    
    
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
    try:        
        username = 'your username'
        password = 'your password'
        insta_bot = InstagramBot()
        time.sleep(3)
        insta_bot.login(username,password,
                    '//a[@href="/accounts/login/?source=auth_switcher"]',
                    '//input[@name="username"]',
                    '//input[@name="password"]')
        
        
            
    finally:
        insta_bot.exit()