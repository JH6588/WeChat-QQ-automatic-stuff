import win32gui
import pyautogui

classname = 'Qt5QWindowIcon'

marks = dict(
    search_result_click_mark=(0.173, 0.158),
    search_mark=(0.798, 0.094),
    send_mark=(0.924, 0.093),
    clean_message_mark=(0.918, 0.185),
    back_mark=(0.045, 0.092),
    minimum_mark=(0.786, 0.012),
    stuck_mark=(0.687, 0.551),
    close_mark=(0.953, 0.012),
    touch_mark=(0.596, 0.091),
    green_button_check=(0.075, 0.33, 0.127, 0.836),
    judge_status_check=(0.561, 0.490, 0.575, 0.492),
    is_friend_check=(0.223, 0.194, 0.289, 0.206),
    search_result_check=(0.047, 0.141, 0.116, 0.153),

)


def get_wechat_info():
    hd = win32gui.FindWindow(classname, None)
    postion = win32gui.GetWindowRect(hd)
    print("wechat postion", postion)
    length = postion[2] - postion[0]
    width = postion[3] - postion[1]
    return {"position": postion, 'length': length, 'width': width}


class WechatPosition:
    mark_keys = list(marks.keys()) + ['wechat_position', 'wechat_length', 'wechat_width']
    __slots__ = mark_keys

    def __init__(self):
        wechat_info = get_wechat_info()
        self.wechat_position = wechat_info['position']
        self.wechat_length = wechat_info['length']
        self.wechat_width = wechat_info['width']

    def clean_marks(self):

        for ele in marks:
            self.__setattr__(ele, self.get_position(marks[ele]))

    def position_processs(self, position):  #得到某个位置 所在的mark 位置所在的比例

        ma = (position[0] - self.wechat_position[0]) * 1000 // self.wechat_length / 1000
        mb = (position[1] - self.wechat_position[1]) * 1000 // self.wechat_width / 1000
        return ma, mb

    def get_position(self, mark): #得到某个比例所在的实际位置
        if len(mark) == 2:
            return (round(self.wechat_position[0] + self.wechat_length * mark[0]),
                    round(self.wechat_position[1] + self.wechat_width * mark[1]))
        else:
            start = self.get_position((mark[0], mark[1]))
            last = self.get_position((mark[2], mark[3]))
            return (start[0], start[1], last[0], last[1])

    def position_processs_now(self): #得到当前位置所在的比例
        mark = pyautogui.position()
        return self.position_processs(mark)

    def judge_stuck(self, stuck_mark, t=5):  #判断是否卡死
        res = 0
        c = 0
        while c < t:
            stuck_point_pixel = pyautogui.pixel(stuck_mark[0], stuck_mark[1])
            if stuck_point_pixel[0] == stuck_point_pixel[1] == stuck_point_pixel[2] and stuck_point_pixel[0] < 57:
                res = 1
                time.sleep(2)
            else:
                res = 0
                break
        return res

    def judge_button(self, check_mark):  # 正常情况下 返回添加位置的坐标
        for position in self.check_marks_ponit(check_mark, 5, 10):
            color = pyautogui.pixel(position[0], position[1])
            print("judge button", position, color)
            if color[0] + color[2] < color[1]:
                return position[0] + 2, position[1] + 5  # 边缘情况向内偏移以保证点击有效

            elif color[0] == color[1] == color[2] and 80 < color[1] < 150: #弹窗
                return 0

    def judge_status(self, check_mark):  # 判断是否频繁

        for position in self.check_marks_ponit(check_mark, 3, 1):
            color = pyautogui.pixel(position[0], position[1])
            print("判断是否频繁", color)
            if color[0] < 255:
                return 1

    def judge_isfriend(self, check_mark):  #判断是否已经为好友
        res = 0  # 非好友
        for position in self.check_marks_ponit(check_mark, 2, 1):
            color = pyautogui.pixel(position[0], position[1])
            if 70 < color[0] < 255:  # 出现灰色字样
                res = 1  # 好友
                print("判断是否为好友", color)
                break
        return res

    def judge_is_repeat(self, check_mark): # 该号码存在多个微信
        res = 1  # 1表示重复  例如 15775192300
        for position in self.check_marks_ponit(check_mark, 1, 1):
            color = pyautogui.pixel(position[0], position[1])
            if color[0] + color[2] < color[1]:
                res = 0  # 有绿色 未重复
                break
        return res

    def check_marks_ponit(self, check_mark, leng_step=1, width_step=1): #得到mark的搜索范围
        for i in range(check_mark[0], check_mark[2], leng_step):
            for j in range(check_mark[1], check_mark[3], width_step):
                yield (i, j)


if __name__ == '__main__':
    import time

    time.sleep(2)

    w = WechatPosition()
    p = w.get_position((0.075, 0.33))
    print(w.position_processs_now())
    print(pyautogui.pixel(pyautogui.position()[0], pyautogui.position()[1]))
