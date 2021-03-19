import win32clipboard as w
import win32con
import win32api
import win32gui
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# 获取日志实例
from util.LoggerUtils import LoggerUtils

logger = LoggerUtils('main').logger

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
def send_message():
    target = '软件学院2020级非全日制'
    logger.info(f'Target message receiver is: {target}')
    logger.info(f'获取鼠标当前位置')
    # 获取鼠标当前位置
    # hwnd=win32gui.FindWindow("MozillaWindowClass",None)
    hwnd = win32gui.FindWindow("WeChatMainWndForPC", None)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.MoveWindow(hwnd, 0, 0, 1000, 700, True)
    time.sleep(0.01)
    logger.info('开始发送消息')
    message = ''
    curr_hour = datetime.now().hour
    if curr_hour == 0:
        # 0:00
        message = '太阳冉冉升起，清风柔柔吹起。新的一天从打卡开始。'
    elif curr_hour == 6:
        # 6:00
        message = '人生是一道风景，快乐是一种心情。行动起来，开始打卡吧。'
    elif curr_hour == 12:
        # 12:00
        message = '中午烈日炎炎，祝你幸运一整天。今天，你打卡了吗？'
    elif curr_hour == 18:
        # 18:00
        message = '晚上日落西山，祝你快乐在心间。还没打卡的同学要抓紧哦。'
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

if __name__ == "__main__":
    logger.info('程序启动')
    # 每天 0:00 6:00 12:00 18:00 发送消息
    scheduler = BlockingScheduler()
    scheduler.add_job(send_message, 'cron', hour='0,6,12,18')
    scheduler.start()
    logger.info('程序结束')