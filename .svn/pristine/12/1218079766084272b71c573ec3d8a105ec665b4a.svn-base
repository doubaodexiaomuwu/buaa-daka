#!/usr/bin/python3  

# -*- coding: utf-8 -*-
# @Author   : Grayson
# @Time     : 2020-12-07 20:48
# @Email    : weipengweibeibei@163.com
# @Description  :

import datetime
import random
class Pic_str:
  def create_uuid(self): #生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S"); # 生成当前时间
    randomNum = random.randint(0, 100); # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
      randomNum = str(0) + str(randomNum);
    uniqueNum = str(nowTime) + str(randomNum);
    return uniqueNum;