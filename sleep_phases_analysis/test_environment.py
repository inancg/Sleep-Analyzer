#! /usr/bin/env python3.4
import preprocessing as pp
import data_import as di
import time_unique as tu
import random as r
import write_to_remarks as w2r
from operator import itemgetter

LIGHT_SLEEP = 'lightSleep'
DEEP_SLEEP = 'deepSleep'
TIMES_TESTED = 50
TEST_SUBJECT_ID = 6771

af_data = dict(pp.di.f_data)

avg_bad_sleep = di.get_average_sleep_in_phase('TEST_SUBJECT_ID', af_data, feeling = [1]) # Average sleep phase times in bad sleeps for subject TEST_SUBJECT_ID
avg_good_sleep = di.get_average_sleep_in_phase('TEST_SUBJECT_ID', af_data, feeling = [3]) # Average sleep phase times in good sleeps for subject TEST_SUBJECT_ID

knn_classified_test_set = dict(pp.knn_data)['TEST_SUBJECT_ID']
naive_classified_test_set = dict(pp.naive_data)['TEST_SUBJECT_ID']

# list -> int
# Returns the number of correct predictions of a test set using k-means-like implementation
def naive_test(test_samples):
	correct = 0
	for daily_sleep in test_samples:
		bad_sleep_diff = tu.time_to_minutes(daily_sleep['lightSleep']) + tu.time_to_minutes(daily_sleep['deepSleep']) - avg_bad_sleep[0] - avg_bad_sleep[1]
		good_sleep_diff = tu.time_to_minutes(daily_sleep['lightSleep']) + tu.time_to_minutes(daily_sleep['deepSleep'])- avg_good_sleep[0] - avg_good_sleep[1]
		guess = 0
		if abs(bad_sleep_diff) < abs(good_sleep_diff):
			guess = 1
		else :
			guess = 3

		if guess==daily_sleep['feeling']:
			correct += 1
	return correct

# int list -> int
# Returns the number of correct predictions of a test set using k-NN with k=k
def knn_test(k,test_samples):
	test_count = len(test_samples)
	euc_dists = []
	prediction = 0
	correct = 0
	for sleep in test_samples:
		good_sleep_count = 0
		bad_sleep_count = 0
		for d in test_samples:
			euc_dists.append({'id':d['id'],'dist':(pp.euclidean_distance( [tu.time_to_minutes(sleep[DEEP_SLEEP]) , tu.time_to_minutes(sleep[LIGHT_SLEEP])], [ tu.time_to_minutes(d[DEEP_SLEEP]) , tu.time_to_minutes(d[LIGHT_SLEEP]) ] ))})
		#Line 46 is taken from the answer of user J0HN http://stackoverflow.com/questions/18595686/how-does-operator-itemgetter-and-sort-work-in-python
		k_nns = sorted(euc_dists, key=itemgetter('dist'))[0:k] # k-elements
		#Checks the feelings of the neighbours
		for nbr in k_nns:
			pred_feeling = ([test_samples[x]['feeling'] for x in range(0,test_count) if test_samples[x]['id'] == nbr['id']][0])
			if pred_feeling == 1:
				bad_sleep_count += 1
			elif pred_feeling == 3:
				good_sleep_count += 1
		#Predict
		if good_sleep_count >= bad_sleep_count:
			prediction = 3
		else:
			prediction = 1
		#Check prediction
		if prediction == sleep['feeling']:
			correct += 1
	print(correct)
	return correct

# int int -> str
#Returns accuracy as a string
def accuracy_as_str(correct,total):
	return str(correct/float(total))

#list int -> 
#Main method for testing and logging to /docs/remarks file.
def test_it(data_set, count):
	#Take Sample
	test_samples = (r.sample(data_set,count))
	#End Take Sample
	stw = "" #str_to_write

	naive_correct = naive_test(test_samples)
	stw += accuracy_as_str(naive_correct, count)[:4]

	knn_correct = knn_test(3,test_samples)
	stw += "\t\t"+accuracy_as_str(knn_correct, count)[:4]

	knn_correct = knn_test(5,test_samples)
	stw += "\t\t"+accuracy_as_str(knn_correct, count)[:4]

	knn_correct = knn_test(10,test_samples)
	stw += "\t\t"+accuracy_as_str(knn_correct, count)[:4]

	w2r.str_to_write = stw
	w2r.write_str()

#Tests the algorithms for TIMES_TESTED times.
for i in range(0,TIMES_TESTED) : test_it(knn_classified_test_set,7)