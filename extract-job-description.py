#url	Position	Company	Location	Job_Description
import pandas as pd
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from csv import writer

driver = webdriver.Chrome(executable_path=r'chromedriver.exe')

def geturl(key, location):
    driver.wait = WebDriverWait(driver, 5)
    driver.maximize_window()
    driver.get("https://www.indeed.com/jobs?q={}&l={}".format(key, location))
    url = set()
    while True:
        if len(url)>=30:
            break
        bs = BeautifulSoup(driver.page_source, "lxml")
        
        main = bs.find_all("td",{"class":"resultContent"})
        for m in main:
            url.add('https://www.indeed.com{}'.format(m.find('a')['href']))       
        try:
            next_element = bs.find("a", {"class": "e8ju0x50"})
            try:
                next_exist = next_element.find('a')
            except AttributeError:
                driver.quit()
                break
            except NoSuchElementException:
                driver.quit()
                break
            if next_exist:
    
                driver.find_element_by_class_name("e8ju0x50").click()
                time.sleep(2)
            else:
                driver.quit()
                break
        except ElementClickInterceptedException:
            pass
    return list(url)

listJobGroups = [
["java", "Lubbock"], 
["software developer", "Lubbock"],
["information security", "Lubbock"],
["Nurse", "Lubbock"],
["physician", "Lubbock"],
["data scientist", "Lubbock"],
["financial", "Lubbock"],
["statistician", "Lubbock"],
["accounting", "Lubbock"],
["banking", "Lubbock"],
["IT", "Lubbock"],
["database", "Lubbock"],
["devops", "Lubbock"],
["java", "San Antonio"], 
["software developer", "San Antonio"],
["information security", "San Antonio"],
["Nurse", "San Antonio"],
["physician", "San Antonio"],
["data scientist", "San Antonio"],
["financial", "San Antonio"],
["statistician", "San Antonio"],
["accounting", "San Antonio"],
["banking", "San Antonio"],
["IT", "San Antonio"],
["database", "San Antonio"],
["devops", "San Antonio"]
]

# driver = webdriver.ChromeOptions()
# driver.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(options=driver)
refined_job_list = {}
for jb in listJobGroups:
    listURL = geturl(jb[0], jb[1])
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
    i = 1
    for u in tqdm(listURL):
        driver.wait = WebDriverWait(driver, 5)
        driver.get(u)
        bs = BeautifulSoup(driver.page_source, "lxml")
        try:
            position = bs.find("h1",{"class":"jobsearch-JobInfoHeader-title"}).get_text()
            company = bs.find("div",{"class":"jobsearch-DesktopStickyContainer-companyrating"}).find("a").get_text()
            description = bs.find("div",{"class":"jobsearch-jobDescriptionText"}).get_text()
            location = bs.find("div", {"class": "jobsearch-JobInfoHeader-subtitle"}).find("div").find_next_sibling().get_text()

            # print(position +" "+ company +" " + description+"\n")
            refined_job_list[i] = {
                    'order':[1],
                    'url' :[u],
                    'Position':[position],
                    'Company': [company],
                    'Job_Description' :[description],
                    'Location': [location]
                }

            df = pd.DataFrame(refined_job_list[i])
 
            # append data frame to CSV file
            df.to_csv('jobList.csv', mode='a', index=False, header=False)

        except AttributeError:
            print("ERR: Attri  ")
            pass
        except IndexError:
            print('Err: Out of range')
        except NoSuchElementException:
            print("WARMING: SKIOP")
            pass
        i+=1


driver.quit()
# addJobFrame = pd.DataFrame(refined_job_list)
# jobDes = addJobFrame.transpose()
# jd.to_csv('jobList.csv', )

df1=pd.read_csv("jobList.csv")
print(df1)