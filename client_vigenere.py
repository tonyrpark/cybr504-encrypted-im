#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import PhotoImage

my_key = 'TURING'

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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
    """Handles receiving of messages."""
    while True:
        try:
            #msg = client_socket.recv(BUFSIZ).decode("utf8")
            decoded = client_socket.recv(BUFSIZ).decode("utf8")
            print(decoded)
            #msg = str(message_decryption(my_key, client_socket.recv(BUFSIZ).decode("utf8")))
            msg = message_decryption(my_key, decoded)
            print(msg)
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(encrypt_message(my_key, msg), "utf8"))
    if msg == "{quit}":
        client_socket.close()
        window.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

window = tkinter.Tk()
window.title("Encrypted Jabber Project") ###Stand in name, can change later
window.iconphoto(True, PhotoImage(file="ironWolf_halfsize.gif"))
window.configure(bg='grey15')
window.resizable(False, False)

messages_frame = tkinter.Frame(window)
my_msg = tkinter.StringVar()  # For the messages to be sent.

scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
scrollbar.configure(bg='grey25')

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
messages_frame.configure(bg='black')

entry_field = tkinter.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(padx=20, pady=5)
send_button = tkinter.Button(window, text="Send", command=send)
send_button.pack(padx=20, pady=5)

window.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
#HOST = input('Enter host: ')
#PORT = input('Enter port: ')
#if not PORT:
#    PORT = 33000
#else:
#    PORT = int(PORT)

#HOST = '127.0.1.1'
HOST = '127.0.1.1'
PORT = 300

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


message = my_msg.get()

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.