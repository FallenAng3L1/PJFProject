from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import datetime
from datetime import date
import time as t
import agoda.constants as const
from agoda.agoda_results import AgodaReport
from selenium.webdriver.common.keys import Keys





class Agoda(webdriver.Chrome):
    def __init__(self, teardown = False):
        self.teardown = teardown
        super(Agoda, self).__init__()
        self.implicitly_wait(const.sleep_val)
        self.maximize_window()
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def accept_popup(self):
        self.implicitly_wait(const.sleep_val)
        accept_button = self.find_element(By.CLASS_NAME, 'ab-close-button')
        accept_button.click()

    def select_place(self, place_to_go):
        search_field = self.find_element(By.CSS_SELECTOR, 'input[data-selenium="textInput"]')
        search_field.send_keys(place_to_go)
        first_result = self.find_element(By.CSS_SELECTOR, f'li[data-text="{place_to_go}"]')
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        today = date.today()
        check_in_parsed = datetime.strptime(check_in_date, '%a %b %d %Y')
        check_out_parsed = datetime.strptime(check_out_date, '%a %b %d %Y')
        num_months = (today.year - check_in_parsed.year) * 12 + (today.month - check_in_parsed.month)
        if num_months >= 2:
            for i in range(1, num_months):
                right_calendar = self.find_element(By.CSS_SELECTOR, 'span[data-selenium="calendar-next-month-button"]')
                right_calendar.click()
        check_in_element = self.find_element(By.CSS_SELECTOR, f'div[aria-label="{check_in_date}"]')
        check_in_element.click()
        num_months = (check_out_parsed.year - check_in_parsed.year) * 12 + (
                    check_out_parsed.month - check_in_parsed.month)
        if num_months >= 1:
            for i in range(0, num_months):
                right_calendar = self.find_element(By.CSS_SELECTOR, 'span[data-selenium="calendar-next-month-button"]')
                right_calendar.click()
        check_out_element = self.find_element(By.CSS_SELECTOR, f'div[aria-label="{check_out_date}"]')
        check_out_element.click()

    def select_guests(self, type, rooms=1, adults=1, minors=1):
        match type:
            case 1:
                selected_type = self.find_element(By.CSS_SELECTOR, 'div[data-element-name="traveler-solo"]')
                selected_type.click()
            case 2:
                selected_type = self.find_element(By.CSS_SELECTOR, 'div[data-element-name="traveler-couples"]')
                selected_type.click()
            case 3:
                selected_type = self.find_element(By.CSS_SELECTOR, 'div[data-element-name="traveler-families"]')
                selected_type.click()
                decrease = self.find_elements(By.CSS_SELECTOR, 'span[data-selenium="minus"]')
                increase = self.find_elements(By.CSS_SELECTOR, 'span[data-selenium="plus"]')
                for i in range(1, rooms):
                    increase[0].click()
                decrease[1].click()
                for i in range(rooms, adults):
                    increase[1].click()
                for i in range(0, minors):
                    increase[2].click()
                    if minors > 0:
                        select_age_all = self.find_elements(By.CLASS_NAME, 'childAges')
                        for select_age in select_age_all:
                            age = select_age.find_element(By.CSS_SELECTOR, 'select[data-selenium="dropdownInput"]')
                            insert_age = Select(age)
                            insert_age.select_by_value("9")
            case 4:
                selected_type = self.find_element(By.CSS_SELECTOR, 'div[data-element-name="traveler-group"]')
                selected_type.click()
                decrease = self.find_elements(By.CSS_SELECTOR, 'span[data-selenium="minus"]')
                increase = self.find_elements(By.CSS_SELECTOR, 'span[data-selenium="plus"]')
                for i in range(1, rooms):
                    increase[0].click()
                decrease[1].click()
                for i in range(rooms, adults):
                    increase[1].click()
                for i in range(0, minors):
                    increase[2].click()
                    if minors > 0:
                        select_age_all = self.find_elements(By.CLASS_NAME, 'childAges')
                        for select_age in select_age_all:
                            age = select_age.find_element(By.CSS_SELECTOR, 'select[data-selenium="dropdownInput"]')
                            insert_age = Select(age)
                            insert_age.select_by_value("9")
            case 5:
                selected_type = self.find_element(By.CSS_SELECTOR, 'div[data-element-name="traveler-business"]')
                selected_type.click()
                decrease = self.find_elements(By.CSS_SELECTOR, 'span[data-selenium="minus"]')
                increase = self.find_elements(By.CSS_SELECTOR, 'span[data-selenium="plus"]')
                for i in range(1, rooms):
                    increase[0].click()
                decrease[1].click()
                for i in range(rooms, adults):
                    increase[1].click()

    def search_click(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[data-element-name="search-button"]')
        search_button.click()

    def scroll_down(self):
        self.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
        t.sleep(const.sleep_val)
        y = const.scroll_value
        new_height = 0
        last_height = self.execute_script("return document.body.scrollHeight")
        while True:
            self.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += const.scroll_value

            t.sleep(const.sleep_scroll_val)
            if y >= last_height:
                break
            last_height = self.execute_script("return document.body.scrollHeight")

    def report_results(self):
        hotel_boxes = self.find_element(By.ID, 'contentContainer')
        report = AgodaReport(hotel_boxes)
        report.pull_titles()
        report.pull_prices()
        report.review_score()


    def next_page(self):
        next_page_button = self.find_element(By.ID, 'paginationNext')
        next_page_button.click()

