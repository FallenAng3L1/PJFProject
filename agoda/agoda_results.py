from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement
import selenium.common.exceptions as ex
import agoda.constants as const
class AgodaReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()


    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.CLASS_NAME, 'PropertyCardItem')

    def pull_titles(self):
        hotel_names = []
        for deal_box in self.deal_boxes:
            try:
                hotel_name = deal_box.find_element(By.CLASS_NAME, 'PropertyCard__HotelName').get_attribute('innerHTML').strip()
                print(hotel_name)
            except ex.NoSuchElementException:
                hotel_name = deal_box.find_element(By.CLASS_NAME, 'PropertyCard__HotelName').get_attribute('innerHTML').strip()
            hotel_names.append(hotel_name)
        const.hotel_names_all += hotel_names

    def pull_prices(self):
        prices = []
        for deal_box in self.deal_boxes:
            price_tag = deal_box.find_element(By.CLASS_NAME, 'PropertyCardPrice__Value').get_attribute('innerHTML').strip()
            prices.append(price_tag)
        const.hotel_prices_all += prices

    def review_score(self):
        review_scores = []
        for deal_box in self.deal_boxes:
            try:
                score = deal_box.find_element(By.CLASS_NAME, 'Hkrzy').get_attribute('innerHTML').strip()
                review_scores.append(score)
            except Exception:
                review_scores.append("NA")
        const.hotel_rating_all += review_scores
