# Tài liệu: Chương trình Điều khiển Robot UR qua Joystick bằng RTDE

# 1. Giới thiệu chung

Script Python này cho phép người dùng điều khiển một robot Universal Robots(UR) thông qua một thiết bị joystick/gamepad được kết nối với máy tính. Chương trình sử dụng thư viện `pygame` để đọc dữ liệu từ joystick(trạng thái các trục, nút bấm, D-pad) và thư viện `rtde` (thông qua một module tùy chỉnh `exchange_data`) để gửi các dữ liệu này đến robot UR theo thời gian thực.

Mục tiêu là tạo ra một giao diện điều khiển từ xa cho robot, nơi các chuyển động của joystick có thể được ánh xạ thành các lệnh di chuyển hoặc hành động của robot.

# 2. Các thành phần chính và Module sử dụng

# 2.1. Module và Thư viện

* **`pygame`**: Thư viện đa phương tiện phổ biến, được sử dụng ở đây chủ yếu cho việc giao tiếp và đọc dữ liệu từ thiết bị joystick.
 *   `pygame.init()`: Khởi tạo tất cả các module của pygame.
  *   `pygame.joystick.init()`: Khởi tạo module joystick.
   *   `pygame.joystick.get_count()`: Lấy số lượng joystick được kết nối.
    *   `pygame.joystick.Joystick(index)`: Tạo đối tượng joystick.
    *   `joystick.init()`: Khởi tạo joystick đã chọn.
    *   `joystick.get_name()`: Lấy tên của joystick.
    *   `joystick.get_numaxes()`: Lấy số lượng trục.
    *   `joystick.get_numbuttons()`: Lấy số lượng nút.
    *   `joystick.get_numhats()`: Lấy số lượng D-pad(hat switch).
    *   `pygame.event.pump()`: Xử lý hàng đợi sự kiện của pygame, cần thiết để cập nhật trạng thái joystick.
    *   `joystick.get_axis(i)`: Đọc giá trị của một trục(thường từ - 1.0 đến 1.0).
    *   `joystick.get_button(i)`: Đọc trạng thái của một nút(0 là nhả, 1 là nhấn).
    *   `joystick.get_hat(i)`: Đọc trạng thái của D-pad(trả về một tuple `(x, y)` với giá trị - 1, 0, hoặc 1 cho mỗi hướng).
    *   `pygame.time.wait(milliseconds)`: Tạm dừng chương trình.
    *   `joystick.quit()`: Hủy khởi tạo joystick.
    *   `pygame.quit()`: Hủy khởi tạo tất cả các module pygame.
* **`time.sleep`**: Dùng để tạo một khoảng dừng nhỏ trong vòng lặp chính.
* **`exchange_data`**: Một module tùy chỉnh(do người dùng cung cấp) chứa class `RTDE_ed`. Module này chịu trách nhiệm thiết lập và quản lý kết nối Real-Time Data Exchange(RTDE) với robot UR.
 *   `exchange_data.RTDE_ed()`: Khởi tạo đối tượng RTDE. Trong code, có một dòng bị comment out `rb = exchange_data.RTDE_ed(robot_ip="172.17.0.2")` cho thấy có thể truyền địa chỉ IP của robot khi khởi tạo.
  *   `rb.send_data_to_robot_joystick(bool_data, double_data)`: Một phương thức tùy chỉnh trong `RTDE_ed` để gửi dữ liệu trạng thái joystick(dạng boolean và số thực) đến robot.
   *   `rb.reconnect()`: Một phương thức tùy chỉnh trong `RTDE_ed` để cố gắng kết nối lại với robot nếu kết nối bị mất.

# 2.2. Các biến lưu trữ dữ liệu Joystick

*   `bool_data` (list): Danh sách chứa các giá trị boolean, được tạo bằng cách kết hợp `hat_data` và `button_data`. Dữ liệu này sẽ được gửi đến robot.
*   `button_data` (list): Danh sách tạm thời lưu trữ trạng thái của 8 nút bấm đầu tiên(0-7) của joystick.
*   `hat_data` (list): Danh sách tạm thời lưu trữ trạng thái của D-pad đầu tiên. Được chuyển đổi thành list các giá trị số nguyên.
*   `double_data` (list): Danh sách lưu trữ giá trị của tất cả các trục joystick(dạng số thực). Dữ liệu này sẽ được gửi đến robot.

# 2.3. Đối tượng RTDE

*   `rb = exchange_data.RTDE_ed()`: Tạo một instance của class `RTDE_ed` từ module `exchange_data` để quản lý giao tiếp với robot.

# 3. Luồng hoạt động của chương trình

1. ** Khởi tạo: **
 *   Khởi tạo `pygame` và module `joystick`.
  *   Kiểm tra số lượng joystick được kết nối. Nếu không có, chương trình thoát.
   *   Chọn và khởi tạo joystick đầu tiên(`pygame.joystick.Joystick(0)`).
    *   In thông tin về joystick(tên, số trục, số nút, số D-pad).
    *   Khởi tạo đối tượng `rb` để giao tiếp RTDE với robot.
2. ** Vòng lặp chính(`while True`): **
  * **Cập nhật sự kiện Pygame: ** `pygame.event.pump()` được gọi để đảm bảo pygame xử lý các sự kiện nội bộ và cập nhật trạng thái joystick.
   * **Đọc dữ liệu Trục(Axes): **
     *   Lặp qua tất cả các trục của joystick(`joystick.get_numaxes()`).
      *   Đọc giá trị của từng trục(`joystick.get_axis(i)`) và thêm vào danh sách `double_data`.
       *   In danh sách `double_data` (giá trị các trục).
    * **Đọc dữ liệu Nút(Buttons): **
     *   Lặp qua 8 nút đầu tiên (chỉ số 0 đến 7).
      *   Đọc trạng thái của từng nút(`joystick.get_button(i)`) và thêm vào `button_data`.
       *   In danh sách `button_data`.
    * **Đọc dữ liệu D-Pad(Hat): **
     *   Lặp qua tất cả các D-pad (thường chỉ có một).
      *   Đọc trạng thái của D-pad(`joystick.get_hat(i)`), trả về một tuple `(x, y)`.
       *   Thêm tuple này vào `hat_data`.
        *   Chuyển đổi `hat_data[0]` (tuple trạng thái D-pad đầu tiên) thành một list.
        *   In danh sách `hat_data`.
    * **Kết hợp Dữ liệu Boolean: **
     *   Tạo `bool_data` bằng cách nối `hat_data` (đã chuyển thành list) và `button_data`.
      *   In danh sách `bool_data`.
    * **Tạm dừng ngắn: ** `pygame.time.wait(100)` (0.1 giây) để giảm tải CPU và giới hạn tần suất gửi dữ liệu.
    * **Gửi dữ liệu đến Robot: **
     *   Gọi `rb.send_data_to_robot_joystick(bool_data, double_data)` để gửi trạng thái joystick hiện tại đến robot qua RTDE.
      *   **Xử lý lỗi kết nối: ** Nếu xảy ra `ConnectionResetError` (nghĩa là kết nối với robot bị mất), in thông báo lỗi và gọi `rb.reconnect()` để cố gắng kết nối lại.
    * **Reset danh sách dữ liệu: ** Xóa nội dung của `bool_data`, `hat_data`, `button_data`, `double_data` để chuẩn bị cho lần đọc tiếp theo.
    * **Tạm dừng rất ngắn: ** `sleep(0.01)` (0.01 giây) để đảm bảo vòng lặp không chạy quá nhanh.
3. ** Kết thúc chương trình (Xử lý `KeyboardInterrupt`): **
 *   Khi người dùng nhấn Ctrl+C, vòng lặp chính bị ngắt.
  *   In thông báo "Thoát chương trình".
4.  ** Dọn dẹp (`finally `): **
 *   `joystick.quit()`: Hủy khởi tạo joystick hiện tại.
  *   `pygame.quit()`: Hủy khởi tạo tất cả các module pygame, giải phóng tài nguyên.
   *   **(Thiếu sót): ** Nên có lệnh ngắt kết nối RTDE với robot (ví dụ: `rb.disconnect()`) trong khối `finally `.

# 4. Cách sử dụng

1.  Đảm bảo module `exchange_data.py` tồn tại và được cấu hình đúng để kết nối với robot UR.
2.  Kết nối một thiết bị joystick/gamepad với máy tính.
3.  Chạy script Python này.
4.  Chương trình sẽ tự động phát hiện joystick đầu tiên.
5.  Di chuyển các trục, nhấn các nút, và sử dụng D-pad trên joystick. Trạng thái của chúng sẽ được in ra terminal và(theo thiết kế) được gửi đến robot UR.
6.  Nhấn Ctrl+C trong terminal để thoát chương trình.

# 5. Các điểm cần lưu ý và Cải tiến tiềm năng

* **Module `exchange_data`: ** Hoạt động của chương trình phụ thuộc hoàn toàn vào việc triển khai chính xác của class `RTDE_ed` và các phương thức `send_data_to_robot_joystick`, `reconnect` trong module này. Cần đảm bảo rằng các "recipes" RTDE trên robot được thiết lập để nhận đúng định dạng dữ liệu(`bool_data` và `double_data`).
* **Địa chỉ IP Robot: ** Hiện tại, `rb = exchange_data.RTDE_ed()` không có tham số IP, ngụ ý rằng IP có thể được hardcode bên trong `RTDE_ed` hoặc có một cơ chế mặc định. Dòng bị comment `rb = exchange_data.RTDE_ed(robot_ip="172.17.0.2")` cho thấy khả năng truyền IP. Nên làm cho việc cấu hình IP linh hoạt hơn(ví dụ: qua tham số dòng lệnh hoặc file config).
* **Xử lý nhiều Joystick: ** Code hiện tại chỉ chọn joystick đầu tiên(`Joystick(0)`). Nếu có nhiều joystick, cần có cơ chế cho phép người dùng chọn hoặc tự động chọn joystick phù hợp.
* **Đọc tất cả Nút/Trục/Hat: ** Code hiện tại chỉ đọc 8 nút đầu tiên. Nếu joystick có nhiều hơn, cần điều chỉnh vòng lặp. Tương tự cho Hat.
*   **Ánh xạ Dữ liệu Joystick sang Hành động Robot: ** Script này chỉ gửi dữ liệu thô từ joystick. Logic thực sự để diễn giải dữ liệu này (ví dụ: trục X của joystick điều khiển chuyển động X của TCP robot, nút A kích hoạt gripper) phải được lập trình ** trên robot UR ** (trong chương trình Polyscope nhận dữ liệu RTDE) hoặc trong một node ROS khác nhận dữ liệu này và ra lệnh cho robot.
* **Tần suất gửi dữ liệu: ** Hiện tại, dữ liệu được gửi mỗi khoảng 0.11 giây(`pygame.time.wait(100)` + `sleep(0.01)`). Tần suất này có thể cần được điều chỉnh tùy thuộc vào yêu cầu đáp ứng của robot và khả năng xử lý của mạng/RTDE.
* **Ngắt kết nối RTDE khi thoát: ** Nên thêm `rb.disconnect()` trong khối `finally ` để đóng kết nối RTDE một cách sạch sẽ.
* **Giao diện người dùng(GUI): ** Nếu muốn một ứng dụng thân thiện hơn, có thể tích hợp logic này vào một GUI Tkinter (tương tự như các ví dụ trước) để chọn joystick, hiển thị trạng thái, và cấu hình IP robot.
* **Xử lý Deadzone cho Trục: ** Các trục analog của joystick thường có một "deadzone" nhỏ ở giữa, nơi chúng không hoàn toàn trả về 0 ngay cả khi không chạm vào. Có thể cần thêm logic để bỏ qua các giá trị rất nhỏ gần 0 của trục để tránh robot bị "trôi" nhẹ.
