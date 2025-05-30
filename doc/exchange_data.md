# Tài liệu: Class `RTDE_ed` - Giao tiếp Real-Time Data Exchange với Robot UR

## 1. Giới thiệu chung

Class `RTDE_ed` được thiết kế để đơn giản hóa việc thiết lập và quản lý giao tiếp Real-Time Data Exchange (RTDE) giữa một ứng dụng Python và robot Universal Robots (UR). Nó cho phép gửi dữ liệu đầu vào (input) đến robot (ví dụ: từ joystick, camera vision) và nhận dữ liệu đầu ra (output) từ robot (ví dụ: trạng thái robot).

Class này sử dụng thư viện `rtde` chính thức của Universal Robots và đọc cấu hình "recipes" (định nghĩa các biến dữ liệu sẽ được trao đổi) từ một file XML (`data.xml`).

## 2. Các thành phần chính và Module sử dụng

### 2.1. Module và Thư viện

*   **`rtde.rtde`**: Module chính từ thư viện `rtde` để tạo đối tượng kết nối RTDE.
*   **`rtde.rtde_config`**: Module từ thư viện `rtde` để đọc file cấu hình XML cho các recipes RTDE.
*   **`time.sleep`**: Dùng để tạo các khoảng dừng cần thiết trong quá trình kết nối hoặc đồng bộ hóa.

### 2.2. Thuộc tính của Class

*   `ROBOT_HOST` (str): Địa chỉ IP của robot UR.
*   `ROBOT_PORT` (int): Cổng RTDE của robot (mặc định là 30004).
*   `config_filename` (str): Tên file XML chứa định nghĩa các recipes (mặc định là "data.xml").
*   `conf` (rtde_config.ConfigFile): Đối tượng chứa cấu hình recipes đã đọc từ file XML.
*   `out_names`, `out_types` (list): Danh sách tên và kiểu dữ liệu của các biến output (dữ liệu từ robot gửi về Python).
*   `in_names`, `in_types` (list): Danh sách tên và kiểu dữ liệu của các biến input (dữ liệu từ Python gửi đến robot).
*   `watchdog_name`, `watchdog_type` (list): Tên và kiểu dữ liệu của biến watchdog (một loại biến input đặc biệt để giám sát kết nối).
*   `con` (rtde.RTDE): Đối tượng kết nối RTDE chính.
*   `inputs` (RTDEInputObject): Đối tượng được trả về từ `con.send_input_setup()`, dùng để thiết lập giá trị cho các biến input gửi đến robot. Các thuộc tính của đối tượng này sẽ tương ứng với tên biến trong recipe "ins" (ví dụ: `self.inputs.input_bit_register_64`).
*   `watchdog` (RTDEInputObject): Đối tượng tương tự `inputs` nhưng dành cho recipe "watchdog" (ví dụ: `self.watchdog.input_int_register_0`).

## 3. Phương thức của Class

### 3.1. `__init__(self, robot_ip="192.168.1.100", robot_port=30004)`

*   **Mục đích:** Khởi tạo đối tượng `RTDE_ed`, thiết lập kết nối với robot, và cấu hình các recipes RTDE.
*   **Tham số:**
    *   `robot_ip` (str, tùy chọn): Địa chỉ IP của robot. Mặc định là "192.168.1.100".
    *   `robot_port` (int, tùy chọn): Cổng RTDE của robot. Mặc định là 30004.
*   **Hoạt động:**
    1.  In thông báo khởi tạo.
    2.  Lưu trữ `ROBOT_HOST` và `ROBOT_PORT`.
    3.  Đọc file cấu hình `config_filename` (mặc định là "data.xml") bằng `rtde_config.ConfigFile`.
    4.  Trích xuất tên và kiểu dữ liệu cho các recipes "outs", "ins", và "watchdog" từ file config.
    5.  Tạo đối tượng `rtde.RTDE` và gọi `self.con.connect()` để kết nối đến robot.
    6.  Nếu kết nối ban đầu thất bại, thử kết nối lại sau 1 giây.
    7.  Gửi cấu hình output (`self.con.send_output_setup`) để robot biết cần gửi những dữ liệu gì.
    8.  Gửi cấu hình input (`self.con.send_input_setup`) để Python có thể gửi dữ liệu. Lưu lại các đối tượng `self.inputs` và `self.watchdog` để truy cập các thanh ghi input.
    9.  Gọi `self.init_rtde_parameters()` để đặt giá trị ban đầu cho các thanh ghi input.
    10. In thông báo hoàn tất thiết lập.
    11. Bắt đầu quá trình đồng bộ hóa dữ liệu (`self.con.send_start()`). Nếu thất bại, thử `self.reconnect()` sau mỗi 3 giây cho đến khi thành công.

### 3.2. `init_rtde_parameters(self)`

*   **Mục đích:** Đặt giá trị khởi tạo cho tất cả các thanh ghi input (bit, double, integer) mà Python sẽ gửi đến robot. Điều này đảm bảo robot nhận được giá trị mặc định hợp lệ khi kết nối bắt đầu.
*   **Hoạt động:**
    *   **Thanh ghi Bit (input_bit_register_64 đến input_bit_register_75):** Tất cả được đặt thành `False`. Các comment trong code giải thích mục đích dự kiến của từng thanh ghi (ví dụ: D-pad, các nút bấm Z-up, Rz-up,...).
    *   **Thanh ghi Double (input_double_register_24 đến input_double_register_31):** Tất cả được đặt thành `0.0`. Các comment giải thích mục đích dự kiến (ví dụ: các trục analog của joystick).
    *   **Thanh ghi Integer (`input_int_register_24`):** Được đặt thành `0`. Comment giải thích các giá trị số nguyên có thể đại diện cho các đối tượng hoặc trạng thái khác nhau được phát hiện bởi hệ thống vision.
    *   **Watchdog (`input_int_register_0`):** Được đặt thành `0`. Đây là một biến thường được tăng lên ở phía Python và gửi đến robot để robot biết rằng kết nối RTDE vẫn còn hoạt động.

### 3.3. `receive_data_from_robot(self)`

*   **Mục đích:** Nhận dữ liệu output từ robot.
*   **Hoạt động:**
    *   Gọi `self.con.receive()` để lấy gói dữ liệu mới nhất từ robot.
    *   **Trả về:** Giá trị của thanh ghi `output_bit_register_64` từ gói dữ liệu nhận được.
    *   *Lưu ý: Hàm này hiện chỉ trả về một thanh ghi cụ thể. Nó có thể cần được mở rộng để trả về nhiều giá trị hơn hoặc một đối tượng chứa tất cả dữ liệu output nếu cần.*

### 3.4. `bool_list_to_inputs(self, data, start=64)`

*   **Mục đích:** Chuyển đổi một danh sách dữ liệu boolean (từ D-pad và các nút joystick) thành các giá trị cho các thanh ghi bit input.
*   **Tham số:**
    *   `data` (list): Danh sách các giá trị. Hai phần tử đầu tiên được giả định là từ D-pad (có thể là -1, 0, 1), các phần tử còn lại là trạng thái nút (0 hoặc 1).
    *   `start` (int, tùy chọn): Chỉ số thanh ghi bit bắt đầu. Mặc định là 64.
*   **Hoạt động:**
    *   **Xử lý D-pad (hai phần tử đầu của `data`):**
        *   Mỗi giá trị D-pad (ví dụ `data[0]` cho X-axis) được ánh xạ vào *hai* thanh ghi bit liên tiếp.
        *   Nếu `value > 0` (ví dụ: D-pad lên), thanh ghi `start + i*2` là `True`, thanh ghi `start + i*2 + 1` là `False`.
        *   Nếu `value < 0` (ví dụ: D-pad xuống), thanh ghi `start + i*2` là `False`, thanh ghi `start + i*2 + 1` là `True`.
        *   Nếu `value == 0`, cả hai thanh ghi là `False`.
    *   **Xử lý các nút còn lại (từ phần tử thứ ba của `data`):**
        *   Mỗi giá trị nút được ánh xạ vào một thanh ghi bit bắt đầu từ 68.
        *   Nếu giá trị nút khác 0, thanh ghi bit tương ứng là `True`, ngược lại là `False`.

### 3.5. `double_list_to_inputs(self, data, start=24)`

*   **Mục đích:** Chuyển đổi một danh sách dữ liệu số thực (từ các trục analog của joystick) thành các giá trị cho các thanh ghi double input.
*   **Tham số:**
    *   `data` (list): Danh sách các giá trị số thực.
    *   `start` (int, tùy chọn): Chỉ số thanh ghi double bắt đầu. Mặc định là 24.
*   **Hoạt động:** Lặp qua danh sách `data` và gán từng giá trị cho thanh ghi `input_double_register` tương ứng.

### 3.6. `send_data_to_robot_joystick(self, bool_data, double_data)`

*   **Mục đích:** Gửi dữ liệu trạng thái joystick (boolean và double) đến robot.
*   **Tham số:**
    *   `bool_data` (list): Danh sách dữ liệu boolean (từ D-pad và nút).
    *   `double_data` (list): Danh sách dữ liệu số thực (từ trục analog).
*   **Hoạt động:**
    1.  Gọi `self.bool_list_to_inputs(bool_data)` để cập nhật các thanh ghi bit.
    2.  Gọi `self.double_list_to_inputs(double_data)` để cập nhật các thanh ghi double.
    3.  Gọi `self.con.send(self.inputs)` để gửi toàn bộ đối tượng `self.inputs` (chứa tất cả các giá trị thanh ghi input đã cập nhật) đến robot.
    4.  In thông báo thành công.

### 3.7. `send_data_to_robot_vision(self, data)`

*   **Mục đích:** Gửi dữ liệu từ hệ thống vision (ví dụ: ID lớp đối tượng) đến robot.
*   **Tham số:**
    *   `data` (int hoặc str): Dữ liệu cần gửi.
        *   Nếu là `int`, giá trị này được gán trực tiếp cho `self.inputs.input_int_register_24`.
        *   Nếu là `str` (ví dụ: "class_1"), chương trình cố gắng ánh xạ chuỗi này thành một số nguyên (1 đến 5) và gán cho `input_int_register_24`.
*   **Hoạt động:**
    1.  Cập nhật `self.inputs.input_int_register_24` dựa trên `data`.
    2.  Gửi `self.inputs` đến robot.
    3.  Tăng giá trị của thanh ghi watchdog (`self.watchdog.input_int_register_0 += 1`).
    4.  Gửi `self.watchdog` đến robot.
    5.  In thông báo thành công.

### 3.8. `reconnect(self)`

*   **Mục đích:** Cố gắng thiết lập lại kết nối RTDE nếu kết nối hiện tại bị mất.
*   **Hoạt động:**
    1.  Ngắt kết nối hiện tại (`self.con.disconnect()`).
    2.  Chờ một chút.
    3.  Kết nối lại (`self.con.connect()`).
    4.  Chờ một chút.
    5.  Thiết lập lại recipes output và input.
    6.  Khởi tạo lại các tham số RTDE (`self.init_rtde_parameters()`).
    7.  **Quan trọng:** Cố gắng bắt đầu lại đồng bộ hóa dữ liệu (`self.con.send_start()`). Nếu thất bại, in lỗi nghiêm trọng và raise `RuntimeError`.

### 3.9. `disconnect_rtde(self)`

*   **Mục đích:** Ngắt kết nối RTDE với robot một cách an toàn.
*   **Hoạt động:** Gọi `self.con.disconnect()` và in thông báo.

## 4. File cấu hình `data.xml` (Bắt buộc)

Hoạt động của class này phụ thuộc hoàn toàn vào sự tồn tại và nội dung chính xác của file `data.xml`. File này phải được đặt cùng thư mục với script Python hoặc đường dẫn phải được chỉ định đúng.

**Nội dung file `data.xml` phải định nghĩa các "recipes" sau:**

*   **Recipe "outs":** Định nghĩa các biến mà robot sẽ gửi về Python (ví dụ: `output_bit_register_64` được sử dụng trong `receive_data_from_robot`).
*   **Recipe "ins":** Định nghĩa các biến mà Python sẽ gửi đến robot. Tên các biến này phải khớp với tên các thuộc tính được truy cập trong `self.inputs` (ví dụ: `input_bit_register_64`, `input_double_register_24`, `input_int_register_24`).
*   **Recipe "watchdog":** Định nghĩa biến watchdog (ví dụ: `input_int_register_0`) mà Python sẽ gửi đến robot.

**Ví dụ một phần nội dung `data.xml` có thể trông như sau:**
```xml
<rtde_config>
    <recipe key="outs">
        <field name="output_bit_register_64" type="UINT8"/>
        <!-- Thêm các biến output khác nếu cần -->
    </recipe>
    <recipe key="ins">
        <field name="input_bit_register_64" type="UINT8"/>
        <field name="input_bit_register_65" type="UINT8"/>
        <!-- ... đến input_bit_register_75 ... -->
        <field name="input_double_register_24" type="DOUBLE"/>
        <!-- ... đến input_double_register_31 ... -->
        <field name="input_int_register_24" type="INT32"/>
    </recipe>
    <recipe key="watchdog">
        <field name="input_int_register_0" type="INT32"/>
    </recipe>
</rtde_config>
