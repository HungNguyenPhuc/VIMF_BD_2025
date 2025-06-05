import pygame
from time import sleep
import exchange_data

bool_data = []
button_data = []
hat_data = []
double_data = []
# rb = exchange_data.RTDE_ed(robot_ip="172.17.0.2")
rb = exchange_data.RTDE_ed()
# Khởi tạo pygame
pygame.init()

# Khởi tạo joystick
pygame.joystick.init()

# Kiểm tra số lượng joystick
joystick_count = pygame.joystick.get_count()
print(f"Số joystick tìm thấy: {joystick_count}")

if joystick_count == 0:
    print("Không có joystick nào được kết nối.")
    exit()

# Chọn joystick đầu tiên
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Đang sử dụng joystick: {joystick.get_name()}")

# In số lượng nút, trục, v.v
print(f"Số trục: {joystick.get_numaxes()}")
print(f"Số nút: {joystick.get_numbuttons()}")
print(f"Số hat (D-pad): {joystick.get_numhats()}")

# Vòng lặp chính
try:
    while True:
        pygame.event.pump()  # Cập nhật sự kiện joystick

        # Đọc giá trị các trục (axis)
        for i in range(joystick.get_numaxes()):
            axis = joystick.get_axis(i)
            double_data.append(axis)
            # print(f"Trục {i}: {axis:.2f}", end="  ")
        print(double_data)

        # Đọc trạng thái nút bấm
        for i in range(0, 8, 1):
            button = joystick.get_button(i)
            button_data.append(button)
        print("button list: ", button_data)
        # Đọc D-Pad (Hat)
        for i in range(joystick.get_numhats()):
            hat = joystick.get_hat(i)
            # print(f"D-Pad {i}: {hat}")
            hat_data.append(hat)
        hat_data = list(hat_data[0])
        print("hat list: ", hat_data)
        bool_data = hat_data + button_data
        print("bool list: ", bool_data)
        pygame.time.wait(100)
        try:
            rb.send_data_to_robot_joystick(bool_data, double_data)
        except ConnectionResetError:
            print("[ERROR]: Mất kết nối với robot. Đang reconnect ...")
            rb.reconnect()
        bool_data = []
        hat_data = []
        button_data = []
        double_data = []
        sleep(0.01)

except KeyboardInterrupt:
    print("\nThoát chương trình")

finally:
    joystick.quit()
    pygame.quit()
