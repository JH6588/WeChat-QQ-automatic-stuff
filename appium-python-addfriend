from time import sleep
from appium import webdriver


class WechatTest:
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.2'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'com.tencent.mm'
        desired_caps['appActivity'] = 'com.tencent.mm.ui.LauncherUI'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(20)
        self.msg = "hello"

    def tearDown(self):
        self.driver.quit()

    def process_alert(self):  # 处理弹窗消息 主要是 app 更新提醒
        qx = self.driver.find_elements_by_android_uiautomator('new UiSelector().text("取消")')  # com.tencent.mm:id/aks
        if qx:
            qx[0].click()
            sleep(2)
            self.driver.find_element_by_id("com.tencent.mm:id/akt").click()  # 是
            sleep(2)

    def judge_back(self):
       #判断是否有 <- 返回按钮 ，有即点击
        while True:
            sleep(3)
            backs0 = self.driver.find_elements_by_id("com.tencent.mm:id/hb")
            backs1 = self.driver.find_elements_by_id("com.tencent.mm:id/hj")
            backs = backs0 or backs1
            if backs:
                print("回撤")
                backs[0].click()
            else:
                break

    def test_login(self, username, password):
        sleep(3)
        # 点击登录
        self.driver.find_element_by_id('com.tencent.mm:id/ctm').click()

        sleep(5)
        self.driver.find_element_by_id("com.tencent.mm:id/bqc").click()  # 用微信号
        sleep(3)
        self.driver.find_elements_by_id('com.tencent.mm:id/he')[0].send_keys(username)

        self.driver.find_elements_by_id('com.tencent.mm:id/he')[1].send_keys(password)
        self.driver.find_element_by_id("com.tencent.mm:id/bqd").click()

        sleep(5)
        prompt = self.driver.find_elements_by_id("com.tencent.mm:id/akt")
        if prompt:
            prompt[0].click()
        sleep(8)

    def process(self, account):
        self.process_alert()
        searches = self.driver.find_elements_by_accessibility_id("搜索")

        if searches:
            searches[0].click()
        acct_input = self.driver.find_elements_by_id("com.tencent.mm:id/he")
        if acct_input:
            acct_input[0].send_keys(account)
        sleep(3)
        lx = self.driver.find_elements_by_id("com.tencent.mm:id/ahc")
        if lx:
            print("重复")
            self.judge_back()
            return 0
        else:
            self.driver.find_elements_by_class_name("android.widget.LinearLayout")[6].click()
            print("已经点击")
            sleep(5)
            not_exist = self.driver.find_elements_by_android_uiautomator('new UiSelector().text("用户不存在")')
            alert_window = self.driver.find_elements_by_id("com.tencent.mm:id/c2n")
            if not_exist:
                print("用户不存在")
                self.driver.find_element_by_id("com.tencent.mm:id/akt").click()
                self.judge_back()
                return 0
            elif alert_window and not not_exist:
                print("频繁")
                self.driver.find_element_by_id("com.tencent.mm:id/akt").click()
                self.judge_back()
                return 2
            else:
                print("准备加好友")

                self.add_friend_0()
                self.judge_back()
                return 1

    def add_friend_0(self):

        self.driver.find_element_by_id("com.tencent.mm:id/am8").click()
        sleep(2)
        message = self.driver.find_elements_by_id("com.tencent.mm:id/cqy")
        if message:
            message[0].clear()
            message[0].send_keys(self.msg)
            sleep(2)
            self.driver.find_element_by_id("com.tencent.mm:id/h1").click()


if __name__ == '__main__':
    wt = WechatTest()
    wt.setUp()
    wt.test_login("xxxx" ,"xxxxxx")  #你的账号和密码
    wt.process("1034002766")
    wt.tearDown()
