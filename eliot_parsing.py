import csv

import pandas as pd
import numpy as np
from pandas import isnull

path = '/home/eliot/Downloads/Data01.csv'

Data = pd.read_csv(path, comment='#', sep=',')
Column_names = list(Data.columns.values)
print(Column_names)

#parse useless columns
mapping = {'CONFIRMED':1,'FALSE POSITIVE':0, 'CANDIDATE':2}
Data['koi_disposition'] = Data['koi_disposition'].map(mapping)
Data.fillna(np.nan, inplace=True)

removing = ['kepid', 'kepoi_name', 'kepler_name', 'koi_pdisposition','koi_fpflag_nt','koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec', 'koi_score','koi_tce_delivname','koi_tce_plnt_num']
Data_dropped = Data.drop(removing,axis=1)
print(Data_dropped)

# make numpy array
DataArray = np.array(Data_dropped)


# Parse the missing fields of Data
# from data, parse the empty fields
def parser1(array: data):
	def median_finder(data, index):
		# The [:, index] slice selects all rows for one column
		median = np.nanmedian(data[:, index])
		return median

	# medians store the median (not affected by nan) of each column
	medians = []
	for i in range(len(data)):
		medians.append(median_finder(data, i))

	def null_replacer(list: row):
		i = 0
		for item in list:
			if isnull(item):
				list[i] = medians[i]
			i = i+1
		return list

	# criteria for when theres a missing field:
	# local sum of missing for each row that if it exceeds len(row)/4 we pop the row
	# if < len(row)/4 we replace missing data with pre-found medians
	for row in range(len(data)):
		rowsum = 0
		for i in range(len(data[row])):
			if isnull(data[row][i]):
				rowsum = rowsum + 1
		if rowsum >= (i/4):
			data = np.delete(data,row,axis=0)
		else:
			data[row] = null_replacer(data[row])
				# print(f'row:{r} col:{f} is None')





for r in range(len(DataArray)):
	for f in range(len(DataArray[r])):
		if isnull(DataArray[r][f]):
			#print(f'row:{r} col:{f} is None')
			pass

# Parse Data into confirmed, false-positive and candidate arrays
real_array = []
fake_array = []
mystery_array = []
random_array = []
# determinator index:
di = 3

for i in range(len(DataArray)):
	if DataArray[i,di] == 'CONFIRMED':
		real_array.append(DataArray[i])
	elif DataArray[i,di] == 'FALSE POSITIVE':
		fake_array.append(DataArray[i])
	elif DataArray[i,di] == 'CANDIDATE':
		mystery_array.append(DataArray[i])
	else:
		#should be empty
		random_array.append(DataArray[i])
