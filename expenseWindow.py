import psycopg2
import matplotlib.pyplot as plt

from tkinter import *

from expensePeriodWindow import ExpensePeriodWindow
from expenseValuesWindow import ExpenseValuesWindow
from tkcalendar import Calendar

# The connection to the database we will be using.
connection = psycopg2.connect(database="ExpenseTrackerDB", user="postgres",
                              password="12345", host="127.0.0.1",
                              port="5432")

# The cursor we will be using in order to apply changes to the database.
cursor = connection.cursor()


"""
This class represents the window with the calendar widget.
From here a user can pick a date and add a new expense for it
while having the possibility to see charts.
"""
class ExpenseWindow:

    def __init__(self, username):
        """Initializer of the class."""
        self.username = username

        # Creating a new Toplevel() widget.
        self.top = Toplevel()
        self.top.resizable(False, False)
        self.top.geometry("600x400")

        # Creating, placing and packing of our Calendar Widget.
        self.calendar = Calendar(
            self.top,
            selectmode='day',
            year=2023,
            day=27,
            month=1
        )
        self.calendar.place(relx=.5, rely=.5, anchor=CENTER)
        self.calendar.pack(pady=20)

        # Button creation, placement and action binding.
        button_new_expense = Button(self.top, text="Add new expense", command=self.add_new_expense).place(relx=.50, rely=.60,
                                                                                                     anchor=CENTER)
        button_show_expense_chart_for_the_day = Button(self.top, text="Show expense chart for the day",
                                                       command=self.show_expense_chart_day).place(relx=.50, rely=.70,
                                                                                                  anchor=CENTER)
        button_show_expense_chart_for_time_period = Button(self.top, text="Show expense chart for time period",
                                                           command=self.show_expense_chart_time_period).place(relx=.50,
                                                                                                              rely=.80,
                                                                                                              anchor=CENTER)

    def add_new_expense(self) -> None:
        """
        Getting the selected date and the userid of the user who is logged into the account
        at the moment and opening a new window of type ExpenseValueWindow with those values.
        @return: None
        """
        date = self.calendar.get_date()
        user_id = self.find_user_by_id()
        expenseValuesWindow = ExpenseValuesWindow(date, user_id)

    def show_expense_chart_day(self) -> None:
        """
        Will save the values that have been input by the user as spending's for a user-picked date.
        Calls the function which will draw the chart on to the screen.
        @return: None
        """
        # Getting the selected date and the userid of the user who is logged into the account
        user_id = self.find_user_by_id()
        date = self.calendar.get_date()

        # Variables which will store the values from our SQL Query.
        necessities = 0
        food = 0
        entertainment = 0
        other = 0

        sql_statement = f"SELECT * FROM expenses where userid = '{user_id}' and date = '{date}' "
        cursor.execute(sql_statement)
        row = cursor.fetchall()

        # Looping through our results one by one
        for r in row:
            # Adding each column to its respective category where:
            #       r[0]: expenseid
            #       r[1]: userid
            necessities = necessities + r[2]
            food = food + r[3]
            entertainment = entertainment + r[4]
            other = other + r[5]

        # Calling the function which will draw our chart.
        self.draw_chart(necessities, food, entertainment, other)


    def show_expense_chart_time_period(self) -> None:
        """
        Will open a new window of type ExpensePeriodWindow where the user has
        the possibility of picking a time period for which his spending's will be calculated.
        @return: None
        """
        user_id = self.find_user_by_id()
        expenseWindowPeriod = ExpensePeriodWindow(user_id)

    def find_user_by_id(self) -> int:
        """
        Returns the id of the current user.
        @return: int, current user id.
        """
        sql_statement = f"SELECT userid FROM users WHERE username = '{self.username}'"
        cursor.execute(sql_statement)
        row = cursor.fetchone()

        return int(row[0])

    def draw_chart(self, necessities, food, entertainment, other) -> None:
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