str_to_write = ""

#Writes str_to_write to remarks.
def write_str() :
	f = open('../docs/remarks','a')
	f.write(str_to_write+"\n")
	f.close()