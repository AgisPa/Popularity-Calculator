import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



def get_google_titles(query, start_date, end_date):
    url = "https://google.com/search?q="
    query = urllib.parse.quote_plus(query)
    link = url + query



    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": r"C:\Users\cooki\PycharmProjects\Trends",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    options.add_argument('--headless=new')
    
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="W0wltc"]/div'))).click()

    title_list=[]
    incomplete_element=True
    new_scroll=0

    def change_time(start_date,end_date,wait_time):
    
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Change to English")) )
        driver.find_element(By.LINK_TEXT, "Change to English").click()
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nfSF8e"))
        )
        driver.find_element(By.CLASS_NAME, "nfSF8e").click()

        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "KTBKoe"))
        )
        driver.find_element(By.CLASS_NAME, "KTBKoe").click()
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div[5]/div/div/div/span[1]/g-popup/div[2]/g-menu/g-menu-item[7]/div/div/span'))
        )

        utt=driver.find_element(By.XPATH, '/html/body/div[5]/div/div[5]/div/div/div/span[1]/g-popup/div[2]/g-menu/g-menu-item[7]/div/div/span')
        utt.click()
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "OouJcb"))

        )

        end_field = driver.find_element(By.CLASS_NAME, "OouJcb")

        driver.execute_script("arguments[0].click();", end_field)

        driver.execute_script("arguments[0].setAttribute('value','" + str(end_date) + "}')", end_field)

        WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "rzG2be"))

        )

        start_field = driver.find_element(By.CLASS_NAME, "rzG2be")
        driver.execute_script("arguments[0].setAttribute('value','" + str(start_date) + "}')", start_field)

        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="T3kYXe"]/g-button'))

        )
        driver.find_element(By.XPATH, '//*[@id="T3kYXe"]/g-button').click()


    wait_time = 20
    change_time(start_date, end_date, wait_time)

    while incomplete_element and new_scroll<3000:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "h3"))

        )

        headings = driver.find_elements(By.TAG_NAME, "h3")
        heads = set([i.text for i in headings if len(i.text) > 0])
        if len(title_list)==len(headings)-1:
            incomplete_element=False

        else:

            for element in heads:
                if element=='Meer resultaten':
                    incomplete_element=False
                elif title_list.count(element) == 0:
                    title_list.append(element)

        txt= "scroll("+str(new_scroll)+", "+str(100+new_scroll)+")"
        new_scroll += 100
        driver.execute_script(txt)
    driver.quit()
    return title_list





