from configparser import ConfigParser
from wechat_add import *
import random
import time
import configparser
from mylog import get_logger
from itertools import cycle

# 读取配置文件
config = ConfigParser()
config.read("setup.ini", encoding="utf8")
is_multi = config.get("multi", "mode") == "on"
unit_width = config.getint("unit", "width")

unit_leng = config.getint("unit", "length")

acct_file_name = "acct.txt"

screen = pyautogui.size()
yeshen_position = (int(unit_leng * 1.5), screen[1] - int(unit_width * 0.5))

print("yeshen_position", yeshen_position)


def get_each_position(yeshen_length, yeshen_num):
    y = yeshen_position[1] - unit_leng
    x_unit = yeshen_length / yeshen_num
    xy = [(int(x_unit / 2 + x_unit * m), y) for m in range(yeshen_num)]

    return xy


def get_random_configuration(opt, key):
    try:
        lst = [ele.strip() for ele in config.get(opt, key).split("---")]
        return random.choice(lst)
    except:
        return config.get(opt, key)


def get_init_yeshens():
    if is_multi:
        yeshen_number = int(config.get('multi', 'number'))
        yeshen_length = int(config.get('multi', 'length'))
        _yeshen_xy = get_each_position(yeshen_length=yeshen_length, yeshen_num=yeshen_number)
        yeshen_infos0 = [{'position': ele} for ele in _yeshen_xy]
        try:
            do = config.get('multi', 'do')
            _do = [int(i) for i in do.split("---")]
            print("夜神操作索引", _do)
            yeshen_infos = [yeshen_infos0[i] for i in _do]
        except configparser.NoOptionError:
            yeshen_infos = yeshen_infos0
        return yeshen_infos
    else:
        return [{"position": yeshen_position}]


def choose_yeshen(yeshen_infos):
    cycle_yeshens = cycle(yeshen_infos)
    while True:
        print("寻找可用的微信.... ")

        ys = next(cycle_yeshens)
        print("备选微信坐标详情", ys)
        if ys.get("sleep") != None:
            if time.time() - ys['sleep_start'] > ys.get('sleep'):
                confirm_to_run(text="已找到可用微信，将进入自动运行, 默认继续", title="寻找微信", timeout=3000)
                yield ys
        else:
            confirm_to_run(text="已找到可用微信，将进入自动运行,默认继续", title="寻找微信", timeout=3000)

            yield ys
        time.sleep(10)


def confirm_to_run(text, title, timeout):
    res = pyautogui.confirm(text=text, title=title, timeout=timeout)
    if res == "Timeout" or res == "OK":
        pass
    else:
        raise Exception("主动停止")
    time.sleep(3)


# 主运行程序
def run(wt, ys, wechat_number):
    time.sleep(3)
    exception_sleep = int(get_random_configuration("sleep", "exception_sleep"))
    try:
        res = add_friend(wt, wechat_number, get_random_configuration("message", "word"))
    except WechatException as e:

        pyautogui.alert(text='{} ,将暂停{}'.format(e, exception_sleep),
                        title="异常", button='ok', timeout=2000)
        ys['sleep'] = exception_sleep
        ys['sleep_start'] = time.time()
        return "exception"
    except Exception as e:
        pyautogui.alert(text=e, title="程序异常", button='ok', timeout=5000)
        return "error"
    return res  # 0 ,1,2  0 ：not exist 1,ok  2 ,repeat


def main(my_ok_yeshens):
    add_number_max = int(get_random_configuration("number", "number"))

    time.sleep(2)
    ys = next(my_ok_yeshens)
    if is_multi:
        pyautogui.click(yeshen_position)
        time.sleep(1)
    pyautogui.click(ys['position'])
    c = 0
    with  open(acct_file_name, encoding="utf8") as f:
        for line in f:
            c += 1
            wt = get_current_wechat()
            result = run(wt, ys, line.strip())
            print("运行结果", result)
            log.info(line + "  -->" + str(result))

            if c == add_number_max or result not in (0, 1, 2):

                print("开始最小化", result, c, add_number_max)
                pyautogui.click(wt.minimum_mark)  # 最小化
                c = 0
                add_number_max = int(get_random_configuration("number", "number"))
                print(int(get_random_configuration("sleep", "round_sleep")), "休息。。。。")
                time.sleep(int(get_random_configuration("sleep", "round_sleep")))
                ys = next(my_ok_yeshens)
                if is_multi:
                    pyautogui.click(yeshen_position)
                    time.sleep(1)
                pyautogui.click(ys['position'])


if __name__ == '__main__':
    print("休息10s后即将启动")
    print("author", "https://github.com/summerlove66")
    time.sleep(10)
    log = get_logger(filename="added.log")
    my_yeshens = get_init_yeshens()
    my_ok_yeshens = choose_yeshen(my_yeshens)
    try:
        main(my_ok_yeshens)
    except KeyboardInterrupt:
        pass
    finally:
        print("程序结束")
