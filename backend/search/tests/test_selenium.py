import socket

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@override_settings(ALLOWED_HOSTS=['*'])  # Disable ALLOW_HOSTS
class BaseTestCase(StaticLiveServerTestCase):
    """
    Provides base test class which connects to the Docker
    container running Selenium.
    """
    host = '0.0.0.0'  # Bind to 0.0.0.0 to allow external access

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set host to externally accessible web server address
        cls.host = socket.gethostbyname(socket.gethostname())

        # Instantiate the remote WebDriver
        cls.selenium = webdriver.Remote(
            #  Set to: htttp://{selenium-container-name}:port/wd/hub
            #  In our example, the container is named `selenium`
            #  and runs on port 4444
            command_executor='http://0.0.0.0:4444/wd/hub',
            # Set to CHROME since we are using the Chrome container
            desired_capabilities=DesiredCapabilities.FIREFOX,

        )
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
