#!/usr/bin/env python3
#"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import PhotoImage, Label
import sys


my_key = 'TURING'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

HOST = '127.0.1.1'
PORT = 300
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

def encrypt_message(key, message):
    encrypted = []

    key_index = 0
    key = key.upper()

    for symbol in message:  # Loop through each symbol in message.
        num = LETTERS.find(symbol.upper())
        if num != -1:  # -1 means symbol.upper() was not found in LETTERS.
            num += LETTERS.find(key[key_index])  # Add if encrypting.

            num %= len(LETTERS)  # Handle any wraparound.

            # Add the encrypted/decrypted symbol to the end of translated:
            if symbol.isupper():
                encrypted.append(LETTERS[num])
            elif symbol.islower():
                encrypted.append(LETTERS[num].lower())

            key_index += 1  # Move to the next letter in the key.
            if key_index == len(key):
                key_index = 0
        else:
            # Append the symbol without encrypting/decrypting.
            encrypted.append(symbol)

    return ''.join(encrypted)

def message_decryption(key, message):
    decrypted = []  # Stores the encrypted/decrypted message string.

    key_index = 0
    key = key.upper()

    for symbol in message:  # Loop through each symbol in message.
        num = LETTERS.find(symbol.upper())
        if num != -1:  # -1 means symbol.upper() was not found in LETTERS.
            num -= LETTERS.find(key[key_index])  # Subtract if decrypting.

            num %= len(LETTERS)  # Handle any wraparound.

            # Add the encrypted/decrypted symbol to the end of translated:
            if symbol.isupper():
                decrypted.append(LETTERS[num])
            elif symbol.islower():
                decrypted.append(LETTERS[num].lower())

            key_index += 1  # Move to the next letter in the key.
            if key_index == len(key):
                key_index = 0
        else:
            # Append the symbol without encrypting/decrypting.
            decrypted.append(symbol)

    return ''.join(decrypted)

def receive():
    #Handles message receipt.
    while True:
        try:
            decoded = client_socket.recv(BUFSIZ).decode("utf8")
            msg = message_decryption(my_key, decoded)

            msg_list.configure(state='normal')
            msg_list.insert(tkinter.END, msg + '\n')
            msg_list.configure(state='disabled')

        except OSError:  # Possibly client has left the chat.
            return
        except BaseException as e:
            return

def send(event=None):
    #Handles sending of messages.
    msg = my_msg.get()
    my_msg.set("")      # Clears input field.
    client_socket.send(bytes(encrypt_message(my_key, msg), "utf8"))

def close_window():
    client_socket.send(bytes(encrypt_message(my_key, '{quit}'), 'utf8'))
    
    window.destroy()
    sys.exit(0)


def disable_titlebar_exit():
    pass

def send_button_hover(e):
    send_button['bg'] = 'white'
    status_bar.configure(text='Send your message')

def send_button_hover_leave(e):
    send_button['bg'] = 'grey15'
    status_bar.configure(text='')

def exit_button_hover(e):
    exit_button['bg'] = 'white'
    status_bar.configure(text='Exit user client window')

def exit_button_hover_leave(e):
    exit_button['bg'] = 'grey15'
    status_bar.configure(text='')

def entry_field_hover(e):
    status_bar.configure(text='Message entry field')

def entry_field_hover_leave(e):
    status_bar.configure(text='')

def msg_list_hover(e):
    status_bar.configure(text='Messaging window')

def msg_list_hover_leave(e):
    status_bar.configure(text='')

###Start of Gui parameters

#Creates the gui window
window = tkinter.Tk()
window.title("Secure PyChat")
window.iconphoto(True, PhotoImage(file="IMG/logo3.png"))
window.configure(bg='grey15')
window.geometry('600x550')
window.resizable(False, False)

#Creates message frame and defines the object my_msg which is 
#used throughout the client script
messages_frame = tkinter.Frame(window)
my_msg = tkinter.StringVar()  

scrollbar = tkinter.Scrollbar(messages_frame)  
scrollbar.configure(bg='grey25')
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# Creates an area which will contain messages.
msg_list = tkinter.Text(messages_frame, yscrollcommand=scrollbar.set, bd=0, relief='sunken', wrap='word')
msg_list.configure(bg='grey30', fg='white', state='disabled')
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()
messages_frame.configure(bg='black', bd=0)

entry_field = tkinter.Entry(window, textvariable=my_msg, relief='sunken')
entry_field.bind("<Return>", send)
entry_field.pack(padx=20, pady=5, ipadx=1, ipady=1)

send_btn = PhotoImage(file='IMG/send_icon_shrunk.png')
send_button = tkinter.Button(window, image=send_btn, command=send, bg='grey15', borderwidth=0)
send_button.place(x=250, y=450)

exit_btn = PhotoImage(file='IMG/close_icon_shrunk.png')
exit_button = tkinter.Button(window, image=exit_btn, command=close_window, bg='grey15', borderwidth=0)
exit_button.place(x=300, y=450)

status_bar = Label(window, text='', bd=1, relief='sunken', anchor='e')
status_bar.pack(pady=1, fill='x', side='bottom', ipady=2)
status_bar.configure(bg='grey30', fg='white')

send_button.bind('<Enter>', send_button_hover)
send_button.bind('<Leave>', send_button_hover_leave)

exit_button.bind('<Enter>', exit_button_hover)
exit_button.bind('<Leave>', exit_button_hover_leave)

entry_field.bind('<Enter>', entry_field_hover)
entry_field.bind('<Leave>', entry_field_hover_leave)

msg_list.bind('<Enter>', msg_list_hover)
msg_list.bind('<Leave>', msg_list_hover_leave)

window.protocol('WM_DELETE_WINDOW', disable_titlebar_exit)

message = my_msg.get()

receive_thread = Thread(target=receive)
receive_thread.start()

def main():
    tkinter.mainloop()  # Starts GUI execution.
    
if __name__ == '__main__':
    main()