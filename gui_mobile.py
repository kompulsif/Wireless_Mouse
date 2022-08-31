from threading import Thread
from time import sleep
import tkinter.messagebox as msg
import tkinter as tk
import socket


mouse_form = tk.Tk()
mouse_form.title("Connect to PC")
mouse_form.geometry("300x400")
mouse_form.resizable(False, False)
mouse_form.config(background="black")

mouse_speed = 5
mouse_not_locked = True


def connect():
    global connection
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(3)
        connection.connect((connect_ip.get(), int(connect_port.get())))
        connection.send(b"!CONNECTED")

    except KeyboardInterrupt:
        quit()

    except BaseException:
        msg.showwarning(
            title="Arguments Error", message="Please, check server ip or port"
        )

    else:
        insert_controller_menu()
        Thread(target=server_recv_for_test, daemon=True).start()


def delete_form_items():
    for widget in mouse_form.winfo_children():
        widget.destroy()


def server_recv_for_test():
    while True:
        try:
            s_msg = connection.recv(5)
            if not s_msg:
                raise Exception

        except BaseException:
            msg.showwarning(
                title="Connection Error",
                message="Connection lost!")
            insert_connect_menu()
            break

        sleep(1)


def right_click_fun():
    connection.send(b"!RIGHT_CLICK")


def close_connection():
    try:
        connection.send(b'!CLOSE')
        sleep(0.5)
        connection.close()

    except BaseException:
        insert_connect_menu()

    finally:
        insert_connect_menu()


def close_program():
    mouse_form.destroy()
    quit()


def change_speed():
    global mouse_speed

    t = entry_set_cursor_speed.get()
    try:
        if int(t) in range(3, 41):
            mouse_speed = int(t)

        else:
            msg.showwarning(
                title="Information", message="Speed, must be between 3 and 40"
            )

    except BaseException:
        pass


def click_lock():
    global mouse_not_locked
    if mouse_not_locked:
        mouse_not_locked = False
        button_left_lock.config(text='LOCK', foreground='black')
        connection.send(b'!LOCK')

    else:
        mouse_not_locked = True
        button_left_lock.config(text='OPEN\nLOCK', foreground='blue')
        connection.send(b'!OPEN_LOCK')


def mouse_action(b):

    while moving:
        try:
            if b == button_up:
                connection.send(bytes(f"!0,-{mouse_speed}", "utf-8"))

            elif b == button_down:
                connection.send(bytes(f"!0,{mouse_speed}", "utf-8"))

            elif b == button_right:
                connection.send(bytes(f"!{mouse_speed},0", "utf-8"))

            elif b == button_left:
                connection.send(bytes(f"!-{mouse_speed},0", "utf-8"))

            elif b == button_left_click:
                connection.send(b"!LEFT_CLICK")

            elif b == button_scroll_down:
                connection.send(b"!S_DOWN")

            elif b == button_scroll_up:
                connection.send(b"!S_UP")

        except BaseException:
            msg.showwarning(title="Server Error", message="Server is closed!")
            insert_connect_menu()
            break

        sleep(0.05)


def start_action(x):
    global moving
    moving = True
    Thread(target=mouse_action, args=(x.widget,), daemon=True).start()


def stop_action(x):
    global moving
    moving = False


def insert_controller_menu():
    global button_up, button_left, button_down, button_right, \
        button_left_click, button_right_click, button_scroll_up, button_scroll_down,\
        label_cursor_speed, entry_set_cursor_speed, button_change_speed, button_close, button_left_lock

    delete_form_items()
    mouse_form.title("Controller")

    button_left_click = tk.Button(
        mouse_form, text="Left\nClick", bg="red", foreground="Yellow"
    )
    button_left_click.bind("<ButtonPress-1>", start_action)
    button_left_click.bind("<ButtonRelease-1>", stop_action)
    button_left_lock = tk.Button(
        mouse_form, text='LOCK', bg='white', foreground='blue', command=click_lock
    )

    button_right_click = tk.Button(
        mouse_form,
        text="Right\nClick",
        bg="red",
        foreground="Yellow",
        command=right_click_fun,
    )

    button_scroll_down = tk.Button(
        mouse_form, text="Scroll\nDown", bg="yellow", foreground="blue"
    )
    button_scroll_down.bind("<ButtonPress-1>", start_action)
    button_scroll_down.bind("<ButtonRelease-1>", stop_action)

    button_scroll_up = tk.Button(
        mouse_form, text="Scroll\nUp", bg="yellow", foreground="blue"
    )
    button_scroll_up.bind("<ButtonPress-1>", start_action)
    button_scroll_up.bind("<ButtonRelease-1>", stop_action)

    button_up = tk.Button(mouse_form, text="UP", bg="white")
    button_up.bind("<ButtonPress-1>", start_action)
    button_up.bind("<ButtonRelease-1>", stop_action)

    button_left = tk.Button(mouse_form, text="LEFT", bg="white")
    button_left.bind("<ButtonPress-1>", start_action)
    button_left.bind("<ButtonRelease-1>", stop_action)

    button_down = tk.Button(mouse_form, text="DOWN", bg="white")
    button_down.bind("<ButtonPress-1>", start_action)
    button_down.bind("<ButtonRelease-1>", stop_action)

    button_right = tk.Button(mouse_form, text="RIGHT", bg="white")
    button_right.bind("<ButtonPress-1>", start_action)
    button_right.bind("<ButtonRelease-1>", stop_action)

    label_cursor_speed = tk.Label(
        mouse_form, text="Cursor Speed: ", background="black", foreground="red"
    )
    entry_set_cursor_speed = tk.Entry(mouse_form, width=6)
    button_change_speed = tk.Button(
        mouse_form,
        text="Change Speed",
        bg="Yellow",
        foreground="blue",
        command=change_speed,
    )

    button_close = tk.Button(
        mouse_form,
        text='Close',
        bg='blue',
        foreground='yellow',
        command=close_connection)

    button_up.place(relx=0.4, rely=0.3, relwidth=0.2, relheight=0.15)
    button_left.place(relx=0.2, rely=0.45, relwidth=0.2, relheight=0.15)
    button_down.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.15)
    button_right.place(relx=0.6, rely=0.45, relwidth=0.2, relheight=0.15)
    button_left_lock.place(relx=0.2, rely=0.045, relwidth=0.2, relheight=0.13)
    button_left_click.place(relx=0.2, rely=0.175, relwidth=0.2, relheight=0.27)
    button_right_click.place(relx=0.6, rely=0.045, relwidth=0.2, relheight=0.4)
    button_scroll_up.place(relx=0.4, rely=0.045, relwidth=0.2, relheight=0.13)
    button_scroll_down.place(relx=0.4, rely=0.17, relwidth=0.2, relheight=0.13)
    label_cursor_speed.place(
        relx=0.1,
        rely=0.85,
        relwidth=0.3,
        relheight=0.0457)
    entry_set_cursor_speed.place(
        relx=0.40,
        rely=0.85,
        relwidth=0.2,
        relheight=0.05)
    button_change_speed.place(
        relx=0.63,
        rely=0.85,
        relwidth=0.27,
        relheight=0.053)
    button_close.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.15)


def insert_connect_menu():
    global connect_ip, connect_port, label_ip,\
        label_port, connect_button

    delete_form_items()

    label_ip = tk.Label(
        mouse_form,
        text="IP",
        background="black",
        foreground="red")
    label_ip.place(relx=0.12, rely=0.3, relheight=0.05, relwidth=0.2)
    label_port = tk.Label(
        mouse_form,
        text="PORT",
        background="black",
        foreground="red")
    label_port.place(relx=0.12, rely=0.4, relheight=0.05, relwidth=0.2)

    connect_ip = tk.Entry(mouse_form)
    connect_ip.place(relx=0.30, rely=0.3, relheight=0.05, relwidth=0.4)
    connect_port = tk.Entry(mouse_form)
    connect_port.place(relx=0.3, rely=0.4, relheight=0.05, relwidth=0.4)

    connect_button = tk.Button(mouse_form, text="CONNECT", command=connect)
    connect_button.place(relx=0.3, rely=0.5, relheight=0.05, relwidth=0.4)

    button_pr_close = tk.Button(
        mouse_form,
        text='Close Program',
        command=close_program)
    button_pr_close.place(relx=0.3, rely=0.6, relheight=0.05, relwidth=0.4)


insert_connect_menu()

mouse_form.mainloop()
