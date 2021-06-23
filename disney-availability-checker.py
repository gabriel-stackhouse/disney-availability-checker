from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from parks import Park
import constant
import time
import argparse


def main():
    args = parse_and_validate_arguments()
    driver = build_chrome_driver()
    driver.get(constant.DISNEY_AVAILABILITY_WEBSITE)  # todo - possibly change this to a property
    time.sleep(3)  # todo - change to something better
    navigate_to_date(driver, args.date)
    date_string = args.date.strftime("%b %#d")
    if is_park_available(driver, args.park):
        message = args.park.value + " is available on " + date_string + "! Hurry up and reserve it!!!"
        send_pushbullet_alert(message)
        print(message)
    else:
        print(args.park.value + " is not available on " + date_string + ".")


def parse_and_validate_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("park",
                        type=Park,
                        choices=list(Park),
                        help="the Disney park to check for availability")
    parser.add_argument("date",
                        type=lambda s: datetime.strptime(s, '%m-%d-%Y').date(),
                        help="date to check for availability, in format MM-dd-yyyy")
    args = parser.parse_args()
    if args.date < date.today():
        print("Date is in the past, dummy!")
        exit(1)
    elif args.date > date.today() + relativedelta(years=1):
        print("Script only supports checking availability for a year and under")
        exit(1)
    return args


def build_chrome_driver():
    options = Options()
    # options.headless = True   # todo - uncomment
    options.add_argument("--log-level=3")
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
def navigate_to_date(driver, date_to_check):
    calendar = find_calendar(driver)
    calendar_nav = expand_shadow_element(driver, calendar)
    month_header = calendar_nav.find_element_by_id("monthHeader")
    while month_header.text != date_to_check.strftime("%B"):
        calendar_nav.find_element_by_id("nextArrow").click()
        time.sleep(2)  # todo - change to something better
    date_buttons = calendar.find_elements_by_tag_name("wdat-date")
    for date_button in date_buttons:
        if date_button.get_attribute("slot") == date_to_check.isoformat():
            date_button.click()  # todo - what happens when button isn't clickable?
            time.sleep(1)  # todo - change to something better
            return


def is_park_available(driver, park_to_check):
    park_availabilities = find_park_availabilities(driver)
    for park_availability in park_availabilities:
        park_name = park_availability.find_elements_by_tag_name("span")[0].text
        if park_to_check.value in park_name:
            return park_availability.get_attribute("class") == "available"
    return False


def send_pushbullet_alert(message):
    # todo - do something
    return


# Start script
if __name__ == "__main__":
    main()

