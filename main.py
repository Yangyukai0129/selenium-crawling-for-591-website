from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

# 設定Chrome Driver的執行檔路徑
options = Options()
options.chrome_executable_path=r"C:\Users\beir6\AppData\Local\Programs\Python\Python310\chromedriver.exe"
driver = webdriver.Chrome(options=options)
driver.get('https://www.591.com.tw/')
page_source = driver.page_source

# 獲取網頁數據
data = []

try:
    # 等待彈跳框出現
    tag  = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "area-box-body")))

    tag.click()
    print("Alert is closed")

except TimeoutException:
    # 如果超時，說明没有彈跳框
    print("There is no alert in the page")

# 點擊新建案連結（使用 JavaScript）
new_building = driver.find_element(By.LINK_TEXT,"新建案")
driver.execute_script("arguments[0].click();", new_building)

try:
    pop = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "close")))
    pop.click()
    print("popup is closed")

except TimeoutException:
    # 如果超時，說明没有彈跳框
    print("There is no popup in the page")

# 等待直到類名為 "areasBox" 的元素可見到
try:
    # 找到 id 為 "areasBox" 的 div 元素
    areas_box = driver.find_element(By.ID, "areasBox")

    # 使用 ActionChains 模擬鼠標懸停操作
    actions = ActionChains(driver)
    actions.move_to_element(areas_box).perform()

    # 等待一段时间，以確保子菜單加載完成
    time.sleep(1)
    # 在 areas_box 中找到所有縣市的連接
    city_links = areas_box.find_elements(By.XPATH, ".//a")
    
    # 循環變例連結元素，找到文本内容為 "新北市" 的連結元素
    for link in city_links:
        if link.text == "新北市":
            new_taipei_link = link
            # 点击新北市的链接
            new_taipei_link.click()
            print("New Taipei is clicked")

except NoSuchElementException:
    print("Element not found. Check if the XPath is correct.")
except TimeoutException:
    print("Timeout waiting for areasBox element")
except Exception as e:
    print("Error:", e)

# 等待直到類名為 "villagesBox" 的元素可見到
try:
    # 找到 id 為 "villagesBox" 的 div 元素
    village_box = driver.find_element(By.ID, "villagesBox")

    # 使用 ActionChains 模擬鼠標懸停操作
    actions = ActionChains(driver)
    actions.move_to_element(village_box).perform()

    # 等待一段时间，以確保子菜單加載完成
    time.sleep(2)
    
    # 在 village_box 中找到所有區的複選框元素
    # 定位到複選框
    checkbox_element = driver.find_element(By.XPATH, "//input[@type='checkbox' and @name='villages' and @value='47']")

    # 判斷複選框是否已經被勾選，如果没有，則勾選它
    if not checkbox_element.is_selected():
        checkbox_element.click()
        print("Luzhou is been clicked")

except NoSuchElementException:
    print("Element not found. Check if the XPath is correct.")
except TimeoutException:
    print("Timeout waiting for village_box element")
except Exception as e:
    print("Error:", e)

# 定位到按钮
button_element = driver.find_element(By.CLASS_NAME,"searchBtn11")

# 點擊按钮
button_element.click()

# 定位到按钮
button_expand = driver.find_element(By.CLASS_NAME,"newhouse-arrow-bottom")

# 點擊按钮
button_expand.click()

try:
    # 使用 find_elements 方法獲取所有的子元素
    filter_item_options = driver.find_elements(By.CLASS_NAME, "filter-item-option")

    # 遍歷每個子元素
    for option in filter_item_options:
        # 獲取複選框文本内容
        checkbox_texts = option.find_elements(By.CLASS_NAME, "t5-checkbox__text")
        for checkbox in checkbox_texts:
            # 如果文本内容為 "蘆洲區"，則定位到相應的複選框元素並點擊
            if checkbox.text == "蘆洲區":
                # 使用 JavaScript 来點擊複選框
                driver.execute_script("arguments[0].click();", checkbox)
                print("Luzhou district checkbox is clicked")
except NoSuchElementException:
    print("Luzhou district checkbox not found")
except Exception as e:
    print("Error:", e)

# time.sleep(3)
# 向下滾動到頁面底部
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 等待按钮加载完成
wait_time = 3

try:
    while True:
        searchMore = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".load-more .btn"))
        )
        if searchMore:
            actions = ActionChains(driver)
            actions.move_to_element(searchMore).click().perform()
except TimeoutException:
    print("No more '查看更多建案' button found. Exiting loop.")
except Exception as e:
    print("Error1:", e)
    

try:
    card_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card-item"))
    )

    # 變歷每個 card-item 元素
    for card_item in card_items:
        # 獲取建案名稱
        build_name_element = card_item.find_element(By.CLASS_NAME, "build-name")
        name_element = build_name_element.find_element(By.TAG_NAME, "span")
        name = name_element.text
        data.append(name) 

        # 獲取地址
        build_address_element = card_item.find_element(By.CLASS_NAME, "build-address")
        address_elements = build_address_element.find_elements(By.TAG_NAME, "span")
        address = " ".join([element.text for element in address_elements])
        data.append(address)

    # 嘗試獲取建案的坪數訊息
        try:
            # 获取建案坪數信息
            build_room_element = card_item.find_element(By.CLASS_NAME, "build-room")
            room_elements = build_room_element.find_elements(By.TAG_NAME, "span")
            room_text = " ".join([element.text for element in room_elements])
            # 将提取的文本添加到数据列表中
            data.append(room_text)
        except NoSuchElementException:
            # 如果找不到建案坪數信息，将 "N/A" 添加到数据列表中
            data.append("N/A")

        # 獲取價錢&單位
        build_other_element = card_item.find_element(By.CLASS_NAME, "build-other")
        price_elements = build_other_element.find_element(By.TAG_NAME, "span")
        unit_elements = build_other_element.find_element(By.CLASS_NAME, "unite")
        price = price_elements.text
        unit = unit_elements.text
        data.append(price)
        data.append(unit)

        # 是否銷完
        try:
            build_finished_element = card_item.find_element(By.CLASS_NAME,"icon-slod-out")
            if build_finished_element:
                data.append("Y")
        except:
            data.append("N")

except NoSuchElementException:
    print("No name. HTML:", card_item.get_attribute('outerHTML'))
except Exception as e:
    print("Error2:", e)


# 保存數據為 CSV 文件
csv_filename = "蘆洲新成屋建案.csv"
csv_header = ["建案名稱","地址","坪數","價錢","單位","是否完銷"]

try:
    with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_header)
        for i in range(0, len(data), 6):  # 每个建案名稱和地址訊息的索引是間隔為5的
            writer.writerow([data[i], data[i + 1], data[i + 2], data[i + 3], data[i + 4], data[i + 5]])
    print(f"building name is saved in {csv_filename}")
except Exception as e:
    print("Error3:", e)

driver.quit()
