# usage python3 extract_pdb_fasta.py id_list db output (pdb)
import sys, os

def extract_tab_id(l):
	return l[0].lower()+'_'+l[1]

def extract_single_line_id(l):
	return l[0]


def file_to_dic(filename,extract_id=extract_single_line_id,header=False,field=0,value=True):
	# Extract set of IDs from file
	ID_set = []
	with open(filename) as ID:
		if header:
			ID.readline()
		else:
			for line_id in ID:
				line_id = line_id.rstrip().split('\t')
				ID_set.append((extract_id(line_id),value))
	# Using the dictionary makes matching the line id with our list faster
	ID_dict = dict(ID_set)
	return ID_dict

def extract_seq (db, ID_d, out_path):
	# Open db file and output file
	#out = open(out_file,'w')
	db_in = open(db)

	flag = 0

	# Match IDs in list and write sequences to output file
	for line in db_in:
		if line[0] == '>':
			# Memory efficient option using Bool
			line_id = line.split(' ')[0][1:]
			if ID_d.get(line_id,False):
			#~ if (ID_d.get(line.split(' ')[0][1:],0)==1):
				out = open(os.path.join(out_path, line_id+'.fasta'),'w')
				out.write(line)
				flag = 1
			else:
				flag = 0

		elif flag == 1:
			out.write(line)
			out.close()

	db_in.close()


if __name__ == "__main__":
	ID_list = sys.argv[1]
	# if the pdb option is specified parse the id_list by reconstructing the id
	if len(sys.argv)==5:
		ID_dict = file_to_dic(ID_list,extract_tab_id)
	else:
		ID_dict = file_to_dic(ID_list)
	db = sys.argv[2]
	out = sys.argv[3]
	extract_seq(db, ID_dict, out)
