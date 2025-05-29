import cv2
from cvzone.HandTrackingModule import HandDetector


##################################################################
#######                                                    #######
#######               SETUP HAND DETECT                    #######
#######                                                    #######
##################################################################


def init_camera(wwidth, wheight):
    cap = cv2.VideoCapture(camera_index)
    cap.set(3, wwidth)
    cap.set(4, wheight)
    return cap


def start_program_hand_detect():
    import math
    import numpy as np

    con, setp, watchdog = init_rtde(IP_entry)
    cap = init_camera(wwidth, wheight)
    # Hand Detect
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    # Find function
    x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
    y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    coff = np.polyfit(x, y, 2)  # y=Ax^2 +Bx +C

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)
        if hands:
            lmList = hands[0]["lmList"]
            x1, y1 = lmList[5][:2]
            x2, y2 = lmList[17][:2]
            distane = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            A, B, C = coff
            distanceCM = A * distane**2 + B * distane + C
            print(distanceCM, distane)
        cv2.imshow("Hand detect", img)

        cv2.waitKey(1)


##################################################################
#######                                                    #######
#######                  SETUP GUI                         #######
#######                                                    #######
##################################################################
def init_rtde(IP_entry):
    from rtde import rtde
    from rtde import rtde_config
    from tkinter import messagebox

    ROBOT_HOST = str(IP_entry.get())
    ROBOT_PORT = 30004

    con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
    con.connect()
    if con.is_connected():
        print("connected")
        # Open the XML file using its filename
        config_filename = "D:/Py program/VSCode/Opencv/Gumi_project/config.xml"
        conf = rtde_config.ConfigFile(config_filename)
        state_names, state_types = conf.get_recipe("state")
        setp_names, setp_types = conf.get_recipe("setp")
        watchdog_names, watchdog_types = conf.get_recipe("watchdog")
        # setup recipes
        con.send_output_setup(state_names, state_types)
        setp = con.send_input_setup(setp_names, setp_types)
        watchdog = con.send_input_setup(watchdog_names, watchdog_types)
        if not con.send_start():
            messagebox.showerror("Lỗi", "Lỗi kết nối RTDE! Khởi động lại chương trình")
            con.send_pause()
            con.disconnect()
        return con, setp, watchdog
    else:
        messagebox.showerror(
            "Lỗi", "Không thể kết nối với IP này, kiểm tra lại kết nối"
        )
        return None


def conn_to_robot(IP_entry):
    from rtde import rtde
    from tkinter import messagebox

    ROBOT_HOST = str(IP_entry.get())
    ROBOT_PORT = 30004

    con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
    con.connect()
    if con.is_connected():
        print("connected")
        messagebox.showinfo("Thông báo", "Đã kết nối với robot")
    else:
        messagebox.showerror(
            "Lỗi", "Không thể kết nối với IP này, kiểm tra lại địa chỉ IP"
        )
    con.disconnect()


def start_program(app):
    start_program_hand_detect()
    app.destroy()


def show_video(CAM_entry):
    global camera_index
    selected_camera = CAM_entry.get()
    camera_index = int(selected_camera)
    video_capture = cv2.VideoCapture(camera_index)

    while True:
        ret, frame = video_capture.read()
        if ret:
            cv2.imshow("Camera Video", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            print("Failed to read camera feed")
            break

    video_capture.release()
    cv2.destroyAllWindows()


def GUI(app):
    from tkinter import Canvas, Entry, Label, StringVar, Button

    ###################### Box1 ############################
    box1 = canvas = Canvas(app, width=250, height=350, bg="white")
    canvas.place(x=100, y=100)

    # Coordinates of the box1
    x2 = 250
    y2 = 400
    x1 = 0
    y1 = 0
    canvas.create_rectangle(x1, y1, x2, y2, outline="")
    # Title bg box1
    tbox1 = canvas = Canvas(app, width=250, height=60, bg="black")
    canvas.place(x=100, y=100)
    # Text of box 1
    label1 = Label(
        tbox1,
        text="Robot setting",
        font=("Aptos Display", 18, "bold"),
        foreground="white",
        background="black",
    )
    canvas.create_window(125, 15, window=label1, anchor="n")
    labelIP = Label(
        box1,
        text="Robot IP",
        font=("Aptos", 15, "bold"),
        foreground="black",
        background="white",
    )
    labelIP.place(x=90, y=150)
    # Entry for robot IP
    IP_var = StringVar
    IP_entry = Entry(
        box1,
        textvariable=IP_var,
        font=("Arial", 14),
        background="gray",
        foreground="white",
    )
    IP_entry.place(x=15, y=200)
    # Button check
    check_button = Button(
        box1,
        text="Check",
        command=lambda: conn_to_robot(IP_entry),
        width=15,
        height=2,
        bg="grey",
        fg="white",
        activebackground="white",
        activeforeground="black",
    )
    check_button.place(x=70, y=250)
    ###################### Box1 ############################
    # Box2
    box2 = canvas = Canvas(app, width=250, height=350, bg="white")
    canvas.place(x=450, y=100)

    # Coordinates of the box
    x2 = 250
    y2 = 400
    x1 = 0
    y1 = 0
    canvas.create_rectangle(x1, y1, x2, y2, outline="")
    # Title bg box2
    tbox2 = canvas = Canvas(app, width=250, height=60, bg="black")
    canvas.place(x=450, y=100)
    # Text of box 1
    label2 = Label(
        tbox2,
        text="Choose camera",
        font=("Aptos Display", 18, "bold"),
        foreground="white",
        background="black",
    )
    canvas.create_window(125, 15, window=label2, anchor="n")
    # Entry for camera
    CAM_var = StringVar
    CAM_entry = Entry(
        box2,
        textvariable=CAM_var,
        font=("Arial", 14),
        background="gray",
        foreground="white",
    )
    CAM_entry.place(x=15, y=200)
    # Button View
    check_button = Button(
        box2,
        text="View",
        command=lambda: show_video(CAM_entry),
        width=15,
        height=2,
        bg="grey",
        fg="white",
        activebackground="white",
        activeforeground="black",
    )
    check_button.place(x=70, y=250)
    ######################## Start ###########################
    # Start check
    start_button = Button(
        app,
        text="START",
        command=lambda: start_program(app),
        width=20,
        height=2,
        bg="black",
        fg="white",
        activebackground="white",
        activeforeground="black",
    )
    start_button.place(x=326, y=520)
    return IP_entry, CAM_entry


def create_GUI():
    from tkinter import Tk

    app = Tk()
    app.title("Hoplongtech")
    app.geometry("800x600")

    # Get screen width and height
    wwidth = app.winfo_screenwidth()
    wheight = app.winfo_screenheight()
    IP_entry, CAM_entry = GUI(app)
    return app, wwidth, wheight, IP_entry


camera_index = 0
app, wwidth, wheight, IP_entry = create_GUI()
app.mainloop()
