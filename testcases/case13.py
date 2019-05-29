from testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class Case13(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 13

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://ssl.test-canitrust.com/iframe.html")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        webDriver.switch_to.frame(webDriver.find_element_by_tag_name("iframe"))
        iframe_content = webDriver.find_element_by_xpath("/html/body").text
        webDriver.close()

        # If the text in iframe_content is equal to that of the surrounding page, the focus switch
        # into the iframe did not work. This is is the case in some older browsers. This result must
        # be treated as if the content of the iframe was empty.
        if (iframe_content == 'Outside of the iframe!'):
            self.data = {'iframe_content': ''}
        else:
            self.data = {'iframe_content': iframe_content}

        return 1

    def evaluate(self):
        if self.data['iframe_content'] == 'We are in the iframe now!':
          result = 2
        else:
          result = 3

        self.result = result
