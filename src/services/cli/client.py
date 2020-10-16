import requests


class Client:

    help_text = "help - show this help text\n"\
        "exit - exit program\n"\
        "login USER_ID - login with user id"

    user_id = ""

    def login(self, user_id):
        self.user_id = user_id

    def main_loop(self):
        print(self.help_text)

        while True:
            inputs = input("memo_chater: ").split(" ")
            command = inputs[0]
            if command == "help":
                print(self.help_text)
            elif command == "exit":
                return
            elif command == "login":
                self.login(user_id=inputs[1])


if __name__ == "__main__":
    client = Client()
    client.main_loop()
