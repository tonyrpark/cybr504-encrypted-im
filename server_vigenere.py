#!/usr/bin/env python3
# """Server for multithreaded (asynchronous) chat application."""

# import required modules
from socket import AF_INET, socket, SOCK_STREAM
import socket
from threading import Thread
import threading
import sys
import errno


# Objects used for vigenere cipher
my_key = 'TURING'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

clients = {}
addresses = {}

HOST = '127.1.1.1'
PORT = 9990
BUFSIZ = 1024
ADDR = (HOST, PORT)

LISTENER_LIMIT = 5


def message_decryption(key, message):
    # Stores the decrypted message string.
    decrypted = []

    key_index = 0
    key = key.upper()

    for symbol in message:  # Loops through each symbol in message.
        num = LETTERS.find(symbol.upper())
        if num != -1:  # -1 means symbol.upper() was not found in LETTERS.
            num -= LETTERS.find(key[key_index])  # Subtract if decrypting.
            num %= len(LETTERS)  # Handle any wraparound.

            # Add the decrypted symbol to the end of decrypted:
            if symbol.isupper():
                decrypted.append(LETTERS[num])
            elif symbol.islower():
                decrypted.append(LETTERS[num].lower())

            # Moves to the next letter in the key.
            key_index += 1
            if key_index == len(key):
                key_index = 0
        else:
            # Append the symbol without decrypting.
            decrypted.append(symbol)

    return ''.join(decrypted)


def encrypt_message(key, message):
    # Stores the encrypted message string
    encrypted = []

    key_index = 0
    key = key.upper()

    for symbol in message:  # Loop through each symbol in message.
        num = LETTERS.find(symbol.upper())
        if num != -1:  # -1 means symbol.upper() was not found in LETTERS.
            num += LETTERS.find(key[key_index])  # Add if encrypting.
            num %= len(LETTERS)  # Handle any wraparound.

            # Add the encrypted symbol to the end of encrypted:
            if symbol.isupper():
                encrypted.append(LETTERS[num])
            elif symbol.islower():
                encrypted.append(LETTERS[num].lower())

            # Moves to the next letter in the key.
            key_index += 1
            if key_index == len(key):
                key_index = 0
        else:
            # Append the symbol without encrypting.
            encrypted.append(symbol)

    return ''.join(encrypted)


def sendallclients(message):
    try:
        for client in clients:
            client.send(message)
    except IOError as e:
        if e.errno == errno.EPIPE:
            pass


def handle_client(client):
    # Handles the client connections to the server

    name = str(message_decryption(my_key, client.recv(BUFSIZ).decode("utf8")))

    welcome = 'Welcome %s! If you ever want to quit, click the exit button below.' % name
    client.send(bytes((encrypt_message(my_key, welcome)), "utf8"))

    msg = str("%s has joined the chat!" % name)
    sendallclients(bytes((encrypt_message(my_key, msg)), "utf8"))

    clients[client] = name

    while True:
        try:
            message = str(message_decryption(my_key, client.recv(BUFSIZ).decode("utf8")))

            if message != "{quit}":
                prefix = (name + ": ")
                prefixed_message = (prefix + message)

                encrypted_msg = (encrypt_message(my_key, prefixed_message))
                sendallclients(bytes((encrypted_msg), "utf8"))

            else:
                client.send(bytes(encrypt_message(my_key, "{quit}"), "utf8"))
                # client.close()

                sendallclients(bytes(encrypt_message(my_key, "%s has left the chat." % name), "utf8"))
                print('%s has disconnected.' % name)

                del clients[client]
                break
        except IOError as e:
            if e.errno == errno.EPIPE:
                pass


def main():
    SERVER = socket.socket(AF_INET, SOCK_STREAM)

    try:
        SERVER.bind(ADDR)
        print(f'Server running on {HOST}: port {PORT}')
        print("Waiting for connection...")

    except:
        print(f'Unable to bind to host {HOST} and port {PORT}')

    # Set server's user limit
    SERVER.listen(LISTENER_LIMIT)

    while 1:
        client, address = SERVER.accept()
        print(f'{address[0]}:{address[1]} has connected.')
        client.send(bytes(encrypt_message(my_key, 'Type your name below and click send to join server'), 'utf8'))

        addresses[client] = address

        threading.Thread(target=handle_client, args=(client,)).start()


if __name__ == "__main__":
    main()

    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()