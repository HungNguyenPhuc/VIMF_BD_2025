# Dự án VIMF_BD_2025: Điều khiển Robot UR bằng Joystick qua RTDE

## 1. Tổng quan

Dự án này cung cấp một giải pháp để điều khiển robot Universal Robots (UR) từ xa bằng cách sử dụng một thiết bị joystick/gamepad tiêu chuẩn. Giao tiếp giữa máy tính chạy script điều khiển và robot UR được thực hiện thông qua giao thức Real-Time Data Exchange (RTDE), cho phép truyền dữ liệu trạng thái joystick (trục, nút, D-pad) đến robot một cách hiệu quả.

Hệ thống bao gồm hai thành phần chính:
*   Một script Python (`main.py`) đọc dữ liệu từ joystick và gửi đi.
*   Một module Python (`exchange_data.py`) đóng gói logic thiết lập và quản lý kết nối RTDE.

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

## 3. Các thành phần chính

*   **`main.py`**:
    *   Sử dụng thư viện `pygame` để phát hiện và đọc dữ liệu từ joystick được kết nối.
    *   Thu thập trạng thái của các trục (analog sticks), nút bấm, và D-pad.
    *   Định dạng dữ liệu joystick thành các danh sách giá trị boolean và số thực.
    *   Sử dụng module `exchange_data.py` để gửi dữ liệu này đến robot UR qua RTDE.
    *   Xử lý việc ngắt chương trình (Ctrl+C) và dọn dẹp tài nguyên.
*   **`exchange_data_module.py`**:
    *   Định nghĩa class `RTDE_ed` để quản lý kết nối RTDE.
    *   Đọc cấu hình "recipes" (các biến dữ liệu sẽ được trao đổi) từ file `data.xml`.
    *   Thiết lập các kênh input và output RTDE với robot.
    *   Cung cấp các phương thức để gửi dữ liệu đã được định dạng (ví dụ: từ joystick) đến các thanh ghi input của robot.
    *   Cung cấp phương thức để nhận dữ liệu từ các thanh ghi output của robot.
    *   Xử lý việc kết nối, ngắt kết nối, và cố gắng kết nối lại nếu mất tín hiệu.
*   **`data.xml`**:
    *   **File cấu hình cốt lõi** cho giao tiếp RTDE.
    *   Định nghĩa chính xác những biến dữ liệu nào (tên và kiểu) sẽ được truyền giữa script Python và chương trình trên robot UR.
    *   Nội dung của file này phải khớp với các thanh ghi mà `exchange_data_module.py` truy cập và chương trình trên robot sử dụng.
*   **Thư mục `rtde/`**:
    *   Chứa mã nguồn của thư viện `python-rtde`.

## 4. Yêu cầu cài đặt

### 4.1. Phần mềm

*   **Python 3.x**
*   **Thư viện Python:**
    *   `pygame`:
        ```bash
        pip install pygame
        ```
    *   Thư viện `rtde` của Universal Robots: Dự án đã bao gồm một bản sao cục bộ trong thư mục `rtde/`. Đảm bảo thư mục này có thể được Python import (ví dụ: nằm trong `PYTHONPATH` hoặc script chạy từ thư mục gốc của dự án). Nếu không, có thể cài đặt qua pip:
        ```bash
        pip install rtde
        ```

### 4.2. Phần cứng

*   Máy tính chạy Python.
*   Robot Universal Robots (UR) hỗ trợ giao tiếp RTDE.
*   Joystick/Gamepad tương thích với `pygame`.

### 4.3. Cấu hình Robot UR

*   **Địa chỉ IP Robot:** Robot cần có địa chỉ IP tĩnh và có thể truy cập được từ máy tính chạy script.
*   **Giao diện RTDE:** Phải được kích hoạt trên robot.
*   **Chương trình Robot (PolyScope):** Cần có một chương trình trên robot được thiết kế để:
    *   Đọc các giá trị từ các thanh ghi input RTDE mà script Python (`exchange_data_module.py`) gửi đến (ví dụ: `input_bit_register_64` đến `_75`, `input_double_register_24` đến `_31`).
    *   Diễn giải các giá trị này để điều khiển chuyển động hoặc hành động của robot.
    *   (Tùy chọn) Ghi dữ liệu vào các thanh ghi output RTDE nếu script Python cần đọc lại trạng thái.
    *   Xử lý watchdog (đọc `input_int_register_0` từ `exchange_data_module.py`) để giám sát kết nối.

## 5. Hướng dẫn sử dụng

1.  **Thiết lập `data.xml`:**
    *   Chỉnh sửa file `data.xml` để định nghĩa chính xác các biến input và output RTDE. Tên và kiểu dữ liệu phải khớp với những gì `exchange_data_module.py` và chương trình trên robot sử dụng. Xem chi tiết trong `doc/exchange_data_module.md`.
2.  **Cấu hình IP Robot:**
    *   Mở file `exchange_data_module.py`.
    *   Trong hàm `__init__` của class `RTDE_ed`, chỉnh sửa giá trị mặc định của `robot_ip` (hiện là "192.168.1.100") nếu cần.
3.  **Kết nối Phần cứng:**
    *   Kết nối robot UR vào mạng.
    *   Kết nối joystick/gamepad vào máy tính.
4.  **Chạy chương trình trên Robot:** Đảm bảo chương trình Polyscope tương ứng đang chạy trên robot và sẵn sàng nhận lệnh qua RTDE.
5.  **Chạy Script Python:**
    *   Mở terminal hoặc command prompt.
    *   Di chuyển đến thư mục gốc của dự án (`VIMF_BD_2025`).
    *   Chạy lệnh:
        ```bash
        python joystick_controller.py
        ```
6.  **Điều khiển:**
    *   Chương trình sẽ phát hiện joystick đầu tiên.
    *   Di chuyển các trục, nhấn nút, và sử dụng D-pad trên joystick. Trạng thái của chúng sẽ được in ra terminal và được gửi đến robot.
    *   Quan sát hành vi của robot (phụ thuộc vào chương trình đang chạy trên robot).
7.  **Thoát:** Nhấn Ctrl+C trong terminal để dừng script.

## 6. Tài liệu chi tiết cho các Module

*   **`doc/exchange_data_module.md`**: Tài liệu chi tiết về class `RTDE_ed` và cách nó xử lý giao tiếp RTDE.
*   **`doc/joystick_controller.md`**: Tài liệu chi tiết về script `joystick_controller.py`, cách đọc dữ liệu joystick và gửi qua `exchange_data_module`.

## 7. Gỡ lỗi và Các vấn đề thường gặp

*   **"Không có joystick nào được kết nối."**: Kiểm tra kết nối joystick.
*   **Lỗi kết nối RTDE:**
    *   Kiểm tra IP robot, kết nối mạng.
    *   Đảm bảo RTDE được kích hoạt trên robot.
    *   Kiểm tra `data.xml` và chương trình robot có khớp với các thanh ghi được sử dụng trong `exchange_data_module.py` không.
*   **Robot không phản hồi dữ liệu joystick:**
    *   Kiểm tra chương trình trên robot (PolyScope) xem nó có đang đọc đúng các thanh ghi RTDE không.
    *   Kiểm tra logic diễn giải dữ liệu joystick thành hành động của robot.

## 8. Hướng phát triển tiềm năng

*   Thêm giao diện người dùng (GUI) để chọn joystick, hiển thị trạng thái, và cấu hình IP robot.
*   Cho phép ánh xạ (mapping) linh hoạt các nút/trục joystick thành các hành động cụ thể của robot.
*   Cải thiện xử lý deadzone cho các trục analog của joystick.
*   Tích hợp phản hồi từ robot (ví dụ: vị trí hiện tại, trạng thái) và hiển thị cho người dùng.
