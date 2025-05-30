# Dự án Điều khiển Robot UR Tích hợp Joystick và Vision (VIMF_BD_2025)

## 1. Giới thiệu

Dự án này nhằm mục đích xây dựng một hệ thống cho phép điều khiển robot Universal Robots (UR) thông qua một thiết bị joystick/gamepad và tích hợp khả năng xử lý tín hiệu từ hệ thống thị giác máy tính (vision). Giao tiếp với robot được thực hiện qua giao thức Real-Time Data Exchange (RTDE).

Hệ thống được quản lý chủ yếu thông qua file `main.py` (cung cấp giao diện người dùng và điều phối) và `exchange_data.py` (xử lý giao tiếp RTDE chi tiết).

## 2. Cấu trúc Thư mục
VIMF_BD_2025/
├── data.xml # File cấu hình RTDE recipes
├── doc/ # Thư mục chứa tài liệu
│ ├── exchange_data.md # Tài liệu cho module exchange_data
│ └── main-node.md # Tài liệu cho file main.py
├── exchange_data.py # Module chính chứa class RTDE_ed để xử lý giao tiếp RTDE
├── init.py # Đánh dấu thư mục là một package Python
├── lib/ # Thư mục chứa các thư viện bên ngoài hoặc đã build (nếu có)
│ └── build/
├── main.py # File Python chính của ứng dụng, chứa GUI, logic đọc joystick, và điều phối
├── pycache/ # Thư mục cache bytecode của Python
├── README.md # File tài liệu này
├── rtde/ # Thư viện RTDE chính thức của Universal Robots (hoặc bản tùy chỉnh)
│ ├── csv_binary_writer.py
│ ├── csv_reader.py
│ ├── csv_writer.py
│ ├── init.py
│ ├── pycache/
│ ├── rtde_config.py # Module xử lý file cấu hình RTDE XML
│ ├── rtde.py # Module RTDE chính
│ └── serialize.py # Module hỗ trợ serialize/deserialize dữ liệu RTDE
└── rtde_instance.py # (File này không cần thiết)


## 3. Các thành phần chính và Chức năng

### 3.1. `main.py`
*   **Giao diện Người dùng (GUI):** Xây dựng bằng Tkinter, cho phép người dùng:
    *   Nhập địa chỉ IP của robot UR.
    *   Chọn chỉ số camera để sử dụng.
    *   Cung cấp các nút để kiểm tra kết nối, xem trước camera, và khởi chạy chương trình điều khiển chính.
*   **Xử lý Joystick:**
    *   Sử dụng thư viện `pygame` để khởi tạo và đọc dữ liệu từ thiết bị joystick/gamepad được kết nối.
    *   Thu thập trạng thái của các trục analog, nút bấm, và D-pad.
    *   Chuẩn bị dữ liệu joystick thành các định dạng phù hợp (thường là danh sách boolean và số thực) để gửi đến robot.
*   **Logic Điều phối:**
    *   Khởi tạo và quản lý các đối tượng cần thiết (ví dụ: camera, đối tượng RTDE từ `exchange_data.py`).
    *   Điều phối luồng hoạt động chính của ứng dụng khi người dùng nhấn nút "START".
    *   Có thể chứa logic xử lý vision cơ bản hoặc gọi các hàm từ một module vision riêng biệt (nếu có).
*   **Ví dụ chức năng trong `main.py` (dựa trên code trước đó):**
    *   `init_camera()`: Khởi tạo camera.
    *   `start_program_hand_detect()` (hoặc tên tương tự): Vòng lặp chính để đọc joystick, xử lý vision (ví dụ: phát hiện bàn tay, ước tính khoảng cách), và gửi dữ liệu đến robot qua RTDE.
    *   `conn_to_robot()`: Kiểm tra kết nối RTDE.
    *   `show_video()`: Hiển thị luồng camera thô.
    *   `GUI()` / `create_GUI()`: Các hàm xây dựng giao diện Tkinter.

### 3.2. `exchange_data.py`
*   Chứa class `RTDE_ed` (hoặc tên tương tự) chịu trách nhiệm cho toàn bộ giao tiếp RTDE:
    *   Thiết lập kết nối với robot UR sử dụng địa chỉ IP và cổng được cung cấp.
    *   Đọc và diễn giải file cấu hình `data.xml` để xác định các "recipes" (biến dữ liệu) sẽ được trao đổi.
    *   Gửi cấu hình input/output đến robot.
    *   Bắt đầu và duy trì phiên đồng bộ hóa dữ liệu RTDE.
    *   Cung cấp các phương thức để:
        *   Gửi dữ liệu từ joystick đến các thanh ghi input của robot (ví dụ: `send_data_to_robot_joystick`).
        *   Gửi dữ liệu từ hệ thống vision đến các thanh ghi input của robot (ví dụ: `send_data_to_robot_vision`).
        *   Nhận dữ liệu từ các thanh ghi output của robot (ví dụ: `receive_data_from_robot`).
    *   Xử lý các tình huống mất kết nối và cố gắng kết nối lại (`reconnect`).
    *   Cung cấp phương thức để ngắt kết nối RTDE một cách an toàn (`disconnect_rtde`).

### 3.3. `data.xml`
*   File cấu hình XML quan trọng, định nghĩa các "recipes" cho giao tiếp RTDE.
*   Một recipe là một tập hợp các biến (fields) mà robot sẽ gửi đi (output) hoặc có thể nhận vào (input).
*   Các biến này được ánh xạ tới các thanh ghi cụ thể trên bộ điều khiển của robot (ví dụ: `input_bit_register_64`, `input_double_register_24`, `output_int_register_0`).
*   **Rất quan trọng:** Nội dung của file này phải **khớp chính xác** với cấu hình RTDE trên chương trình robot (PolyScope) và cách class `RTDE_ed` trong `exchange_data.py` truy cập (đọc/ghi) các thanh ghi này.

### 3.4. Thư mục `rtde/`
*   Chứa mã nguồn của thư viện `rtde` Python chính thức từ Universal Robots. Thư viện này cung cấp các công cụ nền tảng để thực hiện giao tiếp RTDE.
    *   `rtde.py`: Chứa class `RTDE` chính.
    *   `rtde_config.py`: Chứa class `ConfigFile` để đọc file XML.
    *   `serialize.py`: Hỗ trợ việc đóng gói và giải nén dữ liệu cho giao thức RTDE.

### 3.5. `rtde_instance.py` (Nếu vẫn còn)
*   Nếu file này vẫn tồn tại ở thư mục gốc, vai trò của nó cần được làm rõ. Nó có thể là một nỗ lực để tạo ra một đối tượng RTDE singleton hoặc một cách khác để quản lý instance kết nối. Tuy nhiên, với `exchange_data.py` chứa class `RTDE_ed`, file này có thể không còn cần thiết hoặc cần được tích hợp cẩn thận.

## 4. Cài đặt và Chạy

### 4.1. Yêu cầu
*   Python 3.x
*   Thư viện `pygame`: `pip install pygame`
*   Thư viện `numpy`: `pip install numpy`
*   Thư viện `opencv-python`: `pip install opencv-python`
*   Thư viện `cvzone` (nếu sử dụng HandDetector): `pip install cvzone`
*   Thư viện `rtde` của Universal Robots (đã có trong thư mục `rtde/`). Đảm bảo thư mục này có thể được import bởi Python (ví dụ, nằm trong cùng thư mục làm việc hoặc được thêm vào `PYTHONPATH`).
*   Robot UR được kết nối mạng, chạy chương trình PolyScope có cấu hình RTDE phù hợp với `data.xml`.
*   Một thiết bị joystick/gamepad được kết nối với máy tính.

### 4.2. Cấu hình
1.  **`data.xml`**: Kiểm tra và đảm bảo file này định nghĩa chính xác các biến input/output mà `exchange_data.py` và chương trình robot sử dụng.
2.  **Địa chỉ IP Robot:** Người dùng sẽ nhập qua GUI trong `main.py`. Đảm bảo class trong `exchange_data.py` sử dụng IP này hoặc có cơ chế nhận IP.

### 4.3. Chạy ứng dụng
Thực thi file `main.py` từ terminal:
```bash
python main.py
