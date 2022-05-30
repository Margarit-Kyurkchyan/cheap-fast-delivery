from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def ubereats(driver, address, name, queue):
    driver.get('https://www.ubereats.com/')
    search = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'location-typeahead-home-input')))
    # search.send_keys("Detroit, MI")
    search.send_keys(address)
    time.sleep(1.5)
    search.send_keys(Keys.RETURN)
    button = driver.find_element_by_xpath("//button[contains(text(),'Find Food')]")
    button.click()
    # findRestoran = driver.find_element_by_id('search-suggestions-typeahead-input')
    findRestoran = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'search-suggestions-typeahead-input')))
    # findRestoran.send_keys("Detroit City Coney Island")
    findRestoran.send_keys(name)
    findRestoran.send_keys(Keys.RETURN)
    time.sleep(3.5)
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'search-suggestions-typeahead-input')))
    try:
        findPrice = driver.find_element_by_xpath(
            '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/span/div').text
        findDist = driver.find_element_by_xpath(
            '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/span/div').text
        queue['ubereats'] = {'Price': findPrice, 'Distance': findDist}
    except:
        try:
            findPrice = driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div/main/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/span[2]').text
            findDist = driver.find_element_by_xpath(
                '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div[2]/span/div').text
            queue['ubereats'] = {'Price': findPrice, 'Distance': findDist}
        except:
            queue['ubereats'] = driver.find_element_by_xpath(
            '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/span/div').text


def doordash(driver, address, name, queue):
    driver.get("https://www.doordash.com/")
    search = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input')))
    search.send_keys(address)
    time.sleep(3)
    search.send_keys(Keys.RETURN)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                    '/html/body/div[1]/div[1]/div[1]/header/div[1]/div[2]/div[1]/div/div/div/div/div/div/div/div[2]/input')))
    driver.get('https://www.doordash.com/search/store/' + name + '?event_type=search')
    try:
        findPrice = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[1]/div[1]/main/div/div[1]/div/div[3]/div[1]/div/div/div[1]/div/div[2]/a/div/div[4]/div[2]/span').text
        findDist = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[1]/div[1]/main/div/div[1]/div/div[3]/div[1]/div/div/div[1]/div/div[2]/a/div/div[3]/div[2]/div/span').text
        queue['doordash'] = {'Price': findPrice, 'Distance': findDist}
    except:
        queue['doordash'] = "no result"
