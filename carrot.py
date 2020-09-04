### Backend

#Library imports
import pandas as pd
from datetime import datetime
from datetime import timedelta
from columnar import columnar

#Nothing found message
def nothing_found():
	print("No tasks were found with the provided contraints.")

#Import df
def import_df():
	df = pd.read_csv('/home/ra314/All/Academic/LeetCode/carrots.csv')
	df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%d-%m-%Y %H:%M:%S'))
	return df

df = import_df()

#Export dataframe
def export_df(df):
	export_location = '/home/ra314/All/Academic/LeetCode/carrots.csv'
	df.to_csv(export_location, index = False, date_format='%d-%m-%Y %H:%M:%S')

#Get time and date, but only up to seconds
def get_time_now():
	now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	now = datetime.strptime(now, '%d-%m-%Y %H:%M:%S')
	return now

#Adding Tasks
def add_task(df, category, description, carrot):
	now = get_time_now()
	df.loc[len(df)] = [now, category, description, carrot]
	print(f"\nYou've earned {carrot}XP")
	export_df(df)

#Function to calculate XP gained in a day
def xp_per_day(df, selected_date_str, restricted_categories):
	xp = 0
	selected_date = datetime.strptime(selected_date_str, '%d-%m-%Y')
	for row in df.iterrows():
		curr_date = row[1]['Date']
		curr_category = row[1]['Category']
		if curr_date.date() == selected_date.date():
			if (curr_category not in restricted_categories):
				xp += row[1]['Carrot']
	return xp

#Search for last n tasks by category
def last_x_tasks(df, description, category, x):
	#bools contains booleans where there are
	#matches in the df with the desired description or/and category
	if description == "":
		bools = df['Category'] == category
	elif category == "":
		bools = df['Description'] == description
	else:
		bools = df[['Description','Category']] == [description, category]

	tasks = df[['Date', 'Description','Category']][bools].dropna()[-x:]

	if len(tasks) == 0:
		nothing_found()
		return

	headers = ['Date', 'Description', 'Category']
	data = tasks[headers].values.tolist()
	table = columnar(data, headers, terminal_width=100)
	print(table)

#Function to calculate XP gained in last x days
def xp_in_last_x_days(df, x, restricted_categories):
	headers = ['Date', 'Day', 'XP']
	data = []
	total_xp = 0

	today_str = datetime.now().strftime('%d-%m-%Y')
	today = datetime.strptime(today_str, '%d-%m-%Y')

	for i in range(x-1,-1,-1):
		date = (today-timedelta(days=i)).strftime('%d-%m-%Y')
		xp = xp_per_day(df, date, restricted_categories)
		total_xp += xp;
		day = datetime.strptime(date, '%d-%m-%Y')
		data.append([date, day.strftime('%A'), str(xp)])

	if len(data) == 0:
		nothing_found()
		return

	table = columnar(data, headers)
	print(table)

	print(f"Fuck yeah you earned {total_xp}XP in the last {x} days!!!")

#Function to print tasks done on a certain day
def print_tasks_on_day(df, selected_date_str, restricted_categories):
	selected_date = datetime.strptime(selected_date_str, '%d-%m-%Y')
	headers = ['Category', 'Description', 'Carrot']
	data = []
	total_xp = 0

	for row in df.iterrows():
		curr_date = row[1]['Date']

		if curr_date.date() == selected_date.date():
			if row[1]['Category'] not in restricted_categories:
				data.append([
				row[1][headers[0]],
				row[1][headers[1]],
				str(row[1][headers[2]])
				])
				total_xp += row[1]['Carrot']

	if len(data) == 0:
		nothing_found()
		return

	table = columnar(data, headers, terminal_width=100)
	print("On " + selected_date_str + " you earned " + str(total_xp) + "XP")
	print(table)

### Front end

# Library imports
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown  import DropDown

from kivy.core.window import Window
Window.size = (900, 900)

# This class stores the info of .kv file
# when it is called goes to my.kv file
class MainWidget(GridLayout):
	def print_tasks_on_day(self):
		date = self.ids.input_date.text
		categories = self.ids.input_blacklist_categories.text
		restricted_categories = categories.replace(" ","").split(",")

		if date == "":
			date = datetime.now().strftime('%d-%m-%Y')

		print_tasks_on_day(df, date, restricted_categories)

		self.ids.input_date.text = ""
		self.ids.input_blacklist_categories.text = ""

	def last_x_tasks(self):
		description = self.ids.input_description.text
		category = self.ids.input_category.text
		num_tasks = self.ids.input_num.text

		if num_tasks == "":
			num_tasks = 7
		else:
			num_tasks = int(num_tasks)

		last_x_tasks(df, description, category, num_tasks)

		self.ids.input_description.text = ""
		self.ids.input_category.text = ""
		self.ids.input_num.text = ""

	def xp_in_last_x_days(self):
		categories = self.ids.input_blacklist_categories.text
		restricted_categories = categories.replace(" ","").split(",")
		num_days = self.ids.input_num.text

		if num_days == "":
			num_days = 7
		else:
			num_days = int(num_days)

		xp_in_last_x_days(df, num_days, restricted_categories)

		self.ids.input_blacklist_categories.text = ""
		self.ids.input_num.text = ""

	def add_task(self):
		description = self.ids.input_description.text
		category = self.ids.input_category.text
		carrots = int(self.ids.input_carrots.text)

		add_task(df, category, description, carrots)

		self.ids.input_description.text = ""
		self.ids.input_category.text = ""
		self.ids.input_carrots.text = ""

	pass

# we are defining the Base Class of our Kivy App
class carrotApp(App):
	def build(self):
		# return a MainWidget() as a root widget
		return MainWidget()

if __name__ == '__main__':

    # Here the class MyApp is initialized
    # and its run() method called.
    carrotApp().run()
