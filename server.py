import socket


# Basic server-side of Python sockets: https://www.geeksforgeeks.org/socket-programming-python/

hangman_list = [
    "    _________\n"
    "    |       |\n"
    "    |        \n"
    "    |        \n"
    "    |        \n"
    "    |        \n"
    "    |\n"
    "    |_____________",

    "    _________\n"
    "    |       |\n"
    "    |       O\n"
    "    |        \n"
    "    |        \n"
    "    |        \n"
    "    |\n"
    "    |_____________",

    "    _________\n"
    "    |       |\n"
    "    |       O\n"
    "    |       |\n"
    "    |        \n"
    "    |        \n"
    "    |\n"
    "    |_____________",

    "    _________\n"
    "    |       |\n"
    "    |       O\n"
    "    |      /|\n"
    "    |        \n"
    "    |        \n"
    "    |\n"
    "    |_____________",

    "    _________\n"
    "    |       |\n"
    "    |       O\n"
    "    |      /|\\\n"
    "    |        \n"
    "    |        \n"
    "    |\n"
    "    |_____________",

    "    _________\n"
    "    |       |\n"
    "    |       O\n"
    "    |      /|\\\n"
    "    |      /\n"
    "    |        \n"
    "    |\n"
    "    |_____________",

    "    _________\n"
    "    |       |\n"
    "    |       O\n"
    "    |      /|\\\n"
    "    |      / \\\n"
    "    |        \n"
    "    |\n"
    "    |_____________",
]
word_list = ["kitchen", "flannel", "butterscotch", "witcher", "cardigan", "cat", "winter", "pleasure", "hangman",
             "telephone", "cartwheel", "juice"]

sock = socket.socket()
port = 7487
hostname = 'localhost'
sock.bind((hostname, port))
sock.listen(1)
print("server listening on:", hostname, "on port:", port)

while True:
    client, address = sock.accept()
    print("connected by", address)
    received = None
    hangman_index = 0
    word_index = 0
    print("waiting for message...")

    while received != '/q':
        client.send("how about a game of hangman? type anything to play, or /q to quit".encode())
        received = client.recv(1024).decode()
        if received == '/q':
            break
        print(received)

        curr_word = word_list[word_index]  # the word the client is guessing
        word_progress = ['_'] * len(curr_word)  # the blanks to be filled in by the client's guesses
        word_guesses = []  # wrong guesses
        game_won = False
        game_lost = False

        while hangman_index < len(hangman_list):
            # to be sent to the client: the hangman ascii, their progress on the word, the bank of wrong guesses
            send_str = hangman_list[hangman_index] + '\n\n    ' + "".join(word_progress) + '\n\n' + \
                       "wrong guesses:" + str(word_guesses)

            if "".join(word_progress) == curr_word:
                print("game won")
                game_won = True
            if hangman_index == len(hangman_list) - 1:
                print("game lost")
                game_lost = True

            # add special message for game won or lost, and all words played
            if game_won:
                if word_index == len(word_list) - 1:
                    send_str = send_str + '\n\n' + "you won! that's all the words I have. Want to start from the " \
                                                   "beginning? type anything to play, or /q to quit"
                else:
                    send_str = send_str + '\n\n' + "you won! I have more words for you. type anything to play, or " \
                                                   "/q to quit"
            if game_lost:
                if word_index == len(word_list) - 1:
                    send_str = send_str + '\n\n' + "you lost! that's all the words I have. Want to start from the " \
                                                   "beginning? type anything to play, or /q to quit"
                else:
                    send_str = send_str + '\n\n' + "you lost! I have more words for you. type anything to play, or " \
                                                   "/q to quit"

            client.send(send_str.encode())

            received = client.recv(1024).decode()
            received = received.lower()
            print(received)

            if received == '/q':
                break

            if game_won or game_lost:
                break

            if len(received) == 1:  # only single char guesses are counted
                if received not in word_guesses:
                    if received in curr_word:
                        for i in range(len(curr_word)):  # fills in all instances of correct char guess
                            if curr_word[i] == received:
                                word_progress[i] = curr_word[i]
                    else:
                        word_guesses.append(received)  # add to wrong guesses bank and add body parts to hangman
                        hangman_index += 1
                else:
                    print("duplicate guess")
            else:
                print("invalid num char")

        if word_index == len(word_list) - 1:  # reset word list
            word_index = 0
        else:
            word_index += 1  # next word
        hangman_index = 0

    client.close()
    break
