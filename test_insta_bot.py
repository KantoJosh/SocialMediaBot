import unittest
from insta_bot import InstagramBot
import time

class InstaTest(unittest.TestCase):
# #   @classmethod
# #==============================================================================
# #    def setUpClass(cls):
# #        #=======================================================================
# #        # #super(InstaTest, cls).setUpClass()
# #        #=======================================================================
# # 
# #        """Executes setup method before every testing function"""
# #        cls.bot = InstagramBot()
# #        cls.bot.login("testb0t123","G4NEXwYBCwJ66up",
# #                    "//a[@href="/accounts/login/?source=auth_switcher"]",
# #                    "//input[@name="username"]",
# #                    "//input[@name="password"]")
# #        cls.bot.navigate_to(InstagramBot.BASE_URL + "testb0t123/")
# #        time.sleep(2)
# #==============================================================================
    
    def setUp(self):
        self.bot = InstagramBot()
        self.bot.login("testb0t123","G4NEXwYBCwJ66up",
                    "//a[@href='/accounts/login/?source=auth_switcher']",
                    "//input[@name='username']",
                    "//input[@name='password']")
        time.sleep(5)
        

    def test_user_stats(self):
        """Tests user stats including username, post count, follower count,
        and following count """
        self.bot.navigate_to(InstagramBot.BASE_URL + "testb0t123/")
        user_stats = self.bot.get_user_stats()
        self.assertEqual(user_stats.post_count, 0)
        self.assertEqual(user_stats.follower_count,1)
        self.assertEqual(user_stats.following_count,9)
        
    
    def test_follow_user(self):
        """Tests user follow method of InstagramBot by checking if it raises an error, and then prints the error message"""
        try:
            self.bot.follow_user("https://www.instagram.com/nintendo/")
        except Exception as e:
            self.fail(e)

        time.sleep(2)
    
    
    def test_unfollow_user(self):
        """Tests unfollow user method of InstagramBot by checking if it raises an error, and then prints the error message"""
        try:
            self.bot.unfollow_user("https://www.instagram.com/nintendo")
        except Exception as e:
            self.fail(e)
        
        time.sleep(2)

    def test_like_post(self):
        self.bot.navigate_to("https://www.instagram.com/p/Bt321diA5R5/")
        self.assertEqual(self.bot.like_post(),None) # assert that like post returns None and doesn't crash

    def test_unlike_post(self):
        self.bot.navigate_to("https://www.instagram.com/p/Bt321diA5R5/")
        self.assertEqual(self.bot.unlike_post(),None)   # assert that unlike post returns None and doesn't crash
    
    def tearDown(self):
        """Quits"""
        self.bot.driver.quit()
    
    
    #===========================================================================
    # @classmethod
    # def tearDownClass(cls):
    #     # close the browser window
    #     cls.bot.driver.quit()
    #===========================================================================
    
    
if __name__ == "__main__":
    unittest.main()
        
        