TIMESPAN_FACTOR = 50

# str dict -> list
# Returns sleeps for a day.
def get_sleeps_for_day(day,data):
	return [d for d in data if d['date']==day]

# list -> int
# Returns total time spent sleeping in a day.
def get_total_time_spent_in_day(day_data):
	result = 0
	for d in day_data:
		result += d['time_spent']
	return result

# list -> list
# Formats the day by adding time_spent
def format_day(day_data):
	total = 0
	f_data = []
	sleep_time = get_total_time_spent_in_day(day_data)
	for d in day_data:
		new_data = dict(d)
		total += new_data['time_spent']
		new_data['time_spent'] = total
		f_data.append(new_data)
	return f_data

# str dict -> (str, list)
# Returns the stages in timespans throughout the day.
def get_stage_in_timespan(day,data):
	day_data = get_sleeps_for_day(day,data)
	if (len(day_data) > 0) :
		total_time_spent = get_total_time_spent_in_day(day_data)
		f_data = format_day(day_data)
		tmp_list = []

		timespan = total_time_spent / TIMESPAN_FACTOR
		times = []
		cur_time = 0
		while cur_time<total_time_spent:
			times.append(cur_time)
			cur_time += timespan

		for time in times:
			tmp_list.append(search(time,f_data))

		while len(tmp_list) > TIMESPAN_FACTOR:
			tmp_list.pop()

		results = []
		for dat in tmp_list:
			results.append(dat)
		return (day,results)

# int list -> int
# Returns sleeps stage for at a time.
def search(time, sleep_data) :
	for day in sleep_data:
		if day['time_spent']>=time:
			return day['stage']
