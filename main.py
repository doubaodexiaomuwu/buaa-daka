import time

from apscheduler.schedulers.blocking import BlockingScheduler

# 获取日志实例
from apscheduler.schedulers.blocking import BlockingScheduler

# 获取日志实例
from util.CommonUtils import wechat_daka
from util.LoggerUtils import LoggerUtils

logger = LoggerUtils('main').logger

if __name__ == "__main__":
    logger.info('程序启动')
    # 每隔 3 分钟检测一下是否有新增未打卡同学的图片
    scheduler = BlockingScheduler()
    scheduler.add_job(wechat_daka, 'interval', minutes=1)
    scheduler.start()
    logger.info('程序结束')