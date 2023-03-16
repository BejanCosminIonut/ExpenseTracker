import psycopg2

from tkinter import *

from tkinter import messagebox

# The connection to the database we will be using.
connection = psycopg2.connect(database="ExpenseTrackerDB", user="postgres",
                              password="12345", host="127.0.0.1",
                              port="5432")

# The cursor we will be using in order to apply changes to the database.
cursor = connection.cursor()

"""
This class will be used in order to create the window
where all expenses are being input and sent to the DB.
"""
class ExpenseValuesWindow:

    def __init__(self, date, user_id) -> None:
        """Initializer of the class."""
        self.date = date
        self.user_id = user_id

        # Creating a new Toplevel() widget.
        self.top = Toplevel()
        self.top.resizable(False, False)
        self.top.geometry("600x400")

        # Construction float variables for our entries.
        self.necessities_input = DoubleVar()
        self.food_input = DoubleVar()
        self.entertainment_input = DoubleVar()
        self.other_input = DoubleVar()

        # Necessities label & entry creation.
        necessities_entry = Entry(self.top, width=30, textvariable=self.necessities_input)
        necessities_entry.place(relx=.55, rely=.20, anchor=CENTER)
        necessities_label = Label(self.top, text="Necessities: ")
        necessities_label.place(relx=.30, rely=.20, anchor=CENTER)

        # Food label & entry creation.
        food_entry = Entry(self.top, width=30, textvariable=self.food_input)
        food_entry.place(relx=.55, rely=.30, anchor=CENTER)
        food_label = Label(self.top, text="Food: ")
        food_label.place(relx=.30, rely=.30, anchor=CENTER)

        # Entertainment label & entry creation.
        entertainment_entry = Entry(self.top, width=30, textvariable=self.entertainment_input)
        entertainment_entry.place(relx=.55, rely=.40, anchor=CENTER)
        entertainment_label = Label(self.top, text="Entertainment: ")
        entertainment_label.place(relx=.30, rely=.40, anchor=CENTER)

        # Other label & entry creation.
        other_entry = Entry(self.top, width=30, textvariable=self.other_input)
        other_entry.place(relx=.55, rely=.50, anchor=CENTER)
        other_label = Label(self.top, text="Other: ")
        other_label.place(relx=.30, rely=.50, anchor=CENTER)

        # Button creation, placement and action binding.
        button_add_expenses = Button(self.top, text="Add expense", command=self.add_expense).place(relx=.50, rely=.60,
                                                                                              anchor=CENTER)
        button_help = Button(self.top, text="Help", command=self.help).place(relx=.50, rely=.70, anchor=CENTER)

    def add_expense(self) -> None:
        """
        Saves a new entry into our DB with the input it was given by the user.
        @return: None
        """
        # Getting the input values into variables.
        necessities_value = self.necessities_input.get()
        food_value = self.food_input.get()
        entertainment_value = self.entertainment_input.get()
        other_value = self.other_input.get()
        date_value = self.date

        # Inserting the values into our DB.
        sql_statement = f"INSERT INTO expenses(userid, necessities, food, entertainment, other, date) VALUES('{self.user_id}', '{necessities_value}', '{food_value}', '{entertainment_value}', '{other_value}', '{date_value}')"
        cursor.execute(sql_statement)
        connection.commit()

        # Printing successful input to the user.
        messagebox.showinfo(title="Information", message="Expense Added!")

        # Hides the window
        self.top.attributes('-alpha', 0.0)

    def help(self) -> None:
        """
        Gives a brief description of each category to the user.
        @return: None
        """
        messagebox.showinfo(title="Help Window", message="Necessities: Bills, Rent etc\n"
                                                         "Food: Self explanatory\n"
                                                         "Entertainment: Clubs, Parties, Cinema and other fun events\n"
                                                         "Other: Everything else")