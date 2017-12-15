import random
import time

import pyautogui
import pyperclip
from we_chat_marks import WechatPosition


class WechatException(Exception):  # 微信异常
    pass


def sleep_random_time(t=1.0):
    time.sleep(random.randint(10, 20) * t / 10)


def paste(foo):
    pyperclip.copy(foo)
    pyautogui.hotkey('ctrl', 'v')


def get_current_wechat():
    wt = WechatPosition()
    wt.clean_marks()
    print("窗口宽度", wt.wechat_width)
    if wt.wechat_width < 550:  # 窗体宽度可以在 550 到768之间浮动

        pyautogui.alert(text="窗口太小请稍微高大些 ，确保大于550", title="微信异常",
                        timeout=3000)
        raise Exception()

    if wt.judge_stuck(wt.stuck_mark):
        pyautogui.alert(text="微信卡死", title="微信异常",
                        timeout=3000)
        pyautogui.click(wt.close_mark)  # 关闭
        raise Exception()
    return wt


def add_friend(wt, wechat_number, message):  #
    pyautogui.click(wt.search_mark)
    sleep_random_time(t=2)
    paste(wechat_number)
    sleep_random_time()
    print("微信号：", wechat_number)
    if wt.judge_is_repeat(wt.search_result_check):
        print("该号码为重复添加    或者  夜神无法输入需重启")
        pyautogui.click(wt.back_mark)
        return 2
    pyautogui.click(wt.search_result_click_mark)
    sleep_random_time()

    print("寻找添加绿块")
    res = wt.judge_button(wt.green_button_check)
    if res:  # 正常情况
        add_button = res
        pyautogui.click(add_button)
        sleep_random_time(t=0.5)
        print("add-------------")
        pyautogui.click(wt.clean_message_mark)
        sleep_random_time(t=0.5)
        paste(message)
        sleep_random_time(t=0.8)
        pyautogui.click(wt.send_mark)
        sleep_random_time(t=3)
        pyautogui.click(wt.touch_mark)  # 有些事 直接就通过的
        time.sleep(2)
        pyautogui.click(wt.back_mark)
        print("back--------")
        sleep_random_time(t=1.5)
        pyautogui.click(wt.back_mark)
        sleep_random_time(t=3)
        return 1  # 添加成功
    elif res == 0:  # 异常情况

        status_res = wt.judge_status(wt.judge_status_check)

        sleep_random_time(t=0.5)
        pyautogui.click(wt.back_mark)
        sleep_random_time(t=0.5)
        pyautogui.click(wt.back_mark)
        if status_res:
            raise WechatException("微信操作异常")
        if wt.judge_isfriend(wt.is_friend_check):
            pyautogui.click(wt.back_mark)
            sleep_random_time(t=1.5)
            pyautogui.click(wt.back_mark)
            return 2  # 已经是好友
        return 0  # 用户不存在
    else:
        pyautogui.click(wt.back_mark)
        sleep_random_time(t=1.5)
        pyautogui.click(wt.back_mark)
        return 1  # 直接就通过的情况


if __name__ == '__main__':
    time.sleep(2)
    wt = get_current_wechat()
    add_friend(wt, "1034002756", "hello")
