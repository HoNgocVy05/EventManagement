import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class a_SignUpTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.maximize_window()
        time.sleep(1)
        driver = self.driver
        driver.find_element(By.CLASS_NAME, "login").click()
        driver.find_element(By.NAME, "signup").click()
        time.sleep(1)

    #email đã tồn tại
    def test_signup1(self):
        driver = self.driver
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "username").send_keys("visitor")
        driver.find_element(By.NAME, "email").send_keys("hna.191081@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("1234")
        driver.find_element(By.NAME, "confirm_psw").send_keys("1234")
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "btn-login").click()
        time.sleep(2)
        #acp alert
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)

    #cfm mật khẩu không đúng
    def test_signup2(self):
        driver = self.driver
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "username").send_keys("visitor")
        driver.find_element(By.NAME, "email").send_keys("visitor@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("123")
        driver.find_element(By.NAME, "confirm_psw").send_keys("1234")
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "btn-login").click()
        time.sleep(2)
        #acp alert
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)

    #đăng ký tài khoản thành công
    def test_signup3(self):
        driver = self.driver
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "username").send_keys("visitor")
        driver.find_element(By.NAME, "email").send_keys("visitor@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("1233")
        driver.find_element(By.NAME, "confirm_psw").send_keys("1234")
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "btn-login").click()
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

class b_LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.maximize_window()
        time.sleep(1)
        driver = self.driver
        driver.find_element(By.CLASS_NAME, "login").click()
        time.sleep(2)

    #Đăng nhập sai email
    def test_login1(self):
        driver = self.driver
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "email").send_keys("wrongemail@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("1234")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)
        # accept alert
        alert = driver.switch_to.alert
        alert.accept()   

    #Đăng nhập sai mật khẩu
    def test_login2(self):
        driver = self.driver
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "email").send_keys("hna.191081@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("wrongpassword")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)
        # accept alert
        alert = driver.switch_to.alert
        alert.accept() 

    #Đăng nhập đúng
    def test_login3(self):
        driver = self.driver
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "email").send_keys("hna.191081@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("1234")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

class c_AddEventTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.maximize_window()
        time.sleep(1)
        driver = self.driver
        driver.find_element(By.CLASS_NAME, "login").click()
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "email").send_keys("hna.191081@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("1234")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

        driver.find_element(By.ID, "eventDropdown").click()
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "addevent").click()
        time.sleep(2)

    def test_addevent(self):
        driver = self.driver

        #nhập thông tin sự kiện
        driver.find_element(By.ID, "eventName").send_keys("Ứng Dụng Trí Tuệ Nhân Tạo Trong Kinh Doanh")
        time.sleep(0.5)
        driver.find_element(By.ID, "eventDescription").send_keys("Trí tuệ nhân tạo (AI) không còn là một khái niệm xa vời mà đã trở thành công cụ thiết yếu trong nhiều lĩnh vực, đặc biệt là kinh doanh. Hội thapr này sẽ mang đến góc nhìn chuyên sâu về cách AI đang cách mạng hóa các ngành công nghiệp, từ phân tích dữ liệu, tối ưu hóa quy trình cho đến cá nhân hóa trải nghiệm khách hàng.")
        time.sleep(0.5)
        starttime = driver.find_element(By.ID, "eventStartTime")
        starttime.send_keys("02202025") 
        starttime.send_keys(Keys.TAB)
        starttime.send_keys("0330")
        starttime.send_keys("PM")
        driver.find_element(By.ID, "eventTickets").send_keys("100")
        driver.find_element(By.ID, "eventPrice").send_keys("90000")
        #cuộn xuống 400p
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)
        driver.find_element(By.NAME, "add").click()
        time.sleep(1)

    def tearDown(self):
        self.driver.quit()

