from selenium import webdriver
from seleniumwire import webdriver
import time
from selenium.webdriver.common.by import By
import json
import jsonpath
from seleniumwire.utils import decode
import sys
from selenium.webdriver.edge.service import Service





while True:
    try:
        print("===正在尝试模拟登陆===")
        uesr_name = input("===输入B站账号：")
        pass_word = input("===输入登录密码：")
        print("===开始尝试登录，请手动通过图形验证码和手机验证===")
        time.sleep(2)
        service = Service(executable_path=r'MicrosoftWebDriver.exe')  # 修改为您的实际路径
        driver1 = webdriver.Edge(service=service)
        driver1.implicitly_wait(5)
        url_login = "https://account.bilibili.com/login"
        driver1.get(url=url_login)
        driver1.find_element(By.XPATH,'//*[@id="app-main"]/div/div[2]/div[3]/div[2]/div[1]/div[1]/input').send_keys(uesr_name)
        driver1.find_element(By.XPATH,'//*[@id="app-main"]/div/div[2]/div[3]/div[2]/div[1]/div[3]/input').send_keys(pass_word)
        driver1.find_element(By.XPATH,'//*[@id="app-main"]/div/div[2]/div[3]/div[2]/div[2]/div[2]').click()
        input("===确保登陆成功后按回车键继续：")
        try:
            driver1.get('https://space.bilibili.com/')
            driver1.find_element(By.XPATH, '//*[@id="app-main"]/div/div[2]/div[3]/div[2]/div[2]/div[2]')
            input("===未检测到登录，请按回车键重试：")
            driver1.quit()
        except:
            try:
                driver1.get('https://www.bilibili.com/')
                cookies = driver1.get_cookies()
                print("===cookies已获取，登陆环境模拟已完成===")
                break
            except:
                input('===获取cookies失败，请按回车键重试')
    except :
        print("===发生错误，请检查网络，浏览器，以及本程序文件完整性===")
        print('===程序正常关闭，请完成检查后重启===')
        sys.exit()


print(cookies)


def comment():
    video_adress = input('输入BV号')
    # driver1 = webdriver.Edge()
    # driver1.get('https://www.bilibili.com/')
    # for cookie in cookies:
    #     driver1.add_cookie(cookie)
    driver1.get(f'https://bilibili.com/video/{video_adress}/')
    time.sleep(5)
    driver1.refresh()
    time.sleep(5)
    driver1.implicitly_wait(5)

    print('===等待初始化===')
    time.sleep(5)

    driver1.implicitly_wait(1)
    times_1 = 1
    while True:
        try:
            shadow_host = driver1.find_element(By.XPATH, '//*[@id="commentapp"]/bili-comments')
            shadow_root = driver1.execute_script("return arguments[0].shadowRoot", shadow_host)
            shadow_root.find_element(By.CSS_SELECTOR, "#end")
            break
        except:
            times_1 = times_1 + 1
            js = "window.scrollTo(0,document.body.scrollHeight)"
            driver1.execute_script(js)
            print(f"===第{times_1}页加载成功===")
    driver1.implicitly_wait(5)

    # 获取网络请求
    requests_list = driver1.requests

    prefix = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid='
    filtered_urls_1 = [request.url for request in requests_list if request.url.startswith(prefix)]
    filtered_urls = filtered_urls_1[1:]

    i = 1
    comment_list = []
    for url in filtered_urls:
        for request in requests_list:
            if request.url == url:
                try:
                    body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                    json_data = json.loads(body.decode('utf-8'))
                    uid = jsonpath.jsonpath(json_data, "$.data.replies..member.mid")
                    user_name = jsonpath.jsonpath(json_data, "$.data.replies..member.uname")
                    message = jsonpath.jsonpath(json_data, "$.data.replies..content.message")
                    sign = jsonpath.jsonpath(json_data, "$.data.replies..member.sign")
                    pendant = jsonpath.jsonpath(json_data, "$.data.replies..member.pendant.name")
                    send_time = jsonpath.jsonpath(json_data, "$.data.replies..reply_control.time_desc")
                    location = jsonpath.jsonpath(json_data, "$.data.replies..reply_control.location")
                    all_list = zip(uid, user_name, sign, pendant, message, send_time, location)
                    for item_3_1, item_3_2, item_3_3, item_3_4, item_3_5, item_3_6, item_3_7 in all_list:
                        comment_list.append(
                            f'第{i}条=================================================================================\nuid：{item_3_1}\n用户名：{item_3_2}\n{item_3_7}\n签名：{item_3_3}\n装扮：{item_3_4}\n评论内容：{item_3_5}\n发布时间：{item_3_6}\n')
                        i = i + 1
                except Exception as e:
                    print(f"An error occurred: {e}")
    for item_comment in comment_list:
        print(item_comment)
        with open(f'{video_adress}.txt', 'a', encoding='utf-8') as file:
            file.write(item_comment)
    print("===爬取完毕，文件已保存===")




def dynamic():
    uid = input("输入uid（纯数字）")
    url = f'https://space.bilibili.com/{uid}/dynamic'
    #
    # driver1 = webdriver.Edge()
    # driver1.implicitly_wait(5)
    # driver1.get('https://www.bilibili.com/')
    #
    # for cookie in cookies:
    #     driver1.add_cookie(cookie)
    driver1.refresh()
    driver1.get(url=url)
    time.sleep(5)
    driver1.refresh()
    time.sleep(5)
    driver1.implicitly_wait(5)

    print('===等待初始化===')

    time.sleep(5)

    driver1.implicitly_wait(1)
    times_1 = 1
    while True:
        try:
            driver1.find_element(By.XPATH, '//*[@class="bili-dyn-list-no-more"]')
            print("===加载终止===")
            break
        except:
            times_1 = times_1 + 1
            js = "window.scrollTo(0,document.body.scrollHeight)"
            driver1.execute_script(js)
            print(f"===第{times_1}页加载成功===")
    driver1.implicitly_wait(5)

    requests_list = driver1.requests

    prefix = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset='
    filtered_urls = [request.url for request in requests_list if request.url.startswith(prefix)]

    i = 1
    dynamic_list = []
    for url in filtered_urls:
        for request in requests_list:
            if request.url == url:
                try:
                    body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                    json_data = json.loads(body.decode('utf-8'))
                    dynamic_data = jsonpath.jsonpath(json_data, '$.data.items[*]')
                    for item in dynamic_data:
                        dynamic_type = jsonpath.jsonpath(item, '$.type')
                        if dynamic_type == ['DYNAMIC_TYPE_AV']:
                            dynamic_type_txt = '视屏投稿'
                        elif dynamic_type == ['DYNAMIC_TYPE_FORWARD']:
                            dynamic_type_txt = '转发动态'
                        elif dynamic_type == ['DYNAMIC_TYPE_DRAW']:
                            dynamic_type_txt = '图文'
                        else:
                            dynamic_type_txt = '其他'
                        text = jsonpath.jsonpath(item, f'$..module_dynamic.desc.text')
                        send_time = jsonpath.jsonpath(item, '$.modules.module_author.pub_time')
                        url_bv = jsonpath.jsonpath(item, '$.modules.module_dynamic.major.archive.bvid')
                        transmit_url = jsonpath.jsonpath(item, f'$..module_dynamic.major.archive.jump_url')
                        dynamic_list.append(
                            f'第{i}条=================================================================================\n类型：{dynamic_type_txt}\n文本内容：{text}\n发布时间：{send_time}\n投稿视频BV号：{url_bv}\n转发链接：{transmit_url}\n')
                        i = i + 1
                except Exception as e:
                    print(f"发生错误：{e}")

    for item_comment in dynamic_list:
        print(item_comment)
        with open(f'{uid}.txt', 'a', encoding='utf-8') as file:
            file.write(item_comment)
    print("===爬取完毕，文件已保存===")


while True:
    c_code = input('请选择操作指令：\n按"0"键回车退出程序\n按"1"键回车爬取动态\n按"2"键回车爬取视频评论区')
    if c_code == '0':
        break
    if c_code == '1':
        print('===在脚本翻页爬取时请保持屏幕常亮，如有反爬验证码跳出，请手动验证===')
        try:
            dynamic()
        except:
            print("===发生错误，请重试===")
    if c_code == '2':
        print('===在脚本翻页爬取时请保持屏幕常亮，如有反爬验证码跳出，请手动验证===')
        try:
            comment()
        except:
            print("===发生错误，请重试===")