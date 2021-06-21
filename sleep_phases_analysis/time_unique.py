def hours(t): return int(t[:2]) * 60 # Returns hours of t(HH:MM) as minutes
def mins(t): return int(t[3:5]) # Returns minutes of t(HH:MM)
def time_to_minutes(t) : return hours(t) + mins(t) # Returns t as minutes

# str str -> int
# Substract t2 from t1 and returns the result in minutes
def get_minute_difference(t1, t2):
	return time_to_minutes(t1) - time_to_minutes(t2)