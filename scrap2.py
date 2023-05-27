from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
import re
from helper import getManuAndAsin
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_argument('--headless')

links,names=[],[]
prices,ratings=[],[]
descriptions, asins=[],[]
manufacturers, product_description=[],[]
i=1

while i<=15:
    web = f'https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1685007357&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}'
    
    try:

        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        driver.get(web)
        driver.implicitly_wait(1)
        items = wait(driver, 1).until(EC.presence_of_all_elements_located(("xpath", '//div[@class="a-section a-spacing-small a-spacing-top-small"]')))
        for item in items:
            link=item.find_elements("xpath",".//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
            if len(link)!=0: 
                try:
                    driver2 = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
                    links.append(link[0].get_attribute('href'))
                    driver2.get(link[0].get_attribute('href'))
                    driver2.implicitly_wait(1)
                    name=wait(driver2, 1).until(EC.presence_of_all_elements_located(("xpath","//h1[@id='title']")))
                    rating=driver2.find_element("xpath","//span[@class='a-size-base a-color-base']")
                    price=driver2.find_element("xpath","//span[@class='a-price-whole']")
                    get_asin=driver2.find_elements("xpath","//div[@id='detailBullets_feature_div']")
                    description=driver2.find_element("xpath","//span[@class='a-list-item']")
                    p_desc=driver2.find_elements("xpath","//span[@class='a-text-italic']")
                    if p_desc!=[]:
                        product_description.append(p_desc[0].text)
                    else:
                        product_description.append("")
                    if len(get_asin)!=0:
                        asinx=get_asin[0].text.split('\n')
                        d=re.split('[\n:]',get_asin[0].text.strip())
                        c=getManuAndAsin(d)
                        if c is None:
                            manufacturers.append("")
                            asins.append("")
                        else:
                            manufacturers.append(c[1])
                            asins.append(c[0])
                    names.append(name[0].text)
                    descriptions.append(description.text)
                    ratings.append(rating.text)
                    prices.append(price.text)
                    driver2.close()
                except TimeoutException:
                    driver2.close()
        driver.close()
    except TimeoutException:
        driver.close()
    i+=1

x=list(map(list, zip(names, prices, ratings, links, asins, manufacturers, descriptions,product_description)))

# field names
fields = ['Name', 'Prices', 'Ratings', 'Links','ASIN','Manufacturer', 'Descriptions', "Product Descriptions"]

# name of csv file
filename = "part21.csv"
 
# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
     
    # writing the fields
    csvwriter.writerow(fields)
     
    # writing the data rows
    csvwriter.writerows(x)
