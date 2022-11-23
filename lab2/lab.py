from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def try_get_element(XPATH, driver, wait):
    while True:
        try:
            inputElement = driver.find_element(By.XPATH, value=XPATH)
            wait.until(EC.element_to_be_clickable(inputElement))
            inputElement.click()
        except:
            continue
        break
    


def main():
    input_data = input("Please write your number:\n")

    url = "https://www.tinkercad.com/things/75eBorf0c9N-copy-of-spi-bus/editel?tenant=circuits"
    
    options = Options()
    options.add_argument("--headless")
    
    #set link to your firefox and drivers
    options.binary_location = r"C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    driver = webdriver.Firefox(executable_path=r"D:\\Projects\\University\\Proectation\\firefox\\geckodriver.exe", options=options)

    #your login and password to this website
    email = ""
    password = ""

    wait = WebDriverWait(driver, 500)

    try:
        driver.get(url=url)
        #login
        time.sleep(5)
        inputElement = driver.find_element(by="id", value="signInPersonalAccounts")
        wait.until(EC.element_to_be_clickable(inputElement))
        inputElement.click()
        inputElement = driver.find_element(by="id", value="autodeskProviderButton")
        wait.until(EC.element_to_be_clickable(inputElement))
        inputElement.click()
        inputElement = driver.find_element(by="id", value="userName")
        wait.until(EC.element_to_be_clickable(inputElement))
        inputElement.send_keys(email)
        wait.until(EC.element_to_be_clickable(inputElement))
        inputElement.send_keys(Keys.ENTER)
        wait.until(EC.element_to_be_clickable(inputElement))
        inputElement = driver.find_element(by="id", value="password")
        wait.until(EC.element_to_be_clickable(inputElement))
        inputElement.send_keys(password)
        wait.until(EC.element_to_be_clickable(inputElement))
        inputElement.send_keys(Keys.ENTER)
        
        print("Successful login")

        #start arduino
        try_get_element("/html/body/div[2]/div/div/div[5]/div[1]/div[1]/div[3]/div[1]/a",driver, wait)
        try_get_element("/html/body/div[2]/div/div/div[5]/div[2]/div[4]/div/div[1]/div[4]/a/div/div[2]/span[2]",driver, wait)
        try_get_element("/html/body/div[2]/div/div/div[5]/div[2]/div[4]/div/div[1]/div[4]/div/ul/li/ul/li[1]",driver, wait)
        try_get_element("/html/body/div[2]/div/div/div[5]/div[2]/div[4]/div/div[5]/div[1]/a/div[2]",driver, wait)

        print("Successful start arduino")

        #input data
        try_get_element("/html/body/div[2]/div/div/div[5]/div[1]/div[1]/div[3]/div[2]/a/div[2]",driver,wait)
        inputElement = driver.find_element(By.XPATH, value="/html/body/div[2]/div/div/div[5]/div[2]/div[4]/div/div[5]/div[2]/div[2]/input")
        wait.until(EC.element_to_be_clickable(inputElement))
        inputElement.send_keys(input_data)
        time.sleep(4)
        inputElement.send_keys(Keys.ENTER)

        print("Successful input")

        #get output arduino
        try_get_element("/html/body/div[2]/div/div/div[5]/div[2]/div[4]/div/div[1]/div[4]/a/div/div[2]/span[2]",driver, wait)
        try_get_element("/html/body/div[2]/div/div/div[5]/div[2]/div[4]/div/div[1]/div[4]/div/ul/li/ul/li[2]",driver, wait)
        inputElement = driver.find_element(By.XPATH, value="/html/body/div[2]/div/div/div[5]/div[2]/div[4]/div/div[5]/div[2]/div[1]/div[1]")
        flag = False
        while True:
            str = inputElement.text
            if str != "":
                for i in str.split('\n'):
                    if int(i) > 0:
                        print("Result:")
                        print(i)
                        flag = True
                        break
            if flag == True:
                break

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


if __name__=="__main__":
    main()