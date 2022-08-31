from tkinter import messagebox as msg
from threading import Thread
from time import sleep
import tkinter as tk
import pyautogui
import socket

server_form = tk.Tk()
server_form.title('Start Server')
server_form.geometry('300x400')
server_form.resizable(False, False)
server_form.config(background='black')
pc_screen_size = pyautogui.size()
pyautogui.FAILSAFE = False
socket_started = False
receiver_running = True
connection_completed = False
conn = None


def on_closing():
    global socket_started, receiver_running
    if msg.askokcancel('Close Program', 'Do you want to quit ?'):
        server_close()
        server_form.destroy()


def find_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]

        except BaseException:
            msg.showwarning('No Internet',
                            'Please check your internet connection')


def action_editer(x):
    if x[1:].count('!') > 0:
        i = x[1:].index('!')
        return x[1:][:i]
    return x[1:]


def test_connection(conn):
    while receiver_running:
        try:
            conn.send(b'1')
        except BaseException:
            msg.showwarning(
                title='Connection Error',
                message='Connection lost!')
            break

        sleep(1)


def server_close():
    try:
        conn.close()
        server_socket.close()
    except BaseException:
        try:
            server_socket.close()
        except BaseException:
            pass
    finally:
        socket_started = False


def init_action(action):
    x, y = pyautogui.position()
    action = action_editer(action)

    if action == 'CONNECTED':
        pass

    elif action == 'CLOSE':
        server_close()
        insert_create_menu()

    elif action == 'LOCK':
        pyautogui.mouseDown()

    elif action == 'OPEN_LOCK':
        pyautogui.mouseUp()

    elif action == 'RIGHT_CLICK':
        pyautogui.rightClick()

    elif action == 'LEFT_CLICK':
        pyautogui.leftClick()

    elif action == 'S_DOWN':
        pyautogui.scroll(-150)

    elif action == 'S_UP':
        pyautogui.scroll(150)

    else:
        try:
            new_x, new_y = action.split(',')
            if new_x == 0:
                if (y + int(new_y) in range(0, pc_screen_size[1])):
                    pyautogui.moveTo(x + int(new_x), y + int(new_y))
            else:
                pyautogui.moveTo(x + int(new_x), y + int(new_y))

        except BaseException:
            pass


def receiver():
    global server_socket, socket_started

    try:

        port_value = port.get()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip_value, int(port_value)))
        server_socket.listen(1)

    except BaseException:
        msg.showwarning(
            title='Value Error',
            message='Please, check network nonnection or PORT')

    else:
        action_button.config(text='STOP SERVER')
        port.config(state=tk.DISABLED)
        msg.showinfo('Server', 'Server is started!')
        socket_started = True
        while socket_started:
            try:
                conn, addr = server_socket.accept()
                Thread(target=test_connection, args=(conn,)).start()
                msg.showinfo('New Connection', f'New connection: {addr[0]}')
                while receiver_running:
                    try:
                        client_msg = conn.recv(100)
                        if client_msg:
                            client_msg = client_msg.decode()
                            init_action(client_msg)

                    except KeyboardInterrupt:
                        server_form.destroy()

                    except BaseException:
                        socket_started = False
                        insert_create_menu()
                        break
            except BaseException:
                break
        server_close()


def start_server(x):
    global socket_started, receiver_running
    if (not socket_started):
        receiver_running = True
        Thread(target=receiver, daemon=True).start()

    else:
        socket_started = False
        receiver_running = False
        port.config(state=tk.NORMAL)
        action_button.config(text='START SERVER')
        server_close()
        msg.showinfo('Server', 'Server is stoped!')
        insert_create_menu()


def insert_create_menu():
    global port, action_button, ip_value

    ip_value = find_local_ip()
    tk.Label(
        server_form, text='IP', background='black', foreground='red'
    ).place(relx=0.12, rely=0.3, relheight=0.05, relwidth=0.2)

    tk.Label(
        server_form, text='PORT', background='black', foreground='red'
    ).place(relx=0.12, rely=0.4, relheight=0.05, relwidth=0.2)

    label_ip = tk.Label(
        server_form,
        text=ip_value,
        background='black',
        foreground='red')
    label_ip.place(relx=0.3, rely=0.3, relheight=0.05, relwidth=0.4)

    port = tk.Entry(server_form)
    port.place(relx=0.3, rely=0.4, relheight=0.05, relwidth=0.4)

    action_button = tk.Button(server_form, text='START SERVER')
    action_button.bind('<ButtonPress-1>', start_server)
    action_button.place(relx=0.3, rely=0.5, relheight=0.09, relwidth=0.4)


server_form.protocol('WM_DELETE_WINDOW', on_closing)

insert_create_menu()

server_form.mainloop()
