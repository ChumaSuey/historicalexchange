import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from main import DateFinderBackend

class DateFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Date Finder")

        # Initialize backend
        self.backend = DateFinderBackend()

        # Get today's date
        today = datetime.today()

        # Calendar with maxdate set to today
        self.calendar = Calendar(root, selectmode='day', year=today.year, month=today.month, day=today.day, maxdate=today)
        self.calendar.pack(pady=20)

        # Search Button
        self.search_button = ttk.Button(root, text="Search", command=self.search_date)
        self.search_button.pack(pady=10)

        # Value Box
        self.value_label = ttk.Label(root, text="Value")
        self.value_label.pack(pady=5)
        self.value_entry = ttk.Entry(root)
        self.value_entry.pack(pady=5)

    def search_date(self):
        selected_date = self.calendar.get_date()
        # Convert the date format from D/M/YY to YYYY-MM-DD
        date_obj = datetime.strptime(selected_date, '%m/%d/%y')
        formatted_date = date_obj.strftime('%Y-%m-%d')
        self.value_entry.delete(0, tk.END)
        exchange_rate = self.backend.get_exchange_rate(formatted_date)
        self.value_entry.insert(0, exchange_rate)

if __name__ == "__main__":
    root = tk.Tk()
    app = DateFinderApp(root)
    root.mainloop()