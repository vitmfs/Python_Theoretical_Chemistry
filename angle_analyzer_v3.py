#!/usr/bin/python

import sys
import os
import numpy
import math
from math import acos, degrees
import time



def getLinesFromFile(path):

	with open(path) as f:

		lines = f.read().splitlines()

	#lines = [x.strip() for x in lines] 


	return lines

	"""
	THIS FUNCTION THAT GETS LINES FROM 
	THE DATA FILE SPECIFIED IN THE PATH
	"""
	#print "called getLinesFromFile(path)"


def isStepLine( line ):
	
	if "Step" in line:
		
		return True
	else:
	
		return False

		"""
		THIS FUNCTION DETERMINES IF THE 
		LINE CONTAINS THE WORD Step
		"""

def isLineWithDesiredDistance( line, desired_distance ):

	string_to_search = "d=" + str( desired_distance )

	if string_to_search in line:

		return True

	"""
	THIS FUNCTION DETERMINES IF THE LINE 
	HAS THE DESIRED DISTANCE
	"""

	
def getWantedSteps( original_lines, desired_distance, number_of_atoms ):

	wanted_steps = []
	

	for i in range( 0, len( original_lines ) ):

		if 	isStepLine( 	original_lines[i] ) and \
			isLineWithDesiredDistance( original_lines[i], desired_distance ):

			wanted_steps.append( "  " + str( number_of_atoms) )

			wanted_steps.append( original_lines[i] )

			for j in range( 1, number_of_atoms + 1 ):
			
				wanted_steps.append( original_lines[i+j] )


	

	return wanted_steps

	"""
	THIS FUNCTION RETURNS THE LINES OF INTEREST,
	THE STEP LINES WITH THE DISTANCE AND THE
	LINES WITH THE ATOM
	"""

def getInfoStringToWriteToFile( lines_of_interest ):

	stringToWrite = ""

	for i in range( 0, len( lines_of_interest ) ):

		if isStepLine( lines_of_interest[i] ):

			stringToWrite += ""

		stringToWrite += str( lines_of_interest[i] ) + "\n"

		

	return stringToWrite

	"""
	TRANSFORMS THE LIST OF LINES 
	INTO A STRING TO WRITE
	TO ANOTHER FILE
	"""

def writesToFile( chosen_prefix, original_name_of_file, string_to_write ):


	name_of_output_file = chosen_prefix + str( original_name_of_file )
	
	text_file = open(name_of_output_file, "w")
	text_file.write(string_to_write)
	text_file.close()
	
	"""
	THIS FUNCTION WRITES THE STRING WITH
	THE DESIRED STEP INFO TO A SEPARATE
	FILE
	"""

	
def inputWantedRows():
	
	number_of_rows = 3
	list_of_row_numbers_we_want = []

	for i in range (0, number_of_rows):

		if i == 0:
			
			print "Enter first number of row (Ray1 of Angle)"

		if i == 1:
			
			print "Enter second number of row (Vertex of Angle)"

		
		if i == 2:
			
			print "Enter third number of row (Ray2 of Angle)"

		inputed_number_of_row = raw_input()
		
		list_of_row_numbers_we_want.append( inputed_number_of_row )

	return list_of_row_numbers_we_want


def getLinesOfAtomsOfInterest( lines, list_of_row_numbers_we_want ):

	list_of_atoms_of_interest = []

	for i in range( 0, len( lines )  ):


		if isStepLine( lines[i] ):

			#list_of_atoms_of_interest.append( lines[i] )

			for j in range( 0, len( list_of_row_numbers_we_want )  ):

				list_of_atoms_of_interest.append( lines[i + int(list_of_row_numbers_we_want[j])] + "\t" + list_of_row_numbers_we_want[j])


	return list_of_atoms_of_interest






def calculateDistanceBetween3DPoints( coords1, coords2 ):

	#print str( coords1 )
	#print str( coords2)

	x2 = coords2[0]
	x1 = coords1[0]

	y2 = coords2[1]
	y1 = coords1[1]

	z2 = coords2[2]
	z1 = coords1[2]

	distance = math.sqrt( (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )

	return distance

	# https://stackoverflow.com/questions/20184992/finding-3d-distances-using-an-inbuilt-function-in-python


def calculateAngle( distance_BA, distance_BC, distance_AC ):

	#print "Calculate Angle"
	#print str( distance_BA )
	#print str( distance_BC )
	#print str( distance_AC )
	#time.sleep(10)
	
	return degrees(acos((distance_BA **2 + distance_BC **2 - distance_AC **2)/(2.0 * distance_BA * distance_BC)))

	# https://stackoverflow.com/questions/18583214/calculate-angle-of-triangle-python





def getListOfXYZValues( chosen_lines_of_interest, number_of_atoms ):

	xyz_values = []


	for i in range( 0, len( chosen_lines_of_interest ) ):

		if not isStepLine( chosen_lines_of_interest[i]):

			 if str( chosen_lines_of_interest[i] ).strip() != str( number_of_atoms):

				values_of_line = chosen_lines_of_interest[i].split()

				x = float( values_of_line[1] )
				y = float( values_of_line[2] )
				z = float( values_of_line[3] )

				row_number_of_these_values = int(values_of_line[4])

				xyz_values.append( [x,y,z, row_number_of_these_values] )


	return xyz_values


def getListOfAngles( xyz_values ):



	list_of_angles = []

	i = 0

	while i < len( xyz_values ):

		distance_BA = calculateDistanceBetween3DPoints( xyz_values[i], xyz_values[i+1] )
		distance_BC = calculateDistanceBetween3DPoints( xyz_values[i+1], xyz_values[i+2] )
		distance_AC = calculateDistanceBetween3DPoints( xyz_values[i], xyz_values[i+2] )

		
		angle = []
		angle.append( calculateAngle( distance_BA, distance_BC, distance_AC ) )

		angle_identifier = str( xyz_values[i][3] ) + "." + str( xyz_values[i+1][3] ) + "." + str( xyz_values[i+2][3] )
		angle.append( angle_identifier )

		list_of_angles.append( angle )


		i = i + 3

	
	return list_of_angles



def addAnglesToStepLines( wanted_steps, angles ):

	number_of_steplines = 0

	#wanted_steps_with_angles = []

	next_index_of_angles_to_add = 0

	for i in range( 0, len( wanted_steps ) ):

		if isStepLine( wanted_steps[i] ):
			
			wanted_steps[i] = wanted_steps[i] + " Angle(" + str( angles[next_index_of_angles_to_add][1] ) + ")="+ str( round( angles[next_index_of_angles_to_add][0], 2) )

			next_index_of_angles_to_add = next_index_of_angles_to_add + 1

			number_of_steplines += 1


	return wanted_steps	

	
def addNumberOfAtoms( lines_of_interest, number_of_atoms ):


	lines_with_atom_number = []

	for i in range( 0, len( lines_of_interest ) ):
		
		if str( lines_of_interest[i] ) == "":

			lines_of_interest[i] = "  " + str( number_of_atoms )
			#print str( lines_of_interest[i] )
			#time.sleep( 5 )
			lines_with_atom_number.append( lines_of_interest[i] )
		else:

			lines_with_atom_number.append( lines_of_interest[i] )


	return lines_with_atom_number



def cleanEmptyLines ( lines_of_interest ):

	a = []

	count = 0

	for i in range( 0, len( lines_of_interest ) ):

		if len( lines_of_interest[i].split() ) == 1 :

			a.append(lines_of_interest[i])
	return count



def listToString( lines ):

	final_string = ""

	for i in range( 0, len( lines ) ):

		final_string += str( lines[i] ) + "\n"

		
	return final_string




def inputSetsOfThreeRows():

	# THIS WILL HOLD THE LISTS, EACH CONTAINING 
	# 3 ROW NUMBERS NECESSARY TO CALCULATE AN ANGLE
	sets_of_3_rows = []
	
	# HERE WE STORE THE THREE ROW NUMBERS 
	# THAT WE WANT FOR EACH ANGLE
	number_of_rows = 3
	list_of_row_numbers_we_want = []

	wantToContinue = True

	inputed_number_of_row = "0"
	while ( wantToContinue ):

		for i in range (0, number_of_rows):

			if i == 0:
			
				print "Enter first number of row (Ray1 of Angle)"

			if i == 1:
			
				print "Enter second number of row (Vertex of Angle)"

		
			if i == 2:
			
				print "Enter first number of row (Ray2 of Angle)"
			sys.stdin = open('/dev/tty')
			inputed_number_of_row = raw_input()
		
			list_of_row_numbers_we_want.append( inputed_number_of_row )

		sets_of_3_rows.append( list_of_row_numbers_we_want)

		list_of_row_numbers_we_want = []

		
		
		print "Continue? (Type \"no\" to stop, press Enter to continue)"
		answer = raw_input()
		if answer == "no":
			wantToContinue = False

	
	return sets_of_3_rows
	



os.system("clear")
print "******************************* ANGLE ANALYZER *********************************"


# EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!!
# EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! 
# EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! 
# EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! 
# EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!!  


sets_of_3_rows = [ ['28', '9', '2'], ['11', '6', '3'], ['12', '7', '4'] ]

desired_distance = 245

directory_where_input_files_are = "/home/vitmfs/Desktop/Angle_Analyzer_Input_Files"

chosen_prefix = "desired_steps_"

# EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! 
# EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! 
# EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! 
# EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! 
# EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! EDIT HERE!!! 

parts_of_directory_path = directory_where_input_files_are.split("/")
list_of_input_files = os.listdir( directory_where_input_files_are )
results_folder_path = "Results_" + parts_of_directory_path[len(parts_of_directory_path)-1]



#os.system("cd " + directory_where_input_files_are )
os.system("mkdir -p " + directory_where_input_files_are + "/" + results_folder_path )




##############################################################################

path 			= "" 

#sys.argv[1]
#desired_distance 	= sys.argv[2]

for i in range( 0, len ( list_of_input_files ) ):

	path = list_of_input_files[i] 

	original_lines = []
	original_lines = getLinesFromFile( path )

	number_of_atoms = int( original_lines[0].strip() )

	wanted_steps = []
	wanted_steps = getWantedSteps( original_lines, desired_distance, number_of_atoms )

	string_to_write = getInfoStringToWriteToFile( wanted_steps )

	writesToFile( chosen_prefix, path, string_to_write )





	list_of_row_numbers_we_want 	= [] 
	lines_of_interest 		= []
	angles 				= []



	for i in range( 0, len( sets_of_3_rows ) ):

		list_of_row_numbers_we_want = sets_of_3_rows[i] 



		lines_of_interest = []
		lines_of_interest = getLinesFromFile( chosen_prefix + path )



		chosen_lines_of_interest = getLinesOfAtomsOfInterest( lines_of_interest, list_of_row_numbers_we_want ) 



		xyz_values = getListOfXYZValues( chosen_lines_of_interest, number_of_atoms )



		angles = getListOfAngles( xyz_values ) 


		wanted_steps = addAnglesToStepLines( wanted_steps, angles )

		final_string_to_write = getInfoStringToWriteToFile( wanted_steps )

		writesToFile( chosen_prefix, path, final_string_to_write )

		list_of_row_numbers_we_want 	= [] 
		lines_of_interest 		= []
		angles 				= []



	os.system("mv " + chosen_prefix + path  + " " + directory_where_input_files_are + "/" + results_folder_path )



print "**************************** THANK YOU, HAVE A NICE DAY!  ************************"
os.system("cd .." )









