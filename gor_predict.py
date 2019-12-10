import pickle
import argparse
import os
import numpy as np
import GORcounter as gr

def GOR_predict(model,w,dssp,profile):
	'''For each profile use the trainied GOR model to compute the corresponding ss '''

	# Initialise the ss string and window
	predicted_ss = ''
	window = np.zeros((w//2+1,20))
	window = list(window)

	# Open the profile file
	f = open(profile)
	f.readline()

	# Prep window for sliding: load the first w-1 lines
	while len(window)<w:
		# Turns the string into a list of floats
		window.append(list(map(float, f.readline().split()[2:])))
	#~ print(len(window),window)


	i = 0
	# Window sliding + secondary structure prediction
	while i<w//2:
		window = window[1:]
		line = list(map(float, f.readline().split()[2:]))
		if line==[]:
			window.append(list(np.zeros(20)))
			i += 1
		else:
			window.append(line)
		# Secondary structure prediction
		predicted_ss += model.assign_SS(window)

	f.close()

	# Save the predicted ss in a file
	with open(dssp,'w') as out_file:
		out_file.write('>%s\n'%os.path.basename(dssp).split('.')[0])
		out_file.write(predicted_ss+'\n')

if __name__=='__main__':
	'''Take as input id_list dssp_path profile_path (dump_name window_size)
		p=$(pwd)
		python3 gor_predict.py -l fake_id -d $p -p $p -m Gor_model.txt  '''

	parser = argparse.ArgumentParser()
	parser.add_argument("-m", dest="model_store", help="file to load the model")
	parser.add_argument("-l", dest="id_file", help="insert list of the file ids to")
	parser.add_argument("-p", dest="profile_path", help="insert the path of the profile files to perform testing")
	parser.add_argument("-d", dest="dssp_path", help="insert the path for the dssp files produced by testing")
	args = parser.parse_args()

	################# Set up for GOR #####################
	# Load the trained GOR model and extract window size
	with open(args.model_store, 'rb') as f:
		GOR_counter = pickle.load(f)
	w_size = GOR_counter.window_size
	GOR_counter.counter_to_info()

	#################### File cycling ########################
	with open(args.id_file,'r') as id_list:
		for ID in id_list:
			id_profile = os.path.join(args.profile_path, ID.rstrip()+'.profile')
			id_dssp = os.path.join(args.dssp_path, ID.rstrip()+'.gor') # output file
			GOR_predict(GOR_counter,w_size,id_dssp,id_profile)
