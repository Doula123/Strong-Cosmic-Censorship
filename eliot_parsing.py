import pandas as pd
import numpy as np
from pandas import isnull

def parser1(data):
	# Parse the missing fields of Data
	# from data, parse the empty fields
	def median_finder(data, index):
		# The [:, index] slice selects all rows for one column
		median = np.nanmedian(data[:, index])
		return median

	def null_replacer(row):
		i = 0
		for item in row:
			if isnull(item):
				row[i] = medians[i]
			i = i+1
		return row

	# medians store the median (not affected by nan) of each column, iterate over the columns!!!
	medians = []
	for i in range(data.shape[1]):
		medians.append(median_finder(data, i))


	# criteria for when theres a missing field:
	# local sum of missing for each row that if it exceeds len(row)/4 we pop the row
	# if < len(row)/4 we replace missing data with pre-found medians
	to_delete = []
	for row_index in range(len(data)):
		rowsum = 0
		for i in range(len(data[row_index])):
			if isnull(data[row_index][i]):
				rowsum = rowsum + 1
		if rowsum >= (i/4):
			to_delete.append(row_index)
		else:
			data[row_index] = null_replacer(data[row_index])
	data = np.delete(data,to_delete,axis=0)
	return data




if __name__ == '__main__':
	path = '/home/eliot/Downloads/Data01.csv'

	Data = pd.read_csv(path, comment='#', sep=',')
	Column_names = list(Data.columns.values)
	print(Column_names)

	#replace confirmed, false positive and candidate with integers
	mapping = {'CONFIRMED':1,'FALSE POSITIVE':0, 'CANDIDATE':2}
	Data['koi_disposition'] = Data['koi_disposition'].map(mapping)

	#replace all null values with np.nan (required for parser1())
	Data.fillna(np.nan, inplace=True)

	#remove useless and redundant parameters
	dropped_parameters = ['kepid', 'kepoi_name', 'kepler_name', 'koi_pdisposition','koi_fpflag_nt','koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec', 'koi_score','koi_tce_delivname','koi_tce_plnt_num']
	Data_dropped = Data.drop(dropped_parameters,axis=1)

	# make numpy array
	DataArray = np.array(Data_dropped)
	# parse out empty fields
	DataParsed = parser1(DataArray)
	print(DataParsed)


	# Parse Data into confirmed, false-positive and candidate arrays
	real_array = np.array([])
	fake_array = []
	mystery_array = []
	random_array = []
	# determinator index:
	di = 3

	for i in range(len(DataParsed)):
		if DataParsed[i,di] == 1:
			real_array = np.append(real_array, DataParsed[i],axis=0)
		elif DataParsed[i,di] == 0:
			fake_array.append(DataParsed[i])
		elif DataParsed[i,di] == 2:
			mystery_array.append(DataParsed[i])
		else:
			#should be empty
			random_array.append(DataParsed[i])

	df = pd.DataFrame(real_array)
	df.to_csv('output_test.csv')