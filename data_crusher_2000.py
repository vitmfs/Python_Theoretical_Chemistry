#!/usr/bin/python

# to use the program type in the console:
# python name_of_program.py name_of_file.gro atom1 atom2
# Example:
# python data_crusher_2000.py pe_prod.gro OP9 HH7


import sys
import numpy

from math import sqrt

print "\nWelcome to Data Crusher 2000! (pe_prod.gro version!!!)"

##### FUNCTION THAT READS FILE INTO LIST OF LINES #####

def getValuesFromFile(path):

	with open(path) as f:
		lines = f.read().splitlines();

	return lines

#######################################################

##### FUNCTION THAT GETS LINES WITH INTEREST ##########

def getLinesOfInterest(original_lines):

	# variable strings_of_interest will contain strings
	# that we want
	strings_of_interest = ["OR6", "HH7", "OP9", "HO10"]

	# variable lines_of_interest starts empty but
	# will be filled will lines of interest
	lines_of_interest = []

	for original_line in original_lines:

		for string_of_interest in strings_of_interest:

			if string_of_interest in original_line:
				
				lines_of_interest.append(original_line)
	
	return lines_of_interest

######################################################

##### FUNCTION THAT DISCARDS IRRELEVANT INFO #########

def cleanInformationFromLines(lines):

	for line in lines:

		line = line.strip()

	return lines

######################################################


##### FUNCTION THAT PRINTS A LIST ####################

def printList(list):

	for l in list:
	
		
		print l +" " + str(len(l))

#####################################################

##### FUNCTION THAT PRINTS A LIST OF LISTS ###########

def printListOfLists(list_of_lists):

	for list in list_of_lists:

		print list

######################################################

##### FUNCTION THAT EXTRACS IMPORTANT INFORMATION ####

def extractRelevantInfo(cleaned_lines_of_interest):
	
	atoms = []

	for i in range(len(cleaned_lines_of_interest)):

		#print list[i]

		temporary_words = cleaned_lines_of_interest[i].split()
		
		atom_information = []

		if  "OP91" in temporary_words[1] or "HH71" in temporary_words[1] or "OR61" in temporary_words[1] or "HO101" in temporary_words[1]:

			atom_information.append(temporary_words[0])
			atom_information.append(temporary_words[1])
			atom_information.append(float(temporary_words[2]))
			atom_information.append(float(temporary_words[3]))
			atom_information.append(float(temporary_words[4]))
			#atom_information.append(temporary_words[5])
		else:

			atom_information.append(temporary_words[0])
			atom_information.append(temporary_words[1])
			#atom_information.append(temporary_words[2])
			atom_information.append(float(temporary_words[3]))
			atom_information.append(float(temporary_words[4]))
			atom_information.append(float(temporary_words[5]))


		#print atom_information[0] + " " + atom_information[1] + " " + atom_information[2] + " " + atom_information[3] + " " + atom_information[4] + " " + atom_information[5]

		atoms.append(atom_information)
			
	return atoms


######################################################

##### FUNCTION THAT CORRECTS NAME OF SINGLE ATOM #####

def correctsNameOfAtom(atom_information):

	if "OP9" in atom_information[1] or "OP91" in atom_information[1]:

		atom_information[1] = "OP9"

	if "HH7" in atom_information[1] or "HH71" in atom_information[1]:

		atom_information[1] = "HH7"

	if "OR6" in atom_information[1] or "OR61" in atom_information[1]:

		atom_information[1] = "OR6"

	if "HO10" in atom_information[1] or "HO101" in atom_information[1]:

		atom_information[1] = "HO10"

	return atom_information

#######################################################


##### FUNCTION THAT CORRECTS ALL ATOM NAMES ###########


def correctAllNames(list_of_lists):

	for i in range(len(list_of_lists)):

		list_of_lists[i] = correctsNameOfAtom(list_of_lists[i])


	return list_of_lists

#######################################################

##### FUNCTION THAT MAKES ALL CALCULATIONS ##############

def makesAllCalculations(information_matrix, atom1, atom2):

	string_to_write = ""

	for each_atom_info_list in information_matrix:

		for another_atom_info_list in information_matrix:

			if each_atom_info_list[0] != another_atom_info_list[0]:
			
				#print each_atom_info_list[0] + " " + another_atom_info_list[0]
				if each_atom_info_list[1] == atom1 and another_atom_info_list[1] == atom2:

					#point_a = numpy.array( ( each_atom_info_list[2], each_atom_info_list[3], each_atom_info_list[4] ) )
					#point_b = numpy.array( ( another_atom_info_list[2], another_atom_info_list[3], another_atom_info_list[4]) )
					
					xa = each_atom_info_list[2]
					ya = each_atom_info_list[3]
					za = each_atom_info_list[4]

					xb = another_atom_info_list[2]
					yb = another_atom_info_list[3]
					zb = another_atom_info_list[4]

					dist_method_01 = distanceMethod01(xa, ya, za, xb, yb, zb) #sqrt((xa-xb)**2 + (ya-yb)**2 + (za-zb)**2)
					

					

					if dist_method_01 < 0.35:

						#print "Distance between " + each_atom_info_list[0] + "'s " + each_atom_info_list[1] + " and " + another_atom_info_list[0] + "'s " + another_atom_info_list[1] + ": " + str(dist_method_01)

						string_to_write += "Distance between " + each_atom_info_list[0] + "'s " + each_atom_info_list[1] + " and " + another_atom_info_list[0] + "'s " + another_atom_info_list[1] + ": " + str(dist_method_01) + "\n"

			
	#print string_to_write			
	name_of_output_file = "dist_" + atom1 + "_" + atom2 +"_dist.txt"

	text_file = open(name_of_output_file, "w")
	text_file.write(string_to_write)
	text_file.close()

#########################################################

##### FUNCTION THAT RETURNS DISTANCE BETWEEN TWO POINTS ########

def distanceMethod01(xa, ya, za, xb, yb, zb):   
	
	dist = sqrt((xa-xb)**2 + (ya-yb)**2 + (za-zb)**2)

	return dist


# https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy

################################################################

##### MAIN PROGRAM ###################################

print "\nProcessing... please hold!\n"

try:

	#print sys.argv[0]


	#print sys.argv[1]
	path = sys.argv[1]

	#print sys.argv[2]
	atom1 = sys.argv[2]

	#print sys.argv[3]
	atom2 = sys.argv[3]

except IndexError:

	print "\nExample of use: \n"
	print "python name_of_script.py path_of_file_to_analyse.gro atom1 atom2 \n"
	print "Please try again!\n"

	sys.exit()

original_lines = getValuesFromFile(path) #"/home/vitmfs/pe_prod.gro")
#print "original lines: " + str(len(original_lines))
#print original_lines[3]
#print original_lines[len(original_lines)-2]

lines_of_interest = getLinesOfInterest(original_lines)
#print "lines of interest: " + str(len(lines_of_interest))
#print lines_of_interest[0]
#print lines_of_interest[3455]

cleaned_lines_of_interest = cleanInformationFromLines(lines_of_interest)
#print "cleaned lines of interest: " + str(len(cleaned_lines_of_interest))
#print cleaned_lines_of_interest[0]
#print cleaned_lines_of_interest[3455]

relevant_info = extractRelevantInfo(cleaned_lines_of_interest)
#print "relevant info: " + str(len(relevant_info))
#print relevant_info[0]
#print relevant_info[3455]

information_matrix = correctAllNames(relevant_info)
#print "information matrix: " + str(len(information_matrix))
#print information_matrix[0]
#print information_matrix[3455]

#printListOfLists(information_matrix)

makesAllCalculations(information_matrix, sys.argv[2], sys.argv[3])

print "Done!\n"	

print "Thank you, have a nice day!\n"
