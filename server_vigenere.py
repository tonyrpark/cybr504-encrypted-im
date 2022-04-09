#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys
import errno

my_key = 'TURING'

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def message_decryption(key, message):
    #message = message_decryption(client.recv(BUFSIZ).decode("utf8"))
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

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = message_decryption(my_key, client.recv(BUFSIZ).decode("utf8"))
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        #msg = client.recv(BUFSIZ)
        try:
            message = str(message_decryption(my_key, client.recv(BUFSIZ).decode("utf8")))
            #msg = bytes(message_decryption(my_key, client.recv(BUFSIZ).decode("utf8"))))
            #msg = message_decryption(my_key, my_msg)

    #        if msg != bytes("{quit}", "utf8"):
    #            broadcast(msg, name + ": ")
            #if message != bytes("{quit}", "utf8"):
            if message != "{quit}":
                broadcast(bytes(message, "utf8"), name + ": ")

            else:
                client.send(bytes("{quit}", "utf8"))
                #client.send("{quit}")
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break
        except IOError as e:
            if e.errno == errno.EPIPE:
                pass




def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = '127.0.2.1'
PORT = 300
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()