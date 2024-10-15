# import subprocess
import time
import socket

# import pytest
# from selenium import webdriver


# @pytest.fixture(scope="session")
# def driver():
#     # Start the Streamlit application as a separate process
#     app_process = subprocess.Popen(
#         ["streamlit", "run", "../../app.py"]
#         )

#     # Wait for the Streamlit app to start
#     time.sleep(2)

#     driver = webdriver.Chrome()
#     yield driver
#     driver.quit()

#     # Stop the Streamlit application process after the test
#     app_process.terminate()
#     app_process.wait()

# def test_home_title(driver):
#     driver.get("http://localhost:8501")

#     # How to find the streamlit element and then wait for them to being ready?
#     time.sleep(1)

#     assert driver.title == "EduGenius"


import subprocess

from seleniumbase import BaseCase


class PageContentTest(BaseCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app_process = subprocess.Popen(["streamlit", "run", "../../app.py"])

    @classmethod
    def wait_for_streamlit(cls, timeout=30) -> None:
        """Wait for Streamlit to become available on localhost:8501."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Attempt to connect to localhost:8501
                with socket.create_connection(("localhost", 8501), timeout=1):
                    return  # Connection successful, proceed with the tests
            except OSError:
                time.sleep(1)  # Wait a second and try again
        raise RuntimeError("Streamlit app didn't start within the timeout period")


    def test_home_page(self) -> None:
        self.open("http://localhost:8501")
        time.sleep(2)
        self.assert_title("EduGenius")


    @classmethod
    def tearDownClass(cls) -> None:
        cls.app_process.terminate()
        cls.app_process.wait()