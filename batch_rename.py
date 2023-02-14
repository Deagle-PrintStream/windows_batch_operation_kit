import sys,os
from math import log10,floor
from fnmatch import fnmatch 

brief="""\
A simple script to batch rename files in same directory.\n\
Arguments to input: \n\
target directory; substring for filter;\n\
prefix for rename; suffix for rename; sort order\n\
A complete well-rounded example:\n\
`$python batch_rename -d D:/pictures/pixiv R12/ -ss *.jpg -pf anime_ -sf .jpg -so mtime`\n\
Easy mode to modify all files in one dir:\n\
`$python bathc_rename -ez D:/pictures/pixiv R12/`\n\
Or you can directly luanch the script by \n\
`$python batch_rename` and input parameters within.\n\
Wherein -d and -ss are necessary.\n\
If -sf left default then original suffix remains still.\n\
Sort order choices: mtime, ctime, atime, size, name.\n"""

def preocess_argv(argv:list[str])->list[str]:
	command_list:list[str]=["-d","-ss","-pf","-sf","-so","-ez"]
	cmd_arg_dict:dict[str,str]=dict(zip(command_list,[""]*len(command_list)))
	help_cmd_list:list[str]=["-h","h","help","--h"]

	#no argument given by system
	if len(argv)==1:
		return input_args()
	
	#unexpected arg or help arg
	if argv[1] in help_cmd_list or argv[1] not in command_list:
		help()

	#correct arg processing
	for command in command_list:
		if command in argv:
			args:list[str]=[]
			for word in argv[argv.index(command)+1:]:
				if word not in command_list:
					args.append(word)
				else:
					break			
			cmd_arg_dict[command]=" ".join(args)
	
	#easy mode for all files contained renaming
	if cmd_arg_dict["-ez"]!="":
		return [cmd_arg_dict["-ez"],"*","","","mtime"]
		
	return list(cmd_arg_dict.values())[0:5]

def locate_files(dir:str,contain_str:str,sort_order)->list[os.DirEntry[str]]:
	#check if directory exists
	try:
		os.chdir(dir)
	except OSError as reason:
		print("No such directory.")
		print(str(reason))
		exit(-1)

	file_list:list[os.DirEntry[str]]=[]
	
	with os.scandir(dir) as entries:
		for entry in entries:
			if entry.is_file():
				file_list.append(entry)
	if len(file_list)==0:
		print("Empty directory.")
		exit(-1)

	#check if exists files name containing target substring
	if len(contain_str)>0:
		for file in file_list:
			if fnmatch(file.name,contain_str)==0:
				file_list.remove(file)
	if len(file_list)==0:
		print("No file with conditional name.")
		exit(-1)
	
	#sort the list by last modified time
	if sort_order=="mtime" or sort_order=="": #from early to late
		file_list.sort(key=lambda x:x.stat().st_mtime,reverse=True)
	elif sort_order=="name": #from A to Z
		file_list.sort(key=lambda x:x.name,reverse=True)
	elif sort_order=="atime":
		file_list.sort(key=lambda x:x.stat().st_atime,reverse=True)
	elif sort_order=="ctime":
		file_list.sort(key=lambda x:x.stat().st_ctime,reverse=True)
	elif sort_order=="size": #from large to small
		file_list.sort(key=lambda x:x.stat().st_size,reverse=True)

	return file_list

def batch_rename(file_list:list[os.DirEntry[str]],prefix:str,suffix:str)->None:
	file_count=len(file_list)	
	zfill_count=floor(log10(file_count))+1		
	#fullfill the sequential numbers by zeros, like 001,002,003
	sequence_list=[str(x).zfill(zfill_count) for x in range(1,file_count+1)] 
	new_name_list=[prefix+s for s in sequence_list]
	if suffix!="":
		#change the suffix
		new_name_list=[prefix+s+suffix for s in sequence_list]
	else:
		#no preset suffix changing, then keep them still
		suffix_list:list[str]=["."+file.name.split(".")[-1] for file in file_list]	
		new_name_list=[prefix+s+sf for s,sf in zip(sequence_list,suffix_list)]

	#avoid that new name already exists
	tmp_str:str="tmp"
	for file in file_list:
		os.rename(file.name,str(file.name)+tmp_str)

	for file,new_name in zip(file_list,new_name_list):
		try:
			os.rename(file.name+tmp_str,new_name)		
		except FileExistsError:
			file_count-=1
			continue				
		
	print("Totally %d files renamed."% file_count)
	return None

def input_args()->list[str]:
	dir=input("Input the target directory:")
	contain_str=input("Input the target searching substring:")
	prefix=input("Input the prefix:")
	suffix=input("Input the suffix:")
	sort_order=input("Input the sort order:")
	return [dir,contain_str,prefix,suffix,sort_order]

def help()->None:
	print(brief)
	exit(0)

def main()->None:
	[dir,contain_str,prefix,suffix,sort_order]=preocess_argv(sys.argv)		
	file_list=locate_files(dir,contain_str,sort_order)
	batch_rename(file_list,prefix,suffix)
	
	return None
	
if __name__=="__main__":
	main()
