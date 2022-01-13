from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement
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
            except Exception:
                self.execute_script("window.scrollBy(0, 3000)")
                hotel_name = deal_box.find_element(By.CLASS_NAME, 'PropertyCard__HotelName').get_attribute(
                    'innerHTML').strip()
                print(hotel_name)
            hotel_names.append(hotel_name)
        return hotel_names

    def pull_prices(self):
        prices = []
        for deal_box in self.deal_boxes:
            price_tag = deal_box.find_element(By.CLASS_NAME, 'PropertyCardPrice__Value').get_attribute('innerHTML').strip()
            print(price_tag)
            prices.append(price_tag)
        return prices

    def review_score(self):
        review_scores = []
        for deal_box in self.deal_boxes:
            try:
                score = deal_box.find_element(By.CLASS_NAME, 'Hkrzy').get_attribute('innerHTML').strip()
                print(score)
                review_scores.append(score)
            except Exception:
                review_scores.append("NA")
        return review_scores