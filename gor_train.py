import pickle
import argparse
import os
import numpy as np
import GORcounter as gr


def GOR_train(model,w,dssp,profile):
	'''For each dssp and profile update the model with the GOR training algo '''
	# Initialise the window
	window = np.zeros((w//2+1,20))
	window = list(window)

	# Extract the secondary structure from file
	with open(dssp) as d:
		d.readline()
		ss = d.readline().rstrip()

	# Open the profile file & drop the header
	f = open(profile)
	f.readline()

	# Prep window for sliding: load the first w-1 lines
	while len(window)<w:
		# It's a bit cumbersome but it turns the string into float
		window.append(list(map(float, f.readline().split()[2:])))
	#~ print(len(window),window)


	# Window sliding + counting
	for i in range(len(ss)):
		window = window[1:]
		line = list(map(float, f.readline().split()[2:]))
		if line==[]:
			window.append(list(np.zeros(20)))
		else:
			window.append(line)
		# Counting
		model.update_counter(window,ss[i])

	f.close()

if __name__=='__main__':
	'''Take as input id_list dssp_path profile_path (dump_name window_size)
		p=$(pwd)
		python3 run_gor.py -l fake_id -d $p -p $p -m model1.gor -w 17 '''

	parser = argparse.ArgumentParser()
	parser.add_argument("-l", dest="id_file", help="insert list of the file ids to use in training")
	parser.add_argument("-d", dest="dssp_path", help="insert the path of the dssp files to use in training")
	parser.add_argument("-p", dest="profile_path", help="insert the path of the profile files to use in training")
	parser.add_argument("-m", dest="model_store", default='some_dump.txt', help="file to dump the model")
	parser.add_argument("-w", dest="window_size", default=5, help="insert window size to use in training", type=int)
	args = parser.parse_args()

	################# Set up for GOR #####################
	# Set window size and initialise GOR counter
	w_size = args.window_size
	GOR_counter = gr.GorCounter(w_size)

	#################### File cycling ########################
	with open(args.id_file,'r') as id_list:
		for ID in id_list:
			id_profile = os.path.join(args.profile_path, ID.rstrip()+'.profile')
			id_dssp = os.path.join(args.dssp_path, ID.rstrip()+'.dssp')
			GOR_train(GOR_counter,w_size,id_dssp,id_profile)

	###################### Results ~hopefully~ ###########################
	# Dump the model with pickle
	GOR_counter.normalize_counter()
	with open(args.model_store, 'wb') as f:
		pickle.dump(GOR_counter, f)

	###################### snippet testing  ##########################
	#~ print(test.ss_prop)
	#~ print(GOR_counter.ss_windows, GOR_counter.ss_prop, GOR_counter.window_size)

	#~ 'd1o2da_.dssp','d1o2da_.profile'
