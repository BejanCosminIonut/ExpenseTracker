from expenseWindow import *
from tkinter import messagebox

# The connection to the database we will be using.
connection = psycopg2.connect(database="ExpenseTrackerDB", user="postgres",
                              password="12345", host="127.0.0.1",
                              port="5432")

# The cursor we will be using in order to apply changes to the database.
cursor = connection.cursor()

"""
This class represents the initial, set-up window that allows the user
to sign in into his account or sign up for the service.
"""
class SetupWindow:

    def __init__(self, master) -> None:
        """Initializer of the class."""
        self.frame = Frame(master)

        # pack our frame and set it up
        self.frame.pack()
        self.frame.pack_propagate(False)
        self.frame.configure(width=600, height=400)

        # username label & entry - creation and placement
        self.username_input = StringVar()
        username_entry = Entry(self.frame, width=30, textvariable=self.username_input)
        username_entry.place(relx=.55, rely=.20, anchor=CENTER)
        label_username = Label(self.frame, text="Username: ")
        label_username.place(relx=.30, rely=.20, anchor=CENTER)

        # password label & entry - creation and placement
        self.password_input = StringVar()
        password_entry = Entry(self.frame, width=30, show="*", textvariable=self.password_input)
        password_entry.place(relx=.55, rely=.30, anchor=CENTER)
        label_password = Label(self.frame, text="Password: ")
        label_password.place(relx=.30, rely=.30, anchor=CENTER)

        # button creation, placement & action bind
        button_sign_in = Button(self.frame, text="Sing in", command=self.sign_in).place(relx=.50, rely=.40,                                                                           anchor=CENTER)
        button_sign_up = Button(self.frame, text="Sing up", command=self.sign_up).place(relx=.50, rely=.50,
                                                                                        anchor=CENTER)

    def validate_username(self) -> bool:
        """
        Checks whether a username is already taken or not.
        @return: True if username is available, false otherwise.
        """
        sql_statement = f"SELECT userid FROM users WHERE username = '{self.username_input.get()}'"
        cursor.execute(sql_statement)
        row = cursor.fetchone()
        if row == None:
            return True
        else:
            return False

    def sign_in(self) -> None:
        """
        Allows a user to sign in into his existing account.
        @return: None
        """
        username = self.username_input.get()
        password = self.password_input.get()

        sql_statement = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(sql_statement)
        row = cursor.fetchone()
        if row == None:
            print("User not found!")
        else:
            print("User found!")
            username = row[1]
            expenseWindow = ExpenseWindow(username)


    def sign_up(self) -> None:
        """
        Allows the user to sign up for the service. New account creation.
        @return: None
        """
        username = self.username_input.get()
        password = self.password_input.get()

        # Check if the chosen username is available.
        if not self.validate_username():
            messagebox.showerror(message="Username already taken! Please pick something else...")
        # Check for correct user input.
        elif username == "" or password == "":
            messagebox.showerror(message="Please input a name and password...")
        else:
            sql_statement = f"INSERT INTO users(username, password) VALUES('{username}', '{password}')"
            cursor.execute(sql_statement)
            connection.commit()
            expenseWindow = ExpenseWindow(username)
