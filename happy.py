import itchat
from apscheduler.schedulers.blocking import BlockingScheduler
import time


# 发送信息
def send_msg():
    user_info = itchat.search_friends(name='易居装饰')
    if len(user_info) > 0:
        user_name = user_info[0]['UserName']
        itchat.send_msg('王骁铁，生日快乐哦！', toUserName=user_name)


def after_login():
    sched.add_job(send_msg, 'cron', year=2019, month=6, day=12, hour=17, minute=11, second=1)
    sched.start()


def after_logout():
    sched.shutdown()


if __name__ == '__main__':
    sched = BlockingScheduler()
    itchat.auto_login(loginCallback=after_login, exitCallback=after_login)
    itchat.run()