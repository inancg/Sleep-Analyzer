import json
import time_unique as tu

LIGHT_SLEEP = 'lightSleep'
DEEP_SLEEP = 'deepSleep'
FEELINGS = [1,2,3]

test_data = json.load(open('testData.json'))

subject_ids = ['d914','6771','32b6']

# list dict -> dict
# Used for getting formatted dictionaries for subjects(s_ids)
def format_sleeps(s_ids, data):
	sleeps = {}
	for s_id in s_ids:
		sleeps[s_id] = [{'id' : datum['id'], 'lightSleep' : datum[LIGHT_SLEEP], 'deepSleep' : datum[DEEP_SLEEP], 'feeling' : datum['feeling']} for datum in data if (datum['subject_id']==s_id)]
	return sleeps

# list str dict -> list
# Returns all of the sleeps with the selected feelings for a subject(s_id)
def get_sleeps_for_feeling_for_subject(feelings, s_id, data):
	result = []
	for feeling in feelings :
		result += [datum for datum in data[s_id] if feeling == datum['feeling']]
	return result

# str dict list -> (float float)
# Returns average values of time spent in deep sleep and light sleep for a subject(s_id) using only data with selected feelings
def get_average_sleep_in_phase(s_id, formatted_data, feeling = FEELINGS):
	result_light = 0
	result_deep = 0
	subject_sleeps = get_sleeps_for_feeling_for_subject(feeling,s_id,formatted_data)
	sleep_count = float(len(subject_sleeps))
	for daily_sleep in subject_sleeps :
		result_light += tu.time_to_minutes(daily_sleep[LIGHT_SLEEP])
		result_deep += tu.time_to_minutes(daily_sleep[DEEP_SLEEP])
	return result_deep/sleep_count, result_light/sleep_count

#Examples
f_data = format_sleeps(subject_ids,test_data)