import psycopg2
import matplotlib.pyplot as plt

from tkinter import *

from tkcalendar import DateEntry

# The connection to the database we will be using.
connection = psycopg2.connect(database="ExpenseTrackerDB", user="postgres",
                              password="12345", host="127.0.0.1",
                              port="5432")

# The cursor we will be using in order to apply changes to the database.
cursor = connection.cursor()

"""
This class is used to represent the window where the user picks his period
of time in order for his expenses to be calculated.
"""
class ExpensePeriodWindow:

    def __init__(self, user_id):
        self.user_id = user_id

        # Creating a new Toplevel() widget.
        self.top = Toplevel()
        self.top.resizable(False, False)
        self.top.geometry("600x400")
        self.top.title("Date picker")

        # Variables for storing the dates picked by the user.
        self.start_date = None
        self.end_date = None

        # Start Date label & entry creation.
        start_date_label = Label(self.top, text="Start Date: ")
        start_date_label.place(relx=.40, rely=0.30, anchor=CENTER)
        self.start_date_entry = DateEntry(self.top, width=15)
        self.start_date_entry.place(relx=.65, rely=.30, anchor=CENTER)

        # End Date label & entry creation.
        end_date_label = Label(self.top, text="End Date: ")
        end_date_label.place(relx=.40, rely=0.40, anchor=CENTER)
        self.end_date_entry = DateEntry(self.top, width=15)
        self.end_date_entry.place(relx=.65, rely=0.40, anchor=CENTER)

        # Button creation, placement & action bind
        button_confirm = Button(self.top, text="Confirm dates", command=self.calculate_expenses).place(relx=.50,
                                                                                                       rely=.60,
                                                                                                       anchor=CENTER)

    def calculate_expenses(self) -> None:
        """

        @return:
        """
        # Get the input into variables
        user_id = self.user_id
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        # Creating the variables for our categories
        necessities = 0
        food = 0
        entertainment = 0
        other = 0

        sql_statement = f"SELECT * FROM expenses where userid = '{user_id}' and date BETWEEN '{start_date}' AND '{end_date}' "
        cursor.execute(sql_statement)
        row = cursor.fetchall()

        # Looping through our results row by row and adding each category to its respective variable where:
        #       row[0]: expenseid
        #       row[1] userid
        for r in row:
            necessities = necessities + r[2]
            food = food + r[3]
            entertainment = entertainment + r[4]
            other = other + r[5]

        # Draw the chart with the calculated values.
        self.draw_chart(necessities, food, entertainment, other)
        # Hides the window
        self.top.attributes('-alpha', 0.0)

    def draw_chart(self, necessities: float, food: float, entertainment: float, other: float) -> None:
        """
        Will draw a bar-chart where the values are the parameters it was given.
        @param necessities: float value, represents amount spent on current category.
        @param food: float value, represents amount spent on current category.
        @param entertainment: float value, represents amount spent on current category.
        @param other: float value, represents amount spent on current category.
        @return: None
        """
        # Creating our chart bars
        x_axis = ['Necessities', 'Food', 'Entertainment', 'Other']
        y_axis = [necessities, food, entertainment, other]

        # Adding the bars to our chart.
        plt.bar(x_axis, y_axis)
        # Setting chart title.
        plt.title("Spending chart")

        # Labeling
        plt.xlabel("Categories")
        plt.ylabel("Amount spent")

        # Drawing the chart
        plt.show()