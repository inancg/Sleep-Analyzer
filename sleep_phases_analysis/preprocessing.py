import time_unique as tu
import data_import as di
import math as m
from operator import itemgetter
import copy as cp
import matplotlib.pyplot as plt

LIGHT_SLEEP = 'lightSleep'
DEEP_SLEEP = 'deepSleep'
BAD = 1; NEUTRAL = 2; GOOD = 3
TEST_SUBJECT_ID_PP = 6771

# dict (float float) (float float) -> None
# Alters the neutral sleeps dict by assigning each neutral sleep as good or bad sleep.
def classify_neutral_sleeps(neutral_sleeps, avg_bad_sleep, avg_good_sleep):
	bad_sleep_diff = 0
	good_sleep_diff = 0
	for daily_sleep in neutral_sleeps:
		bad_sleep_diff = tu.time_to_minutes(daily_sleep[DEEP_SLEEP]) + tu.time_to_minutes(daily_sleep[LIGHT_SLEEP]) - avg_bad_sleep[0] - avg_bad_sleep[1]
		good_sleep_diff = tu.time_to_minutes(daily_sleep[DEEP_SLEEP]) + tu.time_to_minutes(daily_sleep[LIGHT_SLEEP])- avg_good_sleep[0] - avg_good_sleep[1]

		if abs(bad_sleep_diff) < abs(good_sleep_diff):
			daily_sleep['feeling'] = BAD
		else :
			daily_sleep['feeling'] = GOOD

def square(x): return x*x

# Tuple(deep_sleep, light_sleep) Tuple(deep_sleep, light_sleep) -> float
def euclidean_distance(p1, p2):
	return m.sqrt(square(p1[0]-p2[0]) + square(p1[1]-p2[1]))

# dict dict -> None
# Alters the neutral sleeps dict using k-Nearest Neighbour algorithm
def kNN_classify_neutral_sleeps(k,neutral_sleeps,data):
	neutral_sleep_count = len(neutral_sleeps)
	euc_dists = []
	for sleep in neutral_sleeps:
		good_sleep_count = 0
		bad_sleep_count = 0
		for d in data['TEST_SUBJECT_ID_PP']:
			euc_dists.append({'id':d['id'],'dist':(euclidean_distance( [tu.time_to_minutes(sleep[DEEP_SLEEP]) , tu.time_to_minutes(sleep[LIGHT_SLEEP])], [ tu.time_to_minutes(d[DEEP_SLEEP]) , tu.time_to_minutes(d[LIGHT_SLEEP]) ] ))})
		#Line 42 is taken from the answer of user J0HN http://stackoverflow.com/questions/18595686/how-does-operator-itemgetter-and-sort-work-in-python
		k_nns = sorted(euc_dists, key=itemgetter('dist'))[0:k] # k-elements
		for nbr in k_nns:
			pred_feeling = ([data['TEST_SUBJECT_ID_PP'][x]['feeling'] for x in range(0,len(data['TEST_SUBJECT_ID_PP'])) if data['TEST_SUBJECT_ID_PP'][x]['id'] == nbr['id']][0])
			if pred_feeling == 1:
				bad_sleep_count += 1
			elif pred_feeling == 3:
				good_sleep_count += 1
		if good_sleep_count >= bad_sleep_count:
			sleep['feeling'] = 3
		else:
			sleep['feeling'] = 1


# Returns difference of the timespans.
# -> list
def get_difference():
	difference = []
	for i in range(0,len(knn_data['TEST_SUBJECT_ID_PP'])):
		if (knn_data['TEST_SUBJECT_ID_PP'][i] != naive_data['TEST_SUBJECT_ID_PP'][i]):
			difference.append([knn_data['TEST_SUBJECT_ID_PP'][i][DEEP_SLEEP],knn_data['TEST_SUBJECT_ID_PP'][i][LIGHT_SLEEP]])
	return [[tu.time_to_minutes(d[0]),tu.time_to_minutes(d[1])] for d in difference]

naive_data = cp.deepcopy(di.f_data)
knn_data = cp.deepcopy(di.f_data)

# Tests for subject TEST_SUBJECT_ID_PP
avg_bad_sleep = di.get_average_sleep_in_phase('TEST_SUBJECT_ID_PP', di.f_data, feeling = [BAD]) # Average sleep phase times in bad sleeps for subject TEST_SUBJECT_ID_PP
avg_good_sleep = di.get_average_sleep_in_phase('TEST_SUBJECT_ID_PP', di.f_data, feeling = [GOOD]) # Average sleep phase times in good sleeps for subject TEST_SUBJECT_ID_PP
naive_neutral_sleeps = di.get_sleeps_for_feeling_for_subject([NEUTRAL], 'TEST_SUBJECT_ID_PP', naive_data) # Neutral sleeps dict
knn_neutral_sleeps = di.get_sleeps_for_feeling_for_subject([NEUTRAL], 'TEST_SUBJECT_ID_PP', knn_data) # Neutral sleeps dict

kNN_classify_neutral_sleeps(10,knn_neutral_sleeps,knn_data)
classify_neutral_sleeps(naive_neutral_sleeps,avg_bad_sleep,avg_good_sleep)

#Following function is taken from http://matplotlib.org/users/pyplot_tutorial.html (matplotlib development team, 2016), and modified according to the needs.
def print_results(algorithm_name):
	sleep_data = []
	if (algorithm_name == 'Naive') :
		sleep_data = naive_data['TEST_SUBJECT_ID_PP']
	elif (algorithm_name == 'k-NN'):
		sleep_data = knn_data['TEST_SUBJECT_ID_PP']
	good_sleeps = [[x[DEEP_SLEEP],x[LIGHT_SLEEP]] for x in sleep_data if x['feeling']==3]
	bad_sleeps = [[x[DEEP_SLEEP],x[LIGHT_SLEEP]] for x in sleep_data if x['feeling']==1]
	neut_sleeps =  [[x[DEEP_SLEEP],x[LIGHT_SLEEP]] for x in sleep_data if x['feeling']==2]

	diff = get_difference()

	xs = [tu.time_to_minutes(s[0]) for s in good_sleeps] + [tu.time_to_minutes(s[0]) for s in bad_sleeps] + [tu.time_to_minutes(s[0]) for s in neut_sleeps]
	ys = [tu.time_to_minutes(s[1]) for s in good_sleeps] + [tu.time_to_minutes(s[1]) for s in bad_sleeps] + [tu.time_to_minutes(s[1]) for s in neut_sleeps]

	plt.plot(xs,ys,'ro', markersize=8, label="Good Sleep", color='r')
	plt.plot(xs,ys,'ro', markersize=8, label="Bad Sleep", color='c')
	plt.plot(xs,ys,'ro', markersize=8, label="Difference", color='0.19') # Different Sleeps Grey

	for i in range(0,len(good_sleeps)): # Good Sleeps Red
		if not [xs[i],ys[i]] in diff:													 #Comment out for difference plot
			plt.plot(xs[i],ys[i],'ro', markersize=11, color='r') #Comment out for difference plot
		#plt.plot(xs[i],ys[i],'ro', markersize=11, color='r')  #Uncomment for difference plot
	for i in range(len(good_sleeps),len(good_sleeps)+len(bad_sleeps)):
		if not [xs[i],ys[i]] in diff:													 #Comment out for difference plot
			plt.plot(xs[i],ys[i],'ro', markersize=11, color='c') #Comment out for difference plot
		#plt.plot(xs[i],ys[i],'ro', markersize=11, color='c')  #Uncomment for difference plot

	plt.axis([0,380,0,550])
	plt.ylabel('Light Sleep')
	plt.xlabel('Deep Sleep')
	plt.legend(loc=2,prop={'size':20})
	plt.title("Differences in Neutral Sleep Classification")
	plt.show()

print_results('k-NN')