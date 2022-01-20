from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import datetime
from datetime import date
import time as t
import agoda.constants as const
from agoda.agoda_results import AgodaReport
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class Agoda(webdriver.Chrome):
    def __init__(self, teardown = False):
        self.teardown = teardown
        super(Agoda, self).__init__()
        self.implicitly_wait(const.sleep_val)
        self.maximize_window()

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
        num_months = (today.year - check_in_parsed.year) * 12 + abs(today.month - check_in_parsed.month)
        if num_months >= 2:
            for i in range(1, num_months):
                right_calendar = self.find_element(By.CSS_SELECTOR, 'span[data-selenium="calendar-next-month-button"]')
                right_calendar.click()
        check_in_element = self.find_element(By.CSS_SELECTOR, f'div[aria-label="{check_in_date}"]')
        check_in_element.click()
        num_months = (check_out_parsed.year - check_in_parsed.year) * 12 + abs(
                    check_out_parsed.month - check_in_parsed.month)
        if num_months >= 1:
            for i in range(0, num_months):
                right_calendar = self.find_element(By.CSS_SELECTOR, 'span[data-selenium="calendar-next-month-button"]')
                right_calendar.click()
        check_out_element = self.find_element(By.CSS_SELECTOR, f'div[aria-label="{check_out_date}"]')
        check_out_element.click()

    def select_guests(self, type_r, rooms=1, adults=1, minors=1, minors_age=None):
        if minors_age is None:
            minors_age = [9]
        match type_r:
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
                    age_set = 0
                    for select_age in select_age_all:
                        age = select_age.find_element(By.CSS_SELECTOR, 'select[data-selenium="dropdownInput"]')
                        insert_age = Select(age)
                        insert_age.select_by_value(f"{minors_age[age_set]}")
                        age_set += 1
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
                    age_set = 0
                    for select_age in select_age_all:
                        age = select_age.find_element(By.CSS_SELECTOR, 'select[data-selenium="dropdownInput"]')
                        insert_age = Select(age)
                        insert_age.select_by_value(f"{minors_age[age_set]}")
                        age_set += 1
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

    def scroll_properties(self, properties=None):
        if properties is None:
            properties = ["Śniadanie"]
        breakfast = []
        for prop in range(len(properties)):
            breakfast.append([])
            if const.properties_set == len(properties): continue
            else: breakfast[prop].append(properties[prop])

        self.implicitly_wait(0.3)
        reviev_exists = []
        self.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
        if_skipped = False
        t.sleep(1)
        boxes = self.find_elements(By.CLASS_NAME, 'PropertyCardItem')
        for deal_box in boxes:
            actions = ActionChains(self)
            try:
                pill = deal_box.find_element(By.CLASS_NAME, 'Pills')
                t.sleep(0.1)
                actions.move_to_element(pill).perform()
                if not if_skipped:
                    try:
                        skip = self.find_elements(By.CLASS_NAME, 'BackToTop--btn')
                        skip[1].click()
                        if_skipped = True
                    except:
                        pass
                actions.move_to_element(pill).perform()
                reviev_exists.append(1)
            except Exception:
                reviev_exists.append(0)
            t.sleep(0.2)


        tooltips = self.find_elements(By.CLASS_NAME, 'PillTooltip')

        for prop in range(len(properties)):
            i = 0
            for review in reviev_exists:
                if review == 0:
                    breakfast[prop].append(0)
                else:
                    text = tooltips[i].get_attribute('innerHTML').strip()
                    i += 1
                    breakfast[prop].append(1) if text.find(f"{properties[prop]}") > -1 else breakfast[prop].append(0)

        const.hotel_properties_all += breakfast
