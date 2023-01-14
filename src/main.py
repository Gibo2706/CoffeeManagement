import getpass
from costumer import on_continue
from manager import launch_manager_form

def main():
    def on_login():
        # Get the input from the user
        while(True):
            username = input("Username: ")
            password = getpass.getpass("Password: ")

            # Check the input against the list of users
            with open("res/files/users.txt", "r") as f:
                for line in f:
                    user, pwd = line.strip().split(":")
                    if user == username and pwd == password:
                        # Launch the manager form
                        launch_manager_form()
                        return

            # Show an error message if the login failed
            print("Error: Invalid username or password")



    while(True):
        print("Welcome to the Coffee Management Application")
        print("1. Login")
        print("2. Continue as guest")

        # Get the user's choice
        choice = input("Enter your choice: ")

        if choice == "1":
            on_login()
            break
        elif choice == "2":
            on_continue()
            break
        else:
            print("Invalid choice. Exiting...")

if __name__ == '__main__':
    main()
