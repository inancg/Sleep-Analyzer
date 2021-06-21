import time_unique as tu
import json
import formatter
import mathematical_calculations as mc

file_path = "../docs/d914_sleeps.json"
sample_count = formatter.TIMESPAN_FACTOR

# str -> list
#Imports data as json and returns formatted version
def import_data(file_path):
	with open(file_path,'r') as f:
		tmp = json.loads(f.read())
		return tmp['sleeps']

# list -> list
# Returns unique dates in the data
def get_unique_dates(data):
	dates = []
	for d in data:
		dates.append(d['date'])
	return set(dates)

# list -> dict
# Crowds the dates as dictionary with corresponding data.
def crowd_date_data(dates):
	result = {}
	for date in dates :
		date_data = formatter.get_stage_in_timespan(date,data)
		result[date_data[0]] = date_data[1]
	return result


data = import_data(file_path)
dates = get_unique_dates(data)
result = crowd_date_data(dates)
means = mc.mean(dates,result)
#correlations = {}
#for t in range(0,len(means)):
#	correlations[t] = [mc.correlation_in_t(dates,result,t,i) for i in range(0,len(means))]
std_dev = mc.standard_deviation(dates,result)

# Creates plot.
def show(results= std_dev, start_from=0, end_at=formatter.TIMESPAN_FACTOR) :
	r = range(start_from,end_at)
	mc.plt.plot(r,std_dev[start_from:end_at],linewidth=1,label='Standard Deviation')
	mc.plt.plot(r,means[start_from:end_at],linewidth=1,color="r",label='Means')
	mc.plt.xlabel("Timespan")
	mc.plt.ylabel("Standard Deviation")
	mc.plt.show()

show()

# -> list
# Returns covariance matrix
def get_covariance_matrix():
	covariance_matrix = []
	for i in range(0,formatter.TIMESPAN_FACTOR):
		tmp_covariances = []
		for j in range(0,formatter.TIMESPAN_FACTOR):
			tmp_covariances.append(mc.covariance(dates,result,i,j))
		covariance_matrix.append(tmp_covariances)

	return covariance_matrix

# ->
# Logs the evaluated covariance matrix.
def log_covariance_matrix():
	cov_matrix = get_covariance_matrix()
	cm = open('../docs/d914_covariance','a')
	cm.write("[")
	for elem in cov_matrix:
		cm.write(str(elem)+",")
	cm.write("]")
	cm.close()