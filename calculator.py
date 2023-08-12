# Copyright (C) 2023  the-astronot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.
#
# ________________
# |_File_History_|______________________________________________________________
# |_Programmer______|_Date_______|_Comments_____________________________________
# | the-astronot    | 2023-08-11 | Created File
# |
# |
# |
import os
import pickle
from math import *
import numpy as np


VERBOSE=False
LIB_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)),"lib")
loaded_files = []
var_ownership = {}
safety_vars = ["np","os","pickle","VERBOSE","loaded_files","var_ownership", "safety_vars","filename","LIB_PATH"]


def run():
	# Prints opening banner and sets vars to main
	global var_ownership
	width=os.get_terminal_size()[0]
	banner="#"*width+"\n"
	banner+="## Calculator v0.0 ##\n"
	banner+="#####################"
	print(banner)
	for var in globals():
		var_ownership[var] = "main"
	return


def import_libraries():
	# Add all python files within lib dir
	path = os.path
	for rpath, _, files in os.walk(LIB_PATH):
		#print(rpath,dir,files)
		for file in files:
			if file[-3:] == ".py":
				load(path.join(rpath,file))
	return


def load(filename):
	# Load a python file into memory
	# All vars and code in that file can then be used
	# Modifies loaded_files to make note of addition for reloading workspace
	global var_ownership
	if os.path.exists(filename) and os.path.isfile(filename):
		if VERBOSE:
			print("LOADING",filename)
		exec(open(filename).read())
		local_vars = locals().copy()
		if VERBOSE:
			print(local_vars)
		for key in local_vars:
			globals()[key] = locals()[key]
			var_ownership[key] = os.path.basename(filename.replace(".py","")).lower()
		full_filename = os.path.abspath(filename)
		if not full_filename in loaded_files:
			loaded_files.append(full_filename)


def load_workspace(filename):
	# Reload saved workspaces
	# If necessary file cannot be found, gives option to redefine missing file
	global var_ownership
	filename = add_wksp_ext(filename)
	if not os.path.exists(filename):
		print("ERROR: Workspace not found")
		return
	impfile = getimpfile(filename)
	if os.path.exists(impfile):
		updated_imp = 0
		files = pickle.load(open(impfile,"rb"))
		for file in files:
			if os.path.exists(file):
				load(file)
			else:
				replaced = 0
				while not replaced:
					x = input("FILE: {} not found, specify new path? (Y/n): ".format(file))
					if len(x) == 0 or x[1].lower() != "n":
						newfile=input("Enter updated file location: ")
						if os.path.exists(newfile):
							replaced = 1
							updated_imp = 1
				load(newfile)
				files[files.index(file)] = newfile
		if updated_imp:
			pickle.dump(files,open(impfile,"wb"),protocol=pickle.HIGHEST_PROTOCOL)
	data = pickle.load(open(filename,"rb"))
	for key in data:
		print(key,type(data[key]),data[key])
		if key == "var_ownership":
			for var in data:
				if not var in safety_vars:
					var_ownership[var] = os.path.basename(filename.replace(".wksp","")).lower()
		else:
			globals()[key] = data[key]


def save_workspace(filename):
	# Save current workspace vars, functions, etc
	filename = add_wksp_ext(filename)
	if os.path.exists(filename):
		x = input("Workspace \"{}\" already exists. Overwrite? (y/N): ".format(filename))
		if (len(x) == 0 or x[0].lower() != "y"):
			return
	data = {}
	for key in globals():
		if (type(globals()[key]) != type(np) and not callable(globals()[key]) and key[:2] != "__"):
			if VERBOSE:
				print(key,type(globals()[key]),globals()[key])
			data[key] = globals()[key]
	pickle.dump(data,open(filename,"wb"),protocol=pickle.HIGHEST_PROTOCOL)
	if len(loaded_files)>0:
		impfile = getimpfile(filename)
		pickle.dump(loaded_files,open(impfile,"wb"),protocol=pickle.HIGHEST_PROTOCOL)
	print("Workspace saved to file:",filename)


def clear_workspace(source = None):
	# Clears current workspace of variables from [source]
	# If no source is specified, defaults to main
	global var_ownership
	global_vars = globals().copy()
	for var in global_vars:
		if source is None or source == "main":
			if len(var) > 2 and var[:2] == "__":
				pass
			elif type(global_vars[var]) == type(save_workspace) and (
				not var in var_ownership or var_ownership[var] == "main"
			):
				pass
			elif var in safety_vars:
				pass
			else:
				globals().pop(var)
				if var in var_ownership:
					var_ownership.pop(var)
		else:
			for var in global_vars:
				if var in var_ownership:
					if var_ownership[var] == source:
						globals().pop(var)
						var_ownership.pop(var)
	globals()["loaded_files"] = []


def print_workspace(filename=None):
	# Prints workspace variables in workspace [filename]
	# If no workspace is selected, current workspace is used
	filename = add_wksp_ext(filename)
	if (filename is None):
		data = {}
		for key in globals():
			if (type(globals()[key]) != type(np) and type(globals()[key]) != type(print) and key[:2] != "__"):
				if not VERBOSE and key in safety_vars:
					pass
				else:
					data[key] = globals()[key]
	elif not os.path.exists(filename):
		print("ERROR: Workspace not found")
		return
	else:
		data = pickle.load(open(filename,"rb"))
	for key in data:
		owner = "main"
		if key in var_ownership:
			owner = var_ownership[key]
		print("[{0}]\t=\t[{1}]\t[{2}]".format(key,data[key],owner))


def rm_workspace(filename):
	# Deletes a workspace file [filename]
	filename = add_wksp_ext(filename)
	if os.path.exists(filename):
		os.remove(filename)
	else:
		print("ERROR: Workspace not found")
	return


def print_sources():
	# Lists all sources that own data in current workspace
	sources = []
	for key in var_ownership:
		if not var_ownership[key] in sources:
			sources.append(var_ownership[key])
	print("Current Sources:")
	for source in sources:
		print("\t{}".format(source))


def add_wksp_ext(filename):
	# Adds workspace extension if not included
	if filename is None:
		return None
	elif filename.find(".wksp") == -1:
		return filename+".wksp"
	return filename


def getimpfile(filename):
	# Gets import file from filename
	basename = os.path.basename(filename)
	pathname = os.path.dirname(filename)
	basename = "." + basename
	return os.path.join(pathname,basename)


if __name__ == '__main__':
	run()
	import_libraries()
