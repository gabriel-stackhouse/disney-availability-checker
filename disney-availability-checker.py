from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from parks import Parks
import constant
import time
import datetime


def main():
    park_to_check = Parks.HOLLYWOOD_STUDIOS  # todo - use passed-in argument
    driver = build_chrome_driver()
    driver.get(constant.DISNEY_AVAILABILITY_WEBSITE)  # todo - possibly change this to a property
    time.sleep(3)  # todo - change to something better
    navigate_to_date(driver)
    if is_park_available(driver, park_to_check):
        message = park_to_check.pretty_name + " is available on July 4th! Hurry up and reserve it!!!"
        send_pushbullet_alert(message)
        print(message)
    else:
        print(park_to_check.pretty_name + " is not available on July 4th.")


def build_chrome_driver():
    options = Options()
    # options.headless = True   # todo - uncomment
    return webdriver.Chrome(options=options)


def expand_shadow_element(driver, element):
    return driver.execute_script("return arguments[0].shadowRoot", element)


def find_calendar(driver):
    awakening_calendar = expand_shadow_element(driver, driver.find_elements_by_tag_name("awakening-calendar")[0])
    calendar_container = awakening_calendar.find_element_by_id("calendarContainer")
    return calendar_container.find_elements_by_tag_name("wdat-calendar")[0]


def find_park_availabilities(driver):
    awakening_availability = expand_shadow_element(
        driver, driver.find_elements_by_tag_name("awakening-availability-information")[0])
    park_availability_container = awakening_availability.find_element_by_id("parkAvailabilityContainer")
    return park_availability_container.find_elements_by_tag_name("div")


# todo - make this actually navigate to the correct date
def navigate_to_date(driver):
    calendar = find_calendar(driver)
    calendar_nav = expand_shadow_element(driver, calendar)
    if calendar_nav.find_element_by_id("monthHeader").text == "June":
        calendar_nav.find_element_by_id("nextArrow").click()
        time.sleep(1.5)  # todo - change to something better
    date_buttons = calendar.find_elements_by_tag_name("wdat-date")
    for date_button in date_buttons:
        if date_button.get_attribute("slot") == "2021-07-04":
            date_button.click()  # todo - what happens when button isn't clickable?
            time.sleep(1)  # todo - change to something better
            return


def is_park_available(driver, park_to_check):
    park_availabilities = find_park_availabilities(driver)
    for park_availability in park_availabilities:
        park_name = park_availability.find_elements_by_tag_name("span")[0].text
        if park_to_check.pretty_name in park_name:
            return park_availability.get_attribute("class") == "available"
    return False


def send_pushbullet_alert(message):
    # todo - do something
    return


# Start script
if __name__ == "__main__":
    main()

