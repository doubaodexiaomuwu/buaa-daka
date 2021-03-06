import datetime
import os
import re
import shutil
import time
from datetime import datetime

import urllib3
import win32api
import win32clipboard as w
import win32con
import win32gui
from aip import AipOcr

# 获取日志实例
from util.LoggerUtils import LoggerUtils
from util.MySqlUtils import connect, add


logger = LoggerUtils('CommonUtils').logger

abspath = os.getcwd()
# 警用requests中的警告
urllib3.disable_warnings()

APP_ID = '23019380'
API_KEY = 'dv4p2h8RhPWH42AZPreN0FLf'
SECRECT_KEY = 'RzIgq0MoSdKhYFh1XIs1obORAGs6Wl7z'
EXCLUDE_WORDS = [
    '姓名',
    '学号',
    '身份',
    '疑似或',
    '确',
    '确诊',
    '上报时',
    '间',
    '研究生',
    '今日未上',
    '报',
    '代填',
    '加载完成',
    'C加载中',
    'Z',
    '导出列表',
    '请输入搜索的关键字',
    '￡似或””工的'
]
DATABASE = 'buaa_daka'
client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)

class Student:
    stu_name = ''

# 将数据存入mysql
def save_to_mysql(students, is_late=0):
    conn = connect(DATABASE)
    for student in students:
        upload_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = 'insert into daka_info (stu_name, upload_time, is_late) values (%s, %s, %s);'
        val = (student.stu_name, upload_time, is_late)
        add(conn, sql, val)

# 获取未打卡学生信息
def get_daka(image_path, send_message_target):
    logger = LoggerUtils('get_daka').logger
    # 解析未打卡信息
    img = open(image_path, 'rb').read()
    ret = client.basicGeneral(img)
    # ret = client.basicAccurate(img)
    clear_words = []
    students = []
    logger.info('Detail info for daka:')
    for index, item in enumerate(ret['words_result']):
        is_except = False
        words = item['words']
        logger.info(words)
        if index <= 2 and 'ZF' not in words: continue
        if 'z' in words: words = words[:words.index('z')]
        if 'Z' in words: words = words[:words.index('Z')]
        if 'F' in words: words = words[:words.index('F')]
        if '-' in words: words = words[:words.index('-')]
        if '2' in words: words = words[:words.index('2')]
        for except_word in EXCLUDE_WORDS:
            if except_word in words:
                is_except = True
                break
        if is_except == True: continue
        if bool(re.search(r'\d', words)) == True: continue
        if words == '': continue
        clear_words.append(words)

    # 将未打卡信息进行过滤
    notice_info = ''
    logger.info('Clear info for daka:')
    for word in clear_words:
        notice_info += '@' + word + ' '
        student = Student()
        student.stu_name = word
        students.append(student)
        logger.info(student.stu_name)
    # notice_info += '没打卡的同学记得打卡哈'

    # 将过滤后的未打卡信息数据存入mysql
    # save_to_mysql(students)

    # 输出@信息
    logger.info('Notice info is: %s' % notice_info)

    logger.info(f'发送消息')
    send_message(send_message_target, notice_info)

# 把文字放入剪贴板
def setText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

# 模拟ctrl+V
def ctrlV():
    win32api.keybd_event(17, 0, 0, 0)  # ctrl
    win32api.keybd_event(86, 0, 0, 0)  # V
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

# 模拟alt+s
def altS():
    win32api.keybd_event(18, 0, 0, 0)
    win32api.keybd_event(83, 0, 0, 0)
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)

# 模拟enter
def enter():
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)

# 模拟单击
def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# 模拟右键
def right_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

# 移动鼠标的位置
def movePos(x, y):
    win32api.SetCursorPos((x, y))

