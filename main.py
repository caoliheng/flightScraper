# Liheng Cao
# prereqs:
# bs4, selenium (with chrome webdriver), lxml, datetime, time

from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta
import time

from selenium.common.exceptions import NoSuchElementException


def get_URL(day, month=datetime.today().month, year=datetime.today().year, from_='PEK', to_='LGA'):
    # url of flight website with dates, starting and destination points added
    if day < 10:
        day = '0' + str(day)
    if month < 10:
        month = '0' + str(month)
    return "".join(['https://www.google.com/flights?lite=0#flt=',
                    from_, '.',
                    to_, '.',

                    str(year), '-',
                    str(month), '-',
                    str(day),
                    ';c:USD;e:1;sd:1;t:f;tt:o'])


def fp(f, c):
    # return information ready for printing and does 'error checking'
    try:
        return f.find('div', class_=c).decode_contents().strip()
    except AttributeError:
        return 'None'


date = datetime.today()
runs = int(input('How many days to search? (Enter an integer number of days): '))
option = webdriver.ChromeOptions()
option.add_argument('--ignore-certificate-errors')
option.add_argument('--incognito')
option.add_argument('--headless')  # use if you don't want to see chrome window
# set options for web driver

driver = webdriver.Chrome(options=option)
# init web driver


run = 0
while run < runs:
    print('Day', run + 1,':')
    driver.get(get_URL(date.day, date.month, date.year))  # go to website
    time.sleep(2) # haven't added detecting when page is finished loading
    try:  # expand the results by clicking on more
        driver.find_element_by_css_selector("div[class='gws-flights-results__dominated-toggle flt-subhead2 "
                                            "gws-flights-results__collapsed']").click()
        time.sleep(2) # haven't added detecting when page is finished loading
    except NoSuchElementException:  # do nothing if there is no 'more'
        pass

    soup = BeautifulSoup(driver.page_source, 'lxml')
    flight_items = soup.find_all('div',
                                 class_='gws-flights-results__collapsed-itinerary gws-flights-results__itinerary '
                                        'gws-flights-results__itinerary-narrow')
    if len(flight_items) > 0:
        print('Results for', date.strftime('%B-%d'))
        for i, flight in enumerate(flight_items, 1):
            # lists price and duration of flights for this day
            print('Result', i,
                  fp(flight, 'gws-flights-results__price'),
                  fp(flight, 'gws-flights-results__duration')
                  )
    else:
        print('No matching flights for', date.strftime('%B-%d'))
    date += timedelta(days=1)
    run += 1

driver.quit()  # exit and close browser window
