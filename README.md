# selenium-crawling-for-591-website

### Brief
使用selenium爬取591房屋交易網上蘆洲區的新建案資訊，並下載成csv(可調整區域爬取其他地區的新建案資訊)

### import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv