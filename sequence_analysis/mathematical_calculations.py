import formatter
from matplotlib import pyplot as plt

# Finds the mean for each timespan.
def mean(dates,data):
	result = []
	for t in range(0,formatter.TIMESPAN_FACTOR):
		result.append(mean_helper(dates,data,t))
	return result
# Helper
def mean_helper(dates,data,t):
	result = {}
	count = 0.0
	total = 0
	for date in dates:
		count += 1
		total += altered_value(data[date][t])
	return total/count

# Finds variance for each timespan
def variance(dates,data):
	result = []
	means = mean(dates,data)
	for t in range(0,formatter.TIMESPAN_FACTOR):
		result.append(variance_helper(dates,data,t,means))
	return result
# Helper
def variance_helper(dates,data,t,means):
	result = {}
	count = 0.0
	total = 0
	for date in dates:
		count += 1
		total += square(altered_value(data[date][t]) - means[t])
	return round(total/count, 4)

# Finds standard deviation for each timespan
def standard_deviation(dates,data):
	return list(map((lambda x: round(x**(0.5),4)), variance(dates,data)))

# Finds the correlation between two values of time.
def correlation_in_t(dates,data,t,tt):
	means = mean(dates,data)
	for i in range(0,len(dates)-1):
		date = list(dates)[i]
		day_data = data[date]
		result = 0
		for i in range(0,len(day_data)):
			result += day_data[t]-means[t] + day_data[tt]-means[tt]
		return round(result/float(len(day_data)),4)

# Finds the covariance between two values of time.
def covariance(dates,data,t,tt):
	cor = correlation_in_t(dates,data,t,tt)
	std_dev = standard_deviation(dates,data)
	s_dev_t = std_dev[t]
	s_dev_tt = std_dev[tt]
	print (dates)

	return round(cor / float((s_dev_t*s_dev_tt)),4)

# Light Sleep -> 0
# Deep Sleep -> 1
# Awake -> 0.5 (not affecting)
def altered_value(val):
	if val == 2:
		return 0
	elif val == 3:
		return 1
	else:
		return 0.5

def square(x): return (x*x)
def sqrt(x): return (x**(0.5))