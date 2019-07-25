import urllib.request
import urllib.parse
from urllib.parse import urlparse
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import os, subprocess, threading, sys
from os import rename, listdir

from win32_setctime import setctime
from datetime import datetime 
import time

from PIL import Image
from PIL.ExifTags import TAGS

band_url = "https://band.us/band/9807709"  #영아부
#band_url = "https://band.us/band/73840350"  #유치부
#band_url = "https://band.us/band/69055731" #초등부
#band_url = "https://band.us/band/73840350" #유년부
#band_url = "https://band.us/band/70171406" #고등부

downloadfolder = 'D:\\band\\'
mp4filename = 'BandVideo.mp4'


def download(url, file_name = None):
    if not file_name:
    	file_name = url.split('/')[-1]
    with open(file_name, "wb") as file:   
       	response = requests.get(url)               
       	file.write(response.content)   

def crome_start():
    exteral_chrome = '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"'
    threading._start_new_thread(os.system,(exteral_chrome,))

def change_attribute(path, ttstmp):
    #os.utime('C:\\Users\\User\\Downloads\\BandVideo.mp4',(ttstamp, ttstamp))
    setctime(path, ttstmp)

def frename(path,filetype):   
        basename = filetype
        suffix = time.strftime("%Y%m%d-%H%M%S")
        filename = "_".join([basename, suffix]) +'.'+filetype
        print(filename)

        rename(path,downloadfolder +filename)
		
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def get_filename_from_url(url):
    parts = urlparse(url)
    parts_str = parts.path
    #print(parts_str)

    myindex = parts_str.split('/')
    #print(myindex[len(myindex)-1])
    fname = myindex[len(myindex)-1]
    return fname

def wait4download(path, timeout):
    for i in range(0, timeout):
        if os.path.exists(path) == True:
            break
        else:
            time.sleep(1)


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
    #chrome_driver = 'C:/Users/User/Desktop/py_test/chromedriver.exe'
    chrome_driver = 'C:/Users/anyan/Desktop/py_test/chromedriver.exe'
    driver = webdriver.Chrome(chrome_driver, options = chrome_options)
    driver.implicitly_wait(3)

    driver.get(band_url)
    
    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="lnb"]/ul/li[2]/a/span').click()#사진첩
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/h2/a/strong').click()#전체사진
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/ul/li[1]').click()#사진뷰모드
    time.sleep(3)
    TotalNum = driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div/div/section/div/div[2]/div[1]/div/span')
    print(TotalNum.text)

    for file in os.scandir(downloadfolder):
        if file.name.endswith('.mp4'):
            os.remove(file.path)
            print ("removed " + file.name)



    num = int(TotalNum.text)
    for x in range(1,(num+1)):
        print("--{0}/{1}-- ".format(x,num), end='')
        start = time.time()

        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "optionBox"))        )

        timetag = driver.find_element_by_class_name("time")
        date_tt = timetag.text + ' 12:34:56'
        ttstamp = time.mktime(datetime.strptime(date_tt,'%Y년 %m월 %d일 %H:%M:%S').timetuple())
        #print(ttstamp)

        photoViewer = driver.find_element_by_class_name("photoViewer")
        photoContent = photoViewer.find_element_by_class_name("photoContent")

        optionBox = photoViewer.find_element_by_xpath('//*[@class="optionBox"]/a')
        #optionBox.click()

        try:
            img = photoContent.find_element_by_xpath('//*[@class="mediaWrap _mediaWrap"]/img')

            href = optionBox.get_attribute('href')
            #print(href)
			
            fname = get_filename_from_url(href)

            if os.path.exists(downloadfolder + fname) == False:
                optionBox.click()

            wait4download(downloadfolder + fname, 60)

            change_attribute(downloadfolder + fname , ttstamp)
            print(fname,end='')

        except NoSuchElementException:
            element = WebDriverWait(photoContent, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))        )
			
            video = photoContent.find_element_by_tag_name('video')
            vedio_url = video.get_attribute('src')
            #print(vedio_url)

            fname = get_filename_from_url(vedio_url)

            if os.path.exists(downloadfolder + fname[0:63] + '.mp4') == False:
                optionBox.click()

            wait4download(downloadfolder + mp4filename, 60)

            change_attribute(downloadfolder + mp4filename , ttstamp)
            rename(downloadfolder + mp4filename,downloadfolder + fname[0:63] + '.mp4')
            print(fname[0:63] + '.mp4',end='')

        print("\t\t%.6f sec" %(time.time() - start))
        if x < num:
            photoContent.find_element_by_class_name("btnNext").click()
        





##############################################################################################################################
#여기서부터 시작

if __name__ == "__main__":  
    main()



#####################################################
# sample code
#driver.find_element_by_id("search_btn").click()

#driver.get("https://www.naver.com")
#assert "NAVER" in driver.title

#driver.find_element_by_name("query").clear()
#driver.find_element_by_name("query").send_keys(x)
