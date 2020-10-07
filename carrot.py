### Backend

#Library imports
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from columnar import columnar
from matplotlib import pyplot as plt



#Import df
def import_df():
	df = pd.read_csv('/home/ra314/All/Programming/carrots.csv')
	df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%d-%m-%Y %H:%M:%S'))
	return df

df = import_df()

#Export dataframe
def export_df(df):
	export_location = '/home/ra314/All/Programming/carrots.csv'
	df.to_csv(export_location, index = False, date_format='%d-%m-%Y %H:%M:%S')



#Nothing found message
def nothing_found():
	print("No tasks were found with the provided constraints.")

#Fill fields message
def fill_fields():
	print("Fill all required fields without default values.")



#Get time and date, but only up to seconds
def get_time_now():
	now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	now = datetime.strptime(now, '%d-%m-%Y %H:%M:%S')
	return now

#Adding Tasks
def add_task(df, category, description, carrot):
	now = get_time_now()
	df.loc[len(df)] = [now, category, description, carrot, len(df)]
	print(f"\nYou've earned {carrot}XP")
	export_df(df)

#Function to calculate XP gained in a day
def xp_per_day(df, selected_date, restricted_categories):
	date_bools = df['Date'].apply(lambda x: x.date() == selected_date.date())
	category_bools = df['Category'].apply(lambda x: x not in restricted_categories)
	aggregate_bools = np.array(date_bools) & np.array(category_bools)

	return df[aggregate_bools]['Carrot'].sum()

#Search for last n tasks by category
def last_x_tasks(df, description, category, x):
	#bools contains booleans where there are
	#matches in the df with the desired description or/and category
	if description == "":
		bools = df['Category'] == category
	elif category == "":
		bools = df['Description'].apply(lambda x: description in x)
	else:
		bools = df[['Description','Category']] == [description, category]

	headers = ['Index', 'Date', 'Description', 'Category', 'Carrot']
	tasks = df[headers][bools].dropna()[-x:]

	if len(tasks) == 0:
		nothing_found()
		return

	data = tasks[headers].values.tolist()
	table = columnar(data, headers, terminal_width=100)
	print(table)

#Function to calculate XP gained in last x days
def xp_in_last_x_days(df, x, restricted_categories):
	first_date = df.loc[0][0]
	headers = ['Date', 'Day', 'XP']
	data = []
	total_xp = 0
	today = datetime.now()

	for i in range(x-1,-1,-1):
		date = today-timedelta(days=i)
		#Prevents the loop from executing before the first date
		if date<first_date: continue
		xp = xp_per_day(df, date, restricted_categories)
		total_xp += xp;
		data.append([date.strftime('%d-%m-%Y'), date.strftime('%A'), str(xp)])

	if len(data) == 0:
		nothing_found()
		return

	table = columnar(data, headers)
	print(table)
	print(f"Fuck yeah you earned {total_xp}XP in the last {x} days!!!")

	plt.plot(np.flip(np.array(data)[:,2].astype(int)), marker = 'o')
	plt.xlabel("Days previous to today")
	plt.ylabel("Carrots")
	plt.show()

#Function to print tasks done on a certain day
def print_tasks_on_day(df, selected_date, restricted_categories):
	headers = ['Index', 'Date', 'Description', 'Category', 'Carrot']
	date_bools = df['Date'].apply(lambda x: x.date() == selected_date.date())
	category_bools = df['Category'].apply(lambda x: x not in restricted_categories)
	aggregate_bools = np.array(date_bools) & np.array(category_bools)
	masked_df = df[aggregate_bools][headers]

	if len(masked_df) == 0:
		nothing_found()
		return

	total_xp = masked_df['Carrot'].sum()
	table = columnar(masked_df.values.tolist(), headers, terminal_width=100)

	print(table)
	selected_date_str = str(selected_date.date())
	print("On " + selected_date_str + " you earned " + str(total_xp) + "XP")

#Function to find a task by index
def find_task_by_index(task_index):
	slice = df.loc[task_index]
	return slice[1], slice[2], slice[3]

#Function to edit previous task based on index and input
def edit_task_by_index(df, category, description, carrots, task_index):
	df.loc[task_index, 'Description'] = description
	df.loc[task_index, 'Category'] = category
	df.loc[task_index, 'Carrot'] = carrots
	return

#Function to autcomplete task
def autocomplete_task(df, description):
	bools = df['Description'].str.contains(description)
	masked_df = df[bools]
	last_slice = masked_df.iloc[-1]
	return last_slice[1], last_slice[2], last_slice[3]



### Front end

# Library imports
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown  import DropDown
from kivy.uix.spinner import Spinner

from kivy.core.window import Window
Window.size = (1000,1000)

# This class stores the info of .kv file
# when it is called goes to my.kv file
class MainWidget(GridLayout):
	### Functions to get values from text fields
	def get_blacklisted_categories(self):
		blacklisted_categories = self.ids.input_blacklist_categories.text
		self.ids.input_blacklist_categories.text = ""
		return blacklisted_categories

	def get_date(self):
		date = self.ids.input_date.text
		self.ids.input_date.text = ""
		return date

	def get_description(self):
		description = self.ids.input_description.text
		self.ids.input_description.text = ""
		return description

	def get_category(self):
		category = self.ids.dropdown_category.text
		self.ids.dropdown_category.text = "Select category"
		if category == "Select category":
			return ""
		else:
			return category

	def get_num(self):
		num = self.ids.input_num.text
		self.ids.input_num.text = ""
		if num == "":
			return num
		else:
			return int(num)

	def get_task_index(self):
		num = self.ids.input_task_index.text
		if num == "":
			return num
		else:
			return int(num)

	def set_input_fields(self, category, description, carrots):
		self.ids.input_description.text = description
		self.ids.dropdown_category.text = category
		self.ids.input_num.text = str(carrots)



	### Functions called from Button
	def print_tasks_on_day(self):
		date = self.get_date()
		num_days = self.get_num()
		restricted_categories = self.get_blacklisted_categories()
		restricted_categories = restricted_categories.replace(" ","").split(",")

		#Default Behaviour
		#if date == "" and num_days == "": date = datetime.now().strftime('%d-%m-%Y')
		#if date == "" and num_days != "": date = (datetime.now()-timedelta(num_days)).strftime('%d-%m-%Y')
		if date == "" and num_days == "": date = datetime.now()
		if date == "" and num_days != "": date = datetime.now()-timedelta(num_days)

		print_tasks_on_day(df, date, restricted_categories)

	def last_x_tasks(self):
		description = self.get_description()
		category = self.get_category()
		num_tasks = self.get_num()

		#Default behaviour
		if num_tasks == "":
			num_tasks = 7
		else:
			num_tasks = int(num_tasks)

		last_x_tasks(df, description, category, num_tasks)

	def xp_in_last_x_days(self):
		categories = self.get_blacklisted_categories()
		restricted_categories = categories.replace(" ","").split(",")
		num_days = self.get_num()

		#Default behaviour
		if num_days == "":
			num_days = 7
		else:
			num_days = int(num_days)

		xp_in_last_x_days(df, num_days, restricted_categories)

	def add_task(self):
		description = self.get_description()
		category = self.get_category()
		carrots = self.get_num()

		#Preventing adding tasks without having filled all fields
		if description == "" or carrots == "" or category == "":
			fill_fields()
			return

		add_task(df, category, description, carrots)

	def find_task_by_index(self):
		task_index = self.get_task_index()

		#Default behaviour
		if task_index == "": task_index = len(df)-1

		self.set_input_fields(*find_task_by_index(task_index))

	def edit_task_by_index(self):
		description = self.get_description()
		category = self.get_category()
		carrots = self.get_num()
		task_index = self.get_task_index()

		#Default behaviour
		if task_index == "": task_index = len(df)-1

		#Preventing adding tasks without having filled all fields
		if description == "" or carrots == "" or category == "" or task_index == "":
			fill_fields()
			return

		### Editing task
		edit_task_by_index(df, category, description, carrots, task_index)

	def autocomplete_task(self):
		description = self.get_description()

		#Preventing searching for an empty string
		if description == "":
			fill_fields()
			return

		self.set_input_fields(*autocomplete_task(df, description))

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
