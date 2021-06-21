from datetime import datetime
import requests, json
date_format_formula = '%Y-%m-%dT%H:%M:%S'
# Request and Response Block
request_header = {'access_token':''} #Access token here
request_url = 'https://api.misfitwearables.com/move/resource/v1/user/me/activity/sleeps'
request_params = {'start_date': '2016-05-06', 'end_date': '2016-05-29'}
response_raw = requests.get(request_url, params=request_params, headers = request_header)
response = json.loads(response_raw.text)
# End Request and Response Block

# int -> str
# Returns the corresponding steep stage's name.
def format_value(value) :
	if value == 1:
		return "awake"
	elif value == 2:
		return "light"
	else :
		return "deep"

# datetime datetime -> float
# Returns the time spent between start_time and end_time
def get_times_spent_in_stages(start_time,end_time):
	delta_time = end_time - start_time
	time_difference_in_minutes = delta_time.seconds // 60
	return time_difference_in_minutes

# datetime -> list
# Gathers information on sleep stages on a day.
def gather_data_for_day(day):
	sleep_details = day['sleepDetails']
	result = []
	for i in range(0,len(sleep_details)-1):
		time_HMS = datetime.strptime(sleep_details[i]['datetime'][:19], date_format_formula)
		next_HMS = datetime.strptime(sleep_details[i+1]['datetime'][:19], date_format_formula)
		day = sleep_details[i]['datetime'][:10]
		result.append([time_HMS,get_times_spent_in_stages(time_HMS,next_HMS), sleep_details[i]['value'],day])
	return result

# Response -> list
# API-based function. Gathers data for days that have information about sleeps.
def gather_data_included(response):
	result = []
	for day in response['sleeps']:
		if(len(day['sleepDetails']) != 0):
			result.append(gather_data_for_day(day))
	return result

# None -> list
# Main function
def gather_data():
	return gather_data_included(response)


f = open('','a') #Filename here
data = gather_data()
for day in data:
	for element in day:
		f.write("{\"date\":\""+str(element[3])+"\",\"stage\":"+str(element[2])+",\"time_spent\":"+str(element[1])+"},\n")
		print("123")
f.close()
