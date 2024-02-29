import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_forex_rate(date, currency_code):
    # 设置ChromeDriver路径
    chrome_driver_path = "D:/aaaaa/chrome/chrome-win64/chrome-win64/chromedriver.exe"  # 修改为你的ChromeDriver路径

    # 设置ChromeDriver选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    chrome_service = Service(chrome_driver_path)

    # 初始化WebDriver
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        # 打开中国银行外汇牌价网站
        driver.get("https://www.boc.cn/sourcedb/whpj/")

        # 等待日期输入框加载完成
        date_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "nothing"))
        )

        # 输入日期
        date_input.clear()
        date_input.send_keys(date)

        # 点击查询按钮
        print("Finding query button...")
        query_button = driver.find_element(By.XPATH, "//input[@type='button']")
        print("Query button found.")

        # 点击查询按钮
        query_button.click()

        # 等待表格加载完成
        print("Waiting for table to load...")
        table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//table[@align='left']"))
        )
        print("Table loaded.")

        # 获取货币行情信息
        currency_rows = table.find_elements(By.XPATH, "//tr[@class='odd']")
        forex_rate = None
        for row in currency_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 8 and cells[0].text == currency_code:
                forex_rate = cells[3].text
                break
        else:
            raise ValueError("指定日期没有找到该货币的行情信息")

        # 将结果写入文件
        with open("result.txt", "w") as f:
            f.write(f"Date: {date}\n")
            f.write(f"Currency Code: {currency_code}\n")
            f.write(f"Forex Rate: {forex_rate}\n")

        print("Writing result to file...")

        return forex_rate

    finally:
        # 关闭WebDriver
        print("Closing WebDriver...")
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 yourcode.py <date> <currency_code>")
        sys.exit(1)

    date = sys.argv[1]
    currency_code = sys.argv[2]

    try:
        forex_rate = get_forex_rate(date, currency_code)
        print(f"Forex Rate: {forex_rate}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