# 发送消息
def send_message(target, notice_info):
    logger.info(f'Target message receiver is: {target}')
    logger.info(f'获取鼠标当前位置')
    # 获取鼠标当前位置
    # hwnd=win32gui.FindWindow("MozillaWindowClass",None)
    hwnd = win32gui.FindWindow("WeChatMainWndForPC", None)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.MoveWindow(hwnd, 0, 0, 1000, 700, True)
    time.sleep(0.01)
    logger.info('开始发送消息')
    curr_hour = datetime.now().hour
    if curr_hour < 10:
        # 10:00
        message = notice_info + '人生是一道风景，快乐是一种心情。行动起来，开始打卡吧。'
    elif curr_hour < 14:
        # 14:00
        message = notice_info + '中午烈日炎炎，祝你幸运一整天。今天，你打卡了吗？'
    else:
        message = notice_info + '晚上日落西山，祝你快乐在心间。还没打卡的同学要抓紧哦。'
    logger.info(f'Message is: {message}')
    # 1.移动鼠标到通讯录位置，单击打开通讯录
    logger.info(f'1.移动鼠标到通讯录位置，单击打开通讯录')
    movePos(28, 147)
    click()
    # 2.移动鼠标到搜索框，单击，输入要搜索的名字
    logger.info(f'2.移动鼠标到搜索框，单击，输入要搜索的名字')
    movePos(148, 35)
    click()
    setText('文件传输助手')
    ctrlV()
    time.sleep(1)  # 别问我为什么要停1秒，问就是给微信一个反应的时间，他反应慢反应不过来，其他位置暂停的原因同样
    enter()
    time.sleep(1)
    # 3.发送打卡程序
    logger.info(f'3.发送打卡程序')
    movePos(788, 360)
    right_click()
    movePos(817, 400)
    click()
    time.sleep(1)
    movePos(817, 400)
    click()
    time.sleep(1)
    movePos(478, 169)
    click()
    setText(target)
    ctrlV()
    time.sleep(1)
    movePos(651, 255)
    click()
    time.sleep(1)
    movePos(823, 591)
    click()
    time.sleep(1)
    # 4.发送消息
    logger.info(f'4.发送消息')
    # 4.1.移动鼠标到通讯录位置，单击打开通讯录
    logger.info(f'4.1.移动鼠标到通讯录位置，单击打开通讯录')
    movePos(28, 147)
    click()
    time.sleep(1)
    # 4.2.移动鼠标到搜索框，单击，输入要搜索的名字
    logger.info(f'4.2.移动鼠标到搜索框，单击，输入要搜索的名字')
    movePos(148, 35)
    click()
    setText(target)
    ctrlV()
    time.sleep(1)  # 别问我为什么要停1秒，问就是给微信一个反应的时间，他反应慢反应不过来，其他位置暂停的原因同样
    enter()
    time.sleep(1)
    # 4.3.复制要发送的消息，发送
    logger.info(f'4.3.复制要发送的消息，发送')
    setText(message)
    ctrlV()
    altS()
    logger.info('消息发送成功')

# 获取要发送的消息
def get_message(send_message_target):
    path_to_watch = "E:/Projects/buaa-daka/image/打卡"
    target_path = "E:/Projects/buaa-daka/image/打卡_备份"
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    time.sleep(2)
    after = dict([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    if added:
        before = after
        full_path = f'{path_to_watch}/{added[0]}'
        logger.info(f'新增文件: {full_path}')
        logger.info(f'正在解析打卡信息: {full_path}')
        time.sleep(2)
        get_daka(full_path, send_message_target)
        time.sleep(2)
        remove_file(path_to_watch, target_path)
    return added

# 将一个目录下的文件移动到另一个目录下
def remove_file(old_path, new_path):
    print(f'正在移动文件 -> 源目录: {old_path} 目标目录: {new_path}')
    filelist = os.listdir(old_path) #列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    for file in filelist:
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)
        logger.info(f'src: {src}, dst_src: {dst}')
        shutil.move(src, dst)

# 获取未打卡同学图片
def get_daka_image(target):
    time.sleep(4)
    # 1.移动鼠标到通讯录位置，单击打开通讯录
    logger.info(f'1.移动鼠标到通讯录位置，单击打开通讯录')
    movePos(28, 147)
    click()
    # 2.移动鼠标到搜索框，单击，输入要搜索的名字
    logger.info(f'2.移动鼠标到搜索框，单击，输入要搜索的名字')
    movePos(148, 35)
    click()
    setText(target)
    ctrlV()
    time.sleep(1)  # 别问我为什么要停1秒，问就是给微信一个反应的时间，他反应慢反应不过来，其他位置暂停的原因同样
    enter()
    time.sleep(1)
    # 3.获取未打卡同学图片
    logger.info(f'3.获取未打卡同学图片')
    movePos(422, 168)
    right_click()
    movePos(460, 174)
    click()
    time.sleep(1)
    movePos(460, 174)
    click()
    time.sleep(1)
    movePos(1130, 297)
    click()
    time.sleep(1)
    ctrlV()

# 删除未打卡同学图片
def delete_daka_image(target):
    time.sleep(4)
    # 1.移动鼠标到通讯录位置，单击打开通讯录
    logger.info(f'1.移动鼠标到通讯录位置，单击打开通讯录')
    movePos(28, 147)
    click()
    # 2.移动鼠标到搜索框，单击，输入要搜索的名字
    logger.info(f'2.移动鼠标到搜索框，单击，输入要搜索的名字')
    movePos(148, 35)
    click()
    setText(target)
    ctrlV()
    time.sleep(1)  # 别问我为什么要停1秒，问就是给微信一个反应的时间，他反应慢反应不过来，其他位置暂停的原因同样
    enter()
    time.sleep(1)
    # 3.删除未打卡同学图片
    logger.info(f'3.删除未打卡同学图片')
    movePos(422, 168)
    right_click()
    movePos(460, 174)
    click()
    time.sleep(1)
    movePos(462, 372)
    click()
    time.sleep(1)
    movePos(543, 424)
    click()

# 微信机器人提醒未打卡同学打卡
def wechat_daka():
    send_message_target = '文件传输助手'
    # send_message_target = '软件学院2020级非全日制'
    daka_image_target = '姐'
    # daka_image_target = '赵玉艳'
    logger.info(f'获取未打卡同学图片')
    get_daka_image(daka_image_target)
    logger.info(f'获取要发送的消息')
    added = get_message(send_message_target)
    if added:
        logger.info(f'删除未打卡同学图片')
        delete_daka_image(daka_image_target)
    else:
        logger.info('未发现新增未打卡同学图片')