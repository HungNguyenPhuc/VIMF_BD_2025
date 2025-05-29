from RTDE_exchange.exchange_data import RTDE_ed
import threading

robot = RTDE_ed("192.168.1.100")
rtde_lock = threading.Lock()  # tạo 1 lock