class d_AddSponsorTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.maximize_window()
        time.sleep(1)
        driver = self.driver
        driver.find_element(By.CLASS_NAME, "login").click()
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "email").send_keys("hna.191081@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("1234")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

        driver = self.driver
        #xem danh sách sự kiện
        driver.find_element(By.ID, "eventDropdown").click()
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "list").click()
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "h4").click()
        time.sleep(2)
        driver.find_element(By.NAME, "sponsor").click()
        time.sleep(1)

    #Chọn nhà tài trợ có sẵn
    def test_addsponsor2(self):
        driver = self.driver
        
        driver.find_element(By.NAME, "sponsor").click()
        time.sleep(1)
        driver.find_element(By.ID, "existing-tab").click()
        time.sleep(1)
        #email nhà tài trợ không tồn tại
        driver.find_element(By.NAME, "email").send_keys("sponsor10@gmail.com")
        driver.find_element(By.CLASS_NAME, "btn").click()
        # accept alert
        alert = driver.switch_to.alert
        alert.accept() 

        #thêm thành công
        driver.find_element(By.NAME, "email").send_keys("sponsor1@gmail.com")
        driver.find_element(By.NAME, "add").click()
        time.sleep(2)

    #Tạo tài khoản cho nhà tài trợ mới
    def test_addsponsor2(self):
        driver = self.driver
        #email đã tồn tại
        driver.find_element(By.ID, "new-tab").click()
        time.sleep(1)
        driver.find_element(By.NAME, "name").send_keys("sponsor1")
        driver.find_element(By.NAME, "email").send_keys("sponsor1@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("sponsor1")
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)
        driver.find_element(By.NAME, "confirm_password").send_keys("sponsor1")
        driver.find_element(By.NAME, "btnAdd").click()
        time.sleep(2)
        # accept alert
        alert = driver.switch_to.alert
        alert.accept() 

        #tạo và thêm thành công
        driver.find_element(By.ID, "new-tab").click()
        time.sleep(1)
        driver.find_element(By.NAME, "name").send_keys("sponsor 3")
        driver.find_element(By.NAME, "email").send_keys("sponsor3@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("sponsor3")
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)
        driver.find_element(By.NAME, "confirm_password").send_keys("sponsor3")
        driver.find_element(By.NAME, "btnAdd").click()
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

class e_AddGuestTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.maximize_window()
        time.sleep(1)
        driver = self.driver
        driver.find_element(By.CLASS_NAME, "login").click()
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "email").send_keys("hna.191081@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("1234")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

    def test_addguest(self):
        driver = self.driver
        #xem chi tiết sự kiện
        driver.find_element(By.ID, "eventDropdown").click()
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "list").click()
        time.sleep(1)
        #chi tiết
        driver.find_element(By.TAG_NAME, "h4").click()
        time.sleep(1)

        #nhập khách mời
        driver.find_element(By.NAME, "guest").click()
        time.sleep(1)
        driver.find_element(By.NAME, "num_guests").send_keys("1")
        time.sleep(1)
        driver.find_element(By.NAME, "name_0").send_keys("guest 1")
        driver.find_element(By.NAME, "email_0").send_keys("guest1@gmail.com")
        time.sleep(1)
        driver.find_element(By.NAME, "addguest").click()
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

class f_BuyTicketTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.maximize_window()
        time.sleep(1)
        driver = self.driver
        driver.find_element(By.CLASS_NAME, "login").click()
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "email").send_keys("hna.191081@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("1234")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

    def test_buyticket(self):
        driver = self.driver
        #xem danh sách sự kiện
        driver.find_element(By.ID, "eventDropdown").click()
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "list").click()
        time.sleep(2)
        #chi tiết
        driver.find_element(By.TAG_NAME, "h4").click()
        time.sleep(2)

        #mua vé
        driver.find_element(By.NAME, "buy").click()
        time.sleep(1)
        driver.find_element(By.NAME, "email").send_keys("visitor1@gmail.com")
        driver.find_element(By.NAME, "phone_number").send_keys("0123456789")
        driver.find_element(By.NAME, "quantity").send_keys("1")
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)
        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()




        


        


