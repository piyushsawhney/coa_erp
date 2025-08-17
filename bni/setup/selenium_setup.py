from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()
driver.maximize_window()
