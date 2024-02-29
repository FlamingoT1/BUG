# 导入所需的库
import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service

# 定义一个函数，根据货币代号返回对应的中文名称
def get_currency_name(code):
    # 使用一个字典来存储货币代号和名称的对应关系
    currency_dict = {
        "GBP": "英镑",
        "HKD": "港币",
        "USD": "美元",
        "CHF": "瑞士法郎",
        "DEM": "德国马克",
        "FRF": "法国法郎",
        "SGD": "新加坡元",
        "SEK": "瑞典克朗",
        "DKK": "丹麦克朗",
        "NOK": "挪威克朗",
        "JPY": "日元",
        "CAD": "加拿大元",
        "AUD": "澳大利亚元",
        "EUR": "欧元",
        "MOP": "澳门元",
        "PHP": "菲律宾比索",
        "THB": "泰国铢",
        "NZD": "新西兰元",
        "KRW": "韩元",
        "RUB": "卢布",
        "MYR": "林吉特",
        "TWD": "新台币",
        "ESP": "西班牙比塞塔",
        "ITL": "意大利里拉",
        "NLG": "荷兰盾",
        "BEF": "比利时法郎",
        "FIM": "芬兰马克",
        "INR": "印度卢比",
        "IDR": "印尼卢比",
        "BRL": "巴西里亚尔",
        "AED": "阿联酋迪拉姆",
        "ZAR": "南非兰特",
        "SAR": "沙特里亚尔",
        "TRY": "土耳其里拉"
    }
    # 如果字典中有该代号，返回对应的名称，否则返回None
    return currency_dict.get(code, None)

# 获取命令行参数，第一个参数是日期，第二个参数是货币代号
date = sys.argv[1]
code = sys.argv[2]

# 检查参数是否合法，日期格式应为yyyy-mm-dd，货币代号应为三个大写字母
if not date or not code:
    print("请输入日期和货币代号")
    sys.exit(1)
if len(date) != 10 or date[4] != "-" or date[7] != "-":
    print("日期格式应为yyyy-mm-dd")
    sys.exit(1)
if len(code) != 3 or not code.isupper():
    print("货币代号应为三个大写字母")
    sys.exit(1)

# 根据货币代号获取对应的中文名称
name = get_currency_name(code)
if not name:
    print("无法识别的货币代号")
    sys.exit(1)

# 创建一个Service对象，并指定chromedriver的路径
service = Service("D:\\aaaaa\\chrome\\chrome-win64\\chrome-win64\\chromedriver.exe")

# 创建一个webdriver对象，使用service参数
driver = webdriver.Chrome(service=service)

# 打开中国银行外汇牌价网站
driver.get("https://www.boc.cn/sourcedb/whpj/")

# 找到时间输入框，清空原有内容，输入指定的日期
time_input = driver.find_element(By.XPATH, "//*[@id='historysearchform']/div/table/tbody/tr/td[4]/div/input")
time_input.clear()
time_input.send_keys(date)

# 找到货币选择框，根据货币代号选择下拉列表中的选项
currency_select = Select(driver.find_element(By.XPATH, "//*[@id='pjname']"))
currency_select.select_by_value(code)

# 找到搜索按钮，点击搜索
search_button = driver.find_element(By.XPATH, "//*[@id='historysearchform']/div/table/tbody/tr/td[7]/input")
search_button.click()

# 等待页面加载完成，找到表格元素，使用pandas读取表格数据
driver.implicitly_wait(10)
table = driver.find_element(By.ID, "DefaultMain")
data = pd.read_html(table.get_attribute("outerHTML"))[0]

# 关闭浏览器
driver.quit()

# 检查数据是否为空，如果为空，说明没有找到指定日期和货币的数据
if data.empty:
    print("没有找到指定日期和货币的数据")
    sys.exit(1)

# 从数据中获取第一行第四列的值，即现汇卖出价
price = data.iloc[0, 3]

# 打印结果到屏幕
print(price)

# 将结果写入到result.txt文件中
with open("result.txt", "w") as f:
    f.write(str(price))
