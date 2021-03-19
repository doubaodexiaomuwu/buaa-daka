"""
 ============================
 Author: Grayson
 Time: 2021/3/6 17:08
 E-mail: weipengweibeibei@163.com
 Description: 
 ============================
 """
#先下载pyautogui库，pip install pyautogui
import os,time
import pyautogui as pag

if __name__ == '__main__':
    try:
        print("Press Ctrl-C to end")
        while True:
            x, y = pag.position()  # 返回鼠标的坐标
            posStr = "Position:" + str(x).rjust(4) + ',' + str(y).rjust(4)
            print(posStr)  # 打印坐标
            time.sleep(1)
            os.system('cls')  # 清楚屏幕
    except KeyboardInterrupt:
        print('end....')