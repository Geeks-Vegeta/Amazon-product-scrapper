from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv



options = webdriver.ChromeOptions()
options.add_argument('--headless')

links,names=[],[]
prices,ratings=[],[]
i=1
while i<=20:
    web = f'https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1685007357&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}'

    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.get(web)
    driver.implicitly_wait(5)

    items = wait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "a-section a-spacing-small a-spacing-top-small")]')))
    for item in items:
        link=item.find_elements("xpath",".//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
        name=item.find_elements("xpath",".//span[@class='a-size-medium a-color-base a-text-normal']")
        price=item.find_elements("xpath",".//span[@class='a-price-whole']")
        global_rating=item.find_elements("xpath",".//span[@class='a-size-base s-underline-text']")
        if len(name)!=0: names.append(name[0].text)
        if len(link)!=0: links.append(link[0].get_attribute('href'))
        if len(price)!=0: prices.append(price[0].text)
        if len(global_rating)!=0:ratings.append(global_rating[0].text)

    driver.quit()
    i+=1

x=list(map(list, zip(names, prices, ratings, links)))

# field names
fields = ['Name', 'Prices', 'Ratings', 'Links']

# name of csv file
filename = "part1.csv"
 
# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
     
    # writing the fields
    csvwriter.writerow(fields)
     
    # writing the data rows
    csvwriter.writerows(x)