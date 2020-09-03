#Libs
import pandas as pd
from datetime import datetime
from datetime import timedelta

#Creating the empty df
#df = pd.DataFrame(columns = ['Date', 'Category', 'Description', 'Carrot'])

#Adding Tasks
def add_task(df, category, description, carrot):
	now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	df.loc[len(df)] = [now, category, description, carrot]
	print(f"\nYou've earned {carrot}XP")
	df.to_csv('carrots.csv', index = False)

#Sample Usage
#add_task(df, 'Hygiene', 'Brushed Teeth', 1)

#Exporting and Importing
#df.to_csv('carrots.csv', index = False)
df = pd.read_csv('carrots.csv')

#Todo List
#Calculate XP without certain categories
#Handle Error for when there are no tasks done on a certain day

#Function to calculate XP gained in a day
def xp_per_day(df, selected_date_str):
	xp = 0
	selected_date = datetime.strptime(selected_date_str, '%d-%m-%Y')
	for row in df.iterrows():
		curr_date_str = row[1]['Date']
		curr_date = datetime.strptime(curr_date_str, '%d-%m-%Y %H:%M:%S')
		if curr_date.date() == selected_date.date():
			xp += row[1]['Carrot']
	return xp

#Sample Usage
#xp_per_day(df, '16-08-2020')

#Function to edit xp
def edit_xp(df, index, new_xp):
	df.at[index, 'Carrot'] = new_xp
	print("\nValue has been updated.")
	df.to_csv('carrots.csv', index = False)

#Sample Usage
#edit_xp(df, 15, 15)

#Function to calculate XP gained in last x days
def xp_in_last_x_days(df, x):
	headers = ['XP', 'Date']
	data = []
	total_xp = 0
	today_str = datetime.now().strftime('%d-%m-%Y')
	today = datetime.strptime(today_str, '%d-%m-%Y')
	for i in range(x-1,-1,-1):
		date = (today-timedelta(days=i)).strftime('%d-%m-%Y')
		xp = xp_per_day(df, date)
		total_xp += xp;
		data.append([str(xp), date])
	table = columnar(data, headers)
	print(table)
	print(f"Fuck yeah you earned {total_xp}XP in the last {x} days!!!")

#Sample Usage
#xp_in_last_x_days(df, 7)

#Function to print tasks done on a certain day
def tasks_on_day(df, selected_date_str):
    selected_date = datetime.strptime(selected_date_str, '%d-%m-%Y')
    headers = ['Category', 'Description', 'Carrot']
    data = []
    for row in df.iterrows():
    	curr_date_str = row[1]['Date']
    	curr_date = datetime.strptime(curr_date_str, '%d-%m-%Y %H:%M:%S')
    	if curr_date.date() == selected_date.date():
    		data.append([
                row[1][headers[0]],
                row[1][headers[1]],
                str(row[1][headers[2]])
            ])
    table = columnar(data, headers, terminal_width=100)
    print(table)

#Sample Usage
#tasks_on_day(df, '28-08-2020')
