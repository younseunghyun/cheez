from selenium import webdriver
import unittest

class NewUserTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

        # wait for 3 seconds
        # 셀레늄 테스트에서 기본적인 로직
        # 셀레늄은 페이지 로딩이 끝날때까지 기다리긴 하지만 완벽하진 않음
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_account(self):
        '''

        :return: nothing
        '''

        self.browser.get('http://localhost:8000')

        self.assertIn('Django', self.browser.title)
        self.fail('Finish the test')

        # 가입하기

if __name__ == '__main__':
    unittest.main(warnings='ignore')
