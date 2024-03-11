import sys
import os
import time 

#Imports Packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import cv2

########################################################################
GECKOPATH = "geckodriver.exe"
parent_dir = "dataset"
search='python logo'
########################################################################

# path 
folderName=search.replace(" ","_")
directory = os.path.join(parent_dir, folderName) 
   
# Create the directory 
try: 
    if not os.path.exists(directory):
        os.makedirs(directory) #os.mkdir(directory)
except OSError as error: 
    print("ERROR : {}".format(error)) 


sys.path.append(GECKOPATH)  
#Opens up web driver and goes to Google Images
browser = webdriver.Firefox()#Firefox(firefox_binary=binary)

#load google image
browser.get('https://www.google.ca/imghp?hl=en')

delay = 10 # seconds
try:
    btnId="L2AGLb"
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID , btnId))) #id info-address-place-wrapper 
    #elm=browser.find_element_by_id(btnId)
    elm=browser.find_element(By.ID,btnId)
    elm.click()
    print("Popup is passed!")
except TimeoutException as e:
    print("Loading took too much time!")

time.sleep(15) #loading

# get and fill search bar
#box = browser.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
#box = browser.find_element(By.XPATH,'//*[@id="sbtc"]/div/div[2]/input')
box = browser.find_element(By.TAG_NAME, "textarea")
box.send_keys(search)
box.send_keys(Keys.ENTER)
print("key enter is pressed")
time.sleep(10) #loading

#Will keep scrolling down the webpage until it cannot scroll no more
last_height = browser.execute_script('return document.body.scrollHeight')
while True:
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(20)
    new_height = browser.execute_script('return document.body.scrollHeight')
    try:
        #browser.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
        browser.find_element(By.XPATH,'//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
        
        time.sleep(10)
    except:
        print("button not found")
        pass
        
    if new_height == last_height:
        break
    last_height = new_height

#find all images on page
imgList=[]
try:
    #imgs = browser.find_elements(By.TAG_NAME, "img")
    #imgs = browser.find_elements(By.CLASS_NAME, "rg_i")
    imgs = browser.find_elements(By.XPATH,"//img[contains(@class,'rg_i')]")
    print("found {} images".format(len(imgs)))
    for i,img in enumerate(imgs):
        #src=img.get_attribute("src") # get source of image
        #urllib.request.urlretrieve(str(src),directory+"\{}.png".format(i)) # download source
        img.screenshot(directory + r'\{}.png'.format(i))
        imgList.append(directory + r'\{}.png'.format(i))
  
except:
    print("imagenot found")
    pass
        
browser.quit()
 
#Test images with OpenCV
for img in imgList:
    try:   
        cv2.imread(img)
    except Exception as e:
        os.remove(img)
        print("remove {}".format(img))