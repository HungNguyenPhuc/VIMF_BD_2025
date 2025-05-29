# Tài liệu: Ứng dụng Phát hiện Bàn tay và Điều khiển Robot qua RTDE

## 1. Giới thiệu chung

Ứng dụng Python này được thiết kế để thực hiện các chức năng sau:
1.  **Hiển thị Giao diện Người dùng (GUI):** Cung cấp một giao diện đơn giản bằng Tkinter để người dùng nhập địa chỉ IP của robot Universal Robots (UR) và chọn camera.
2.  **Kết nối Robot qua RTDE:** Thiết lập kết nối Real-Time Data Exchange (RTDE) với robot UR để có thể gửi và nhận dữ liệu.
3.  **Phát hiện Bàn tay:** Sử dụng camera để phát hiện bàn tay người dùng trong thời gian thực.
4.  **Ước tính Khoảng cách:** Dựa trên kích thước của bàn tay được phát hiện trong ảnh, ước tính khoảng cách từ camera đến bàn tay.
5.  **(Ngụ ý) Điều khiển Robot:** Mặc dù logic điều khiển robot dựa trên khoảng cách bàn tay chưa được triển khai đầy đủ trong phần `start_program_hand_detect`, nền tảng RTDE đã được thiết lập để có thể gửi dữ liệu (ví dụ: khoảng cách) đến robot.

Quy trình chính là người dùng nhập IP robot, chọn camera, sau đó nhấn "START" để khởi chạy phần phát hiện bàn tay và giao tiếp RTDE.

## 2. Các thành phần chính và Module sử dụng

### 2.1. Giao diện người dùng (GUI - Tkinter)

*   **Cửa sổ chính (`app`):** Có tiêu đề "Hoplongtech" và kích thước 800x600.
*   **Box 1 (Robot Setting):**
    *   Tiêu đề: "Robot setting".
    *   Nhãn "Robot IP".
    *   Ô nhập liệu (`IP_entry`): Để người dùng nhập địa chỉ IP của robot.
    *   Nút "Check": Gọi hàm `conn_to_robot` để kiểm tra kết nối nhanh đến robot (chỉ kết nối rồi ngắt).
*   **Box 2 (Choose camera):**
    *   Tiêu đề: "Choose camera".
    *   Ô nhập liệu (`CAM_entry`): Để người dùng nhập chỉ số của camera (ví dụ: 0, 1,...).
    *   Nút "View": Gọi hàm `show_video` để hiển thị luồng video trực tiếp từ camera đã chọn trong một cửa sổ OpenCV riêng biệt.
*   **Nút "START":** Gọi hàm `start_program` để bắt đầu logic chính (phát hiện bàn tay và RTDE).

### 2.2. Thư viện và Module ngoài

*   **`cv2` (OpenCV-Python)**: Dùng cho tất cả các tác vụ liên quan đến camera và xử lý ảnh cơ bản.
    *   `cv2.VideoCapture`: Mở và đọc luồng video từ camera.
    *   `cap.set(3, wwidth)`, `cap.set(4, wheight)`: Cố gắng đặt độ phân giải cho camera (có thể không được hỗ trợ bởi mọi camera).
    *   `cv2.flip`: Lật ảnh (để tạo hiệu ứng gương).
    *   `cv2.imshow`, `cv2.waitKey`, `cv2.destroyAllWindows`: Hiển thị ảnh/video trong cửa sổ OpenCV.
*   **`cvzone.HandTrackingModule.HandDetector`**:
    *   Sử dụng module `HandDetector` từ thư viện `cvzone` để phát hiện bàn tay và các điểm mốc (landmarks) trên bàn tay.
    *   `detectionCon=0.8`: Ngưỡng tin cậy để coi một phát hiện là bàn tay.
    *   `maxHands=1`: Chỉ phát hiện tối đa một bàn tay.
*   **`rtde`, `rtde.rtde_config`**:
    *   Thư viện Python chính thức của Universal Robots để giao tiếp qua giao thức RTDE.
    *   `rtde.RTDE`: Class chính để tạo đối tượng kết nối.
    *   `rtde_config.ConfigFile`: Dùng để đọc cấu hình "recipes" (các biến dữ liệu sẽ được trao đổi) từ một file XML.
*   **`numpy`**: Sử dụng cho các phép toán mảng, đặc biệt là `np.polyfit` để nội suy hàm tính khoảng cách.
*   **`math`**: Sử dụng cho các phép toán cơ bản như `math.sqrt`.
*   **`tkinter`**: Xây dựng giao diện đồ họa người dùng.
*   **`threading`**: (Đã import nhưng chưa thấy sử dụng trong code bạn cung cấp cho việc cập nhật video lên GUI Tkinter. `start_program_hand_detect` chạy trong luồng chính sau khi GUI bị hủy).

### 2.3. Các biến toàn cục

*   `wwidth`, `wheight`: Lưu trữ chiều rộng và chiều cao màn hình (lấy từ cửa sổ Tkinter ban đầu).
*   `camera_index`: Chỉ số camera được người dùng chọn, được sử dụng bởi `init_camera` và `show_video`.
*   `IP_entry`: Đối tượng ô nhập liệu IP (được trả về từ `create_GUI` và truyền đi).

## 3. Các hàm chính

### 3.1. Phát hiện Bàn tay và Ước tính Khoảng cách

#### `init_camera(wwidth, wheight)`

*   **Mục đích:** Khởi tạo và mở camera được chọn bởi `camera_index`.
*   **Hoạt động:**
    *   Tạo đối tượng `cv2.VideoCapture` với `camera_index`.
    *   Cố gắng đặt chiều rộng (`wwidth`) và chiều cao (`wheight`) cho camera.
*   **Trả về:** Đối tượng `cap` (VideoCapture).

#### `start_program_hand_detect()`

*   **Mục đích:** Hàm chính thực hiện vòng lặp phát hiện bàn tay, ước tính khoảng cách, và (theo thiết kế) sẽ giao tiếp với robot.
*   **Hoạt động:**
    1.  **Khởi tạo RTDE:** Gọi `init_rtde(IP_entry)` để kết nối với robot và thiết lập các "recipes" (luồng dữ liệu vào/ra).
    2.  **Khởi tạo Camera:** Gọi `init_camera(wwidth, wheight)`.
    3.  **Khởi tạo Hand Detector:** Tạo đối tượng `HandDetector` từ `cvzone`.
    4.  **Nội suy Khoảng cách:**
        *   Định nghĩa một tập các điểm dữ liệu `x` (khoảng cách pixel giữa hai điểm mốc trên bàn tay) và `y` (khoảng cách thực tế tương ứng tính bằng cm).
        *   Sử dụng `np.polyfit(x, y, 2)` để tìm các hệ số (A, B, C) của một đa thức bậc 2 (`y = Ax^2 + Bx + C`) phù hợp nhất với dữ liệu này. Hàm này sẽ được dùng để ước tính khoảng cách cm từ khoảng cách pixel.
    5.  **Vòng lặp Chính:**
        *   Đọc frame từ camera.
        *   Lật frame theo chiều ngang (`cv2.flip`).
        *   Sử dụng `detector.findHands(img)` để tìm bàn tay và các điểm mốc.
        *   Nếu tìm thấy bàn tay:
            *   Lấy danh sách các điểm mốc (`lmList`).
            *   Lấy tọa độ của hai điểm mốc cụ thể (ví dụ: `lmList[5]` và `lmList[17]`, thường là đầu ngón tay và gốc bàn tay).
            *   Tính khoảng cách pixel (`distane`) giữa hai điểm mốc này.
            *   Sử dụng đa thức đã nội suy (`A, B, C`) và `distane` để ước tính khoảng cách thực tế bằng cm (`distanceCM`).
            *   In ra `distanceCM` và `distane`.
            *   **(Phần thiếu sót):** Tại đây nên có logic gửi `distanceCM` (hoặc một giá trị điều khiển dựa trên nó) đến robot qua RTDE (sử dụng các đối tượng `con`, `setp`, `watchdog` đã khởi tạo).
        *   Hiển thị ảnh (`img`) với bàn tay đã được vẽ (nếu có) trong một cửa sổ OpenCV tên là "Hand detect".
        *   Chờ một phím nhấn (`cv2.waitKey(1)`). Vòng lặp này sẽ chạy vô hạn cho đến khi bị ngắt (ví dụ: Ctrl+C).

### 3.2. Giao tiếp RTDE với Robot UR

#### `init_rtde(IP_entry)`

*   **Mục đích:** Thiết lập kết nối RTDE ban đầu với robot UR, định nghĩa và gửi các "recipes" (cấu hình dữ liệu trao đổi).
*   **Hoạt động:**
    1.  Lấy địa chỉ IP từ `IP_entry`.
    2.  Tạo đối tượng `rtde.RTDE` với IP và cổng 30004.
    3.  Gọi `con.connect()`.
    4.  Nếu kết nối thành công:
        *   Đọc file cấu hình RTDE (`config.xml`) để lấy định nghĩa các biến trạng thái (`state_names`, `state_types`), biến cài đặt (`setp_names`, `setp_types`), và biến giám sát (`watchdog_names`, `watchdog_types`).
        *   Gửi cấu hình output (`con.send_output_setup`) để robot bắt đầu gửi các biến trạng thái đã định nghĩa.
        *   Gửi cấu hình input (`con.send_input_setup`) để Python có thể gửi các biến cài đặt và giám sát đến robot. Hàm này trả về các đối tượng (`setp`, `watchdog`) có thể được dùng để cập nhật giá trị các biến input.
        *   Gọi `con.send_start()` để bắt đầu đồng bộ hóa dữ liệu. Nếu thất bại, hiển thị lỗi, tạm dừng và ngắt kết nối.
*   **Trả về:** `(con, setp, watchdog)` nếu thành công, `None` nếu thất bại.

#### `conn_to_robot(IP_entry)`

*   **Mục đích:** Một hàm đơn giản để kiểm tra nhanh kết nối đến robot.
*   **Hoạt động:**
    *   Lấy IP, tạo đối tượng RTDE, kết nối.
    *   Hiển thị thông báo thành công hoặc lỗi.
    *   **Luôn ngắt kết nối (`con.disconnect()`) sau khi kiểm tra.**

### 3.3. Quản lý GUI và Chương trình

#### `start_program(app)`

*   **Mục đích:** Được gọi khi nhấn nút "START". Khởi chạy logic chính và đóng GUI.
*   **Hoạt động:**
    *   Gọi `start_program_hand_detect()`. Hàm này sẽ chạy vòng lặp vô hạn của nó.
    *   Gọi `app.destroy()` để đóng cửa sổ Tkinter.

#### `show_video(CAM_entry)`

*   **Mục đích:** Hiển thị luồng video thô từ camera đã chọn trong một cửa sổ OpenCV riêng biệt.
*   **Hoạt động:**
    *   Lấy chỉ số camera từ `CAM_entry`.
    *   Mở `cv2.VideoCapture`.
    *   Vòng lặp đọc frame và hiển thị bằng `cv2.imshow`.
    *   Thoát vòng lặp khi nhấn 'q'.
    *   Giải phóng camera và đóng cửa sổ.

#### `GUI(app)`

*   **Mục đích:** Xây dựng các thành phần giao diện người dùng (ô nhập liệu, nút bấm) trên cửa sổ `app` Tkinter.
*   **Hoạt động:** Sử dụng các widget `Canvas`, `Label`, `Entry`, `Button` của Tkinter để tạo hai box chính cho cài đặt robot và chọn camera, cùng với nút "START".
*   **Trả về:** Các đối tượng `IP_entry` và `CAM_entry` để có thể truy cập giá trị của chúng từ các hàm khác.

#### `create_GUI()`

*   **Mục đích:** Hàm khởi tạo chính cho GUI.
*   **Hoạt động:**
    *   Tạo cửa sổ Tkinter gốc (`app = Tk()`).
    *   Đặt tiêu đề và kích thước.
    *   Lấy kích thước màn hình (`wwidth`, `wheight`).
    *   Gọi `GUI(app)` để vẽ các widget.
*   **Trả về:** `(app, wwidth, wheight, IP_entry)`.

## 4. Luồng hoạt động của người dùng và chương trình

1.  Chạy script Python. Hàm `create_GUI()` được gọi, tạo và hiển thị cửa sổ Tkinter.
2.  Người dùng nhập địa chỉ IP của robot vào `IP_entry`.
3.  (Tùy chọn) Người dùng nhấn "Check" để gọi `conn_to_robot` và kiểm tra kết nối nhanh.
4.  Người dùng nhập chỉ số camera vào `CAM_entry`.
5.  (Tùy chọn) Người dùng nhấn "View" để gọi `show_video` và xem luồng camera thô.
6.  Người dùng nhấn "START":
    *   Hàm `start_program(app)` được gọi.
    *   Bên trong `start_program`, `start_program_hand_detect()` được gọi.
        *   `init_rtde()`: Kết nối RTDE với robot, thiết lập recipes.
        *   `init_camera()`: Mở camera được chọn.
        *   Vòng lặp phát hiện bàn tay bắt đầu:
            *   Đọc frame, tìm bàn tay, tính khoảng cách pixel.
            *   Ước tính khoảng cách cm.
            *   In thông tin khoảng cách.
            *   **(Thiếu):** Logic gửi dữ liệu điều khiển đến robot dựa trên khoảng cách.
            *   Hiển thị frame với thông tin phát hiện trong cửa sổ OpenCV "Hand detect".
    *   `app.destroy()`: Cửa sổ Tkinter bị đóng. Chương trình tiếp tục chạy trong vòng lặp của `start_program_hand_detect` ở terminal (hoặc nền nếu không có cửa sổ OpenCV nào được hiển thị).

## 5. Các điểm cần lưu ý và Cải tiến tiềm năng

*   **Luồng GUI và Luồng xử lý:** Hiện tại, khi `start_program_hand_detect()` được gọi, nó chạy trong luồng chính và GUI bị hủy (`app.destroy()`). Vòng lặp `while True` trong `start_program_hand_detect` sẽ chặn. Nếu muốn GUI vẫn tương tác được *trong khi* phát hiện bàn tay diễn ra, logic phát hiện bàn tay cần được chạy trong một luồng riêng biệt (tương tự như cách `update_video` được làm trong ví dụ code `GCodeApp` bạn gửi trước đó).
*   **Truyền dữ liệu RTDE:** Logic gửi dữ liệu (ví dụ: `distanceCM` hoặc một lệnh điều khiển dựa trên nó) đến robot qua các đối tượng `setp` hoặc `watchdog` của RTDE chưa được triển khai trong vòng lặp `start_program_hand_detect`.
*   **Cấu hình Camera:** `wwidth`, `wheight` được lấy từ kích thước màn hình của GUI, nhưng khi `app.destroy()` được gọi, các biến này có thể không còn ý nghĩa nếu `init_camera` được gọi sau đó hoặc trong một ngữ cảnh khác. Nên truyền trực tiếp giá trị mong muốn hoặc để camera tự chọn độ phân giải mặc định.
*   **Đóng kết nối RTDE:** Hiện tại, không có lệnh `con.disconnect()` rõ ràng khi chương trình kết thúc hoặc bị ngắt (ví dụ: Ctrl+C trong terminal sau khi GUI đóng). Nên thêm xử lý `try...finally` hoặc `atexit` để đảm bảo ngắt kết nối RTDE một cách an toàn.
*   **Đường dẫn file `config.xml`:** Đường dẫn `D:/Py program/.../config.xml` là cố định. Nên làm cho nó linh hoạt hơn (ví dụ: đặt cùng thư mục script hoặc cho phép người dùng chọn).
*   **Xử lý lỗi camera:** Nếu camera bị ngắt giữa chừng, vòng lặp đọc frame sẽ gặp lỗi.
*   **Tính toán `coff`:** Các hệ số `coff` cho việc nội suy khoảng cách được tính toán mỗi khi `start_program_hand_detect` chạy. Nếu dữ liệu `x, y` không đổi, có thể tính toán một lần và lưu lại.
*   **Sử dụng `global camera_index`:** Việc sử dụng biến global có thể làm code khó theo dõi hơn. Cân nhắc truyền `camera_index` như một tham số.
