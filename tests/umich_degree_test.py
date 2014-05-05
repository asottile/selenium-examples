import getpass

import testify as T
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from testing.selenium_util import with_driver


class TestUmich(T.TestCase):
    """Test that a student has graduated from umich with a CS degree."""

    @T.setup
    def get_umich_login(self):
        self.username = getpass.getpass('Username:')
        self.password = getpass.getpass('Password:')

    def switch_to_content_frame(self, driver):
        content_frame = driver.find_element_by_id('ptifrmtgtframe')
        driver.switch_to_frame(content_frame)

    @with_driver(DesiredCapabilities.FIREFOX)
    def test_my_degree(self, driver):
        driver.get('https://wolverineaccess.umich.edu')

        # Students tab
        driver.find_element_by_css_selector('[title=Students]').click()

        # Student Business
        driver.find_elements_by_css_selector('.gatewayLinkList a')[0].click()

        # Type username and password
        driver.find_element_by_id('login').send_keys(self.username)
        driver.find_element_by_id('password').send_keys(self.password)
        driver.find_element_by_id('loginSubmit').click()

        # Ugh wolverineaccess why do you use frames
        self.switch_to_content_frame(driver)

        # And ugly selectors :'(
        driver.find_element_by_xpath(
            '//*[text() = "View Unofficial Transcript"]'
        ).click()

        # frames :(
        self.switch_to_content_frame(driver)
        driver.find_element_by_id('GO').click()

        # Select an element to make sure we're on the transcript page
        driver.find_element_by_xpath(
            '//*[contains(text(), "UNOFFICIAL TRANSCRIPT")]'
        )

        # Assert I got my degree!
        table_contents = ' '.join(
            driver.find_element_by_id('ACE_width').text.split()
        )
        T.assert_in('MAJOR: Computer Science', table_contents)
        T.assert_in('DEGREE: Bachelor of Science', table_contents)
