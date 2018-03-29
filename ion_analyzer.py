#!/usr/bin/python

import os
import sys
import numpy
import time

os.system("clear")

# https://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/python 
# python ion_analyzer.py npt_30dca.gro 1 1 0.36
# python ion_analyzer.py npt_30dca.gro 2 3 3.0


##### FUNCTION THAT GETS ATOMS OF INTEREST FOR STUDY #######################################################
def fillWantedAtomsList( list_of_atoms, number_of_times, type_of_ion  ):

	for i in range (0, number_of_times):

		inputed_atom_of_interest = raw_input("     Enter atom of interest for " + \
		(type_of_ion if type_of_ion == "cation" else type_of_ion + " ")  + ":   ")
		inputed_atom_of_interest = inputed_atom_of_interest.upper()
		list_of_atoms.append(inputed_atom_of_interest)
		#print str(list_of_atoms)

	return list_of_atoms
	
	# References:
	# https://stackoverflow.com/questions/394809/does-python-have-a-ternary-conditional-operator
############################################################################################################


##### FUNCTION THAT READS LINES FROM GROMACS FILE  #########################################################
def getLinesFromFile(path):

	with open(path) as f:
		lines = f.read().splitlines();

	return lines
############################################################################################################


##### FUNCTION THAT REMOVES NON DATA LINES AND TRIMS WHITE SPACE ###########################################
def getCleanLinesFromFile( lines_from_file ):

	lines_of_interest = lines_from_file
	
	lines_of_interest.pop(0)
	lines_of_interest.pop(0)
	lines_of_interest.pop( len(lines_of_interest) - 1)

	for i in range ( 0, (len(lines_of_interest) - 1) ):

		lines_of_interest[i] = lines_of_interest[i].strip()
	
	return lines_of_interest
############################################################################################################


##### FUNCTION THAT REMOVES WHITESPACE #####################################################################
def cleanInformationFromLines(lines):

	for line in lines:

		line = line.strip()

	return lines
############################################################################################################


##### FUNCTION THAT REMOVES SOLVENT LINES ##################################################################
def removeSolventLines(trimmed_lines):

	lines_without_solvent = trimmed_lines

	line_with_solvent_name = lines_without_solvent[ len(lines_without_solvent) - 1 ]

	word_with_solvent_name = line_with_solvent_name.split()[0]

	solvent_identidier = "SOL"

	#showMeTheValue( word_with_solvent_name )

	while ( ( solvent_identidier in lines_without_solvent[ len(lines_of_interest) -1 ] ) ):
	
		lines_without_solvent.pop()

	#showMeTheValue( lines_without_solvent )

	return lines_without_solvent
############################################################################################################


##### FUNCTION THAT TRANFORMS LINES INTO MATRIX OF VALUES OF INTEREST ######################################
def createAMatrixOfValues(pre_prepared_lines):

	number_of_rows = len(pre_prepared_lines)
	number_of_columns = len( pre_prepared_lines[0].split() )

	#showMeTheValue(number_of_rows)
	#showMeTheValue(number_of_columns)


	my_matrix = [""] * number_of_rows

	for i in range(number_of_rows):

	    my_matrix[i] = [""] * number_of_columns


	for n in range(number_of_rows):

		current_line = pre_prepared_lines[n]
		
		current_words = current_line.split()

		for x in range(number_of_columns):

			my_matrix[n][x] = current_words[x]

	#showMeTheValue(my_matrix)

	return my_matrix

	# References:
	# https://www.programiz.com/python-programming/matrix
############################################################################################################


##### FUNCTION THAT CALCULATES DISTANCE BETWEEN TWO POINTS #################################################
def calculateDistanceTwoPoints(xa, ya, za, xb, yb, zb):

	a_point = numpy.array((xa ,ya, za))
	b_point = numpy.array((xb, yb, zb))

	distance = numpy.linalg.norm( a_point - b_point )

	return distance

	# References:
	# https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
############################################################################################################


##### FUNCTION THAT SHOWS VARIABLE CONTENT SIMILAR TO PRINT ################################################
def showMeTheValue( variable_to_show ):

	print str(variable_to_show)
############################################################################################################


##### FUNCTION THAT GETS ONLY TUPLES OF INTEREST FROM MATRIX OF VALUES #####################################
def getAtomsToCompare(matrix_of_values):

	atoms_to_compare = []

	for each_tuple in matrix_of_values:

		if each_tuple[1] in cation_atoms_of_interest or each_tuple[1] in anion_atoms_of_interest:

			atoms_to_compare.append( each_tuple )

	return atoms_to_compare
############################################################################################################


##### FUNCTION THAT GETS THE NAMES OF IONS #################################################################

def getNamesOfIons( original_matrix_of_strings ):

	list_of_ion_names = []

	for each_tuple in original_matrix_of_strings:

		if each_tuple[0] not in list_of_ion_names:

			list_of_ion_names.append( each_tuple[0] )

	return list_of_ion_names

############################################################################################################


##### CLASS ATOM ###########################################################################################
class Atom:

	def __init__(self, name_of_ion, name_of_atom, id_of_atom, x_position, y_position, z_position):

		self.name_of_ion = name_of_ion
		self.name_of_atom = name_of_atom
		self.id_of_atom = id_of_atom
		self.x_position = x_position
		self.y_position = y_position
		self.z_position = z_position

	def get_name_of_ion(self):

		return self.name_of_ion

	def get_name_of_atom(self):

		return self.name_of_atom

	def get_id_of_atom(self):

		return self.id_of_atom


	def get_x_position(self):

		return float( self.x_position )

	def get_y_position(self):

		return float( self.y_position )

	def get_z_position(self):

		return float( self.z_position )

	def to_string(self):

		return 	self.name_of_ion + " " + self.name_of_atom + " " + self.id_of_atom + " " + \
			self.x_position + " " + self.y_position + " " + self.z_position

############################################################################################################

##### CLASS ION ############################################################################################

class Ion:

	def __init__(self, name_of_ion, list_of_selected_atoms):

		self.name_of_ion = name_of_ion

		self.list_of_atoms_of_ion = list_of_selected_atoms

	def get_name_of_ion(self):

		return self.name_of_ion

	def get_list_of_atoms_of_ion(self):

		return self.list_of_atoms_of_ion

############################################################################################################

##### CLASS INTERACTION ####################################################################################

class Interaction:

	def __init__(self, atom1, atom2, distance):

		self.atom1 = atom1
		self.atom2 = atom2
		self.distance = distance
		self.is_checked = False

	def get_atom1(self):

		return self.atom1

	def get_atom2(self):

		return self.atom2

	def get_distance(self):

		return self.distance

	def get_is_checked(self):

		return self.is_checked

	def to_string(self):

		return 	self.atom1.get_name_of_ion() + " " + self.atom2.get_name_of_ion() + " " + \
			str( self.distance ) + " " + str( self.is_checked )

############################################################################################################

##### FUNCTION THAT GETS THE LIST OF ATOMS FOR THAT ION ####################################################

def getListOfAtomsForIon( ion_nameT, list_of_atom_objsT ):

	list_of_ats_for_ion = []

	for each_at_obj in list_of_atom_objsT:

		if ion_nameT == each_at_obj.get_name_of_ion():

			list_of_ats_for_ion.append( each_at_obj ) 

	return list_of_ats_for_ion

############################################################################################################

##### FUNCTION THAT GETS THE LIST OF ATOM OBJECTS OF INTEREST ##############################################

def getListOfAtomsOfInterest(atoms_to_compareT):

	#print "entrei no getListOfAtomsOfInterest(atoms_to_compareT)"
	#time.sleep(5)

	list_of_atom_objects_of_interest = []

	#print "antes do ciclo)"
	#time.sleep(5)


	for each_tuple in atoms_to_compareT:

		#print str( each_tuple )

		newly_created_atom = Atom(each_tuple[0], each_tuple[1], each_tuple[2], each_tuple[3], each_tuple[4], each_tuple[5] )
		
		#print each_tuple[0]
		#print each_tuple[1]
		#print each_tuple[2]
		#print each_tuple[3]
		#print each_tuple[4]
		#print each_tuple[5]
		list_of_atom_objects_of_interest.append( newly_created_atom )

	#list_of_atom_objects_of_interest.append( newly_created_atom )

	return list_of_atom_objects_of_interest

############################################################################################################

##### FUNCTION THAT CRATES ALL IONS ########################################################################

def createAllIons( names_of_ionsT, list_of_atom_objects_of_interestT ):

	list_of_ion_objs = []

	for each_name_of_ion in names_of_ionsT:
		
		temp_list_of_atoms_for_ion = getListOfAtomsForIon( each_name_of_ion, list_of_atom_objects_of_interestT )

		temp_new_ion = Ion( each_name_of_ion, temp_list_of_atoms_for_ion)

		list_of_ion_objs.append( temp_new_ion )

	return list_of_ion_objs

############################################################################################################

		
##### FUNCTION THAT REMOVES DIGITS FROM STRING##############################################################
def removeDigitsFromString(string_with_numbers):

	string_no_digits = ""
	# Iterate through the string, adding non-numbers to the no_digits list
	for i in string_with_numbers:
	    if not i.isdigit():
		#string_no_digits.append(i)
		string_no_digits += i

	return string_no_digits
############################################################################################################


##### FUNCTION THAT CHECKS IF TWO INTERACTIONS ARE THE SAME ################################################

def sameInteraction( interaction_01, interaction_02):


	if 	( interaction_01.get_atom1() == interaction_02.get_atom1() and interaction_01.get_atom2() == interaction_02.get_atom2() ) or \
		( interaction_01.get_atom1() == interaction_02.get_atom2() and interaction_01.get_atom2() == interaction_02.get_atom1() ) :


		#print str( interaction_01.get_distance() ) + " " + str( interaction_02.get_distance() )
		#time.sleep(5)

		if str( interaction_01.get_distance() ) == str( interaction_02.get_distance() ):
			
			return True	
		else:

			return False

	else:

		return False
############################################################################################################

##### FUNCTION THAT RETURNS THE LIST OF INTERACTIONS GIVEN A LIST OF ATOM OBJECTS OF INTEREST ##############

def getListOfInteractions( list_of_atom_objects_of_interest ):

	list_of_interactions = []

	temp_atom_one = None

	for each_atom in list_of_atom_objects_of_interest:

		# EVERY ATOM WILL HAVE THE CHANCE TO BE THE FIRST
		temp_atom_one = each_atom

		xa = float( temp_atom_one.get_x_position() )
		ya = float( temp_atom_one.get_y_position() )
		za = float( temp_atom_one.get_z_position() )

		for another_atom in list_of_atom_objects_of_interest:

			if 	temp_atom_one != another_atom and \
				removeDigitsFromString( temp_atom_one.get_name_of_ion() ) != removeDigitsFromString( another_atom.get_name_of_ion() ):

				xb = float( another_atom.get_x_position() )
				yb = float( another_atom.get_y_position() )
				zb = float( another_atom.get_z_position() )

				# CALCULATE THE DISTANCE BETWEEN THE FIRST TWO ATOMS
				distance = float( calculateDistanceTwoPoints( xa, ya, za, xb, yb, zb ) )

				if ( distance < max_distance_between_atoms ):

					# print str( distance ) 
					new_interaction = Interaction( temp_atom_one, another_atom, distance)
					list_of_interactions.append( new_interaction )

	print str( len(list_of_interactions) )

	for each in list_of_interactions:

		print each.get_atom1().get_name_of_ion() + " " +  each.get_atom2().get_name_of_ion() + " " + str( each.get_distance() )

	
	return list_of_interactions

############################################################################################################

###### FUNCTION THAT REMOVES DUPLICATES FRM LIST OF INTERACTIONS ###########################################

def removeDuplicatesFromListOfInteractions( list_of_interactions ):

	has_duplicates = True

	while has_duplicates == True:

		has_duplicates = False

		interaction_to_compare = list_of_interactions[len(list_of_interactions) - 1]

		for i in range (0, len( list_of_interactions ) - 1 ):

			if sameInteraction( list_of_interactions[i], interaction_to_compare):
				
				has_duplicates = True
			
		if has_duplicates == True:

			list_of_interactions.pop()
			#print str( len(list_of_interactions) )
			

	#print str( len(list_of_interactions) )

	#for each in list_of_interactions:

		#print each.get_atom1().get_name_of_ion() + " " +  each.get_atom2().get_name_of_ion() + " " + str( each.get_distance() )

	return list_of_interactions

############################################################################################################

#####FUNCTION OF THAT GETS CHECKED INTERACTIONS OF THIS RUN ################################################

def getCheckedInteractionsInThisRun( list_of_interactions ):

	# WE CHOOSE THE FIRST INTERACTION OF THE LIST
	first_interaction = list_of_interactions[0]

	# WE GET A REFERENCE FOR THE FIRST ATOM OF THE INTERACTION
	first_atom_of_first_interaction = first_interaction.get_atom1()

	# WE GET A REFERENCE FOR THE SECOND ATOM OF THE INTERACTION
	second_atom_of_first_interaction = first_interaction.get_atom2()

	# WE INITIALIZE A LIST OF CHECKED INTERACTIONS
	list_of_checked_interactions = []

	# WE ADD THE FIRST INTERACTION TO THE LIST
	list_of_checked_interactions.append( first_interaction )

	# WE INITIALIZE A LIST OF NEW INTERACTIONS
	list_of_news = []

	# WE ADD THE FIRST INTERACTION TO THE LIST
	#list_of_news.append( first_interaction )


	for each_int in list_of_interactions:

		if not 	sameInteraction( first_interaction, each_int) and \
			each_int.get_atom1().get_name_of_ion() == first_interaction.get_atom2().get_name_of_ion() and \
			each_int not in list_of_checked_interactions:

			# IF THEY ARE NOT THE SAME INTERACTION, WITH THE SAME ATOMS AND DISTANCE AND
			# IF THE FIRST ATOM OF THE NEXT INTERACTION IS THE SAME AS THE SECOND ATOM IN THIS INTERACTION
			# IF THIS INTERACTION IS NOT ON THE LIST OF CHECKED INTERACTIONS

			list_of_checked_interactions.append( each_int )

			list_of_news.append( each_int )

			#print each_int.get_atom1().get_name_of_ion() + " " + each_int.get_atom2().get_name_of_ion() + " " + str( each_int.get_distance() )

	print "\n"

	while len( list_of_news ) > 0:
		# FOR EACH NEW INTERACTION TO VERIFY
		for each_new_int in list_of_news:
			# CHECK ALL OTHER INTERACTIONS
			for each_int in list_of_interactions:

				if not 	sameInteraction( each_new_int, each_int) and \
					each_int.get_atom1().get_name_of_ion() == each_new_int.get_atom2().get_name_of_ion() and \
					each_int not in list_of_checked_interactions:

					# IF THEY ARE NOT THE SAME INTERACTION, WITH THE SAME ATOMS AND DISTANCE AND
					# IF THE FIRST ATOM OF THE NEXT INTERACTION IS THE SAME AS THE SECOND ATOM IN THIS INTERACTION
					# IF THIS INTERACTION IS NOT ON THE LIST OF CHECKED INTERACTIONS

					list_of_checked_interactions.append( each_int )

					list_of_news.append( each_int )

		list_of_news = []

					#print each_int.get_atom1().get_name_of_ion() + " " + each_int.get_atom2().get_name_of_ion() + " " + str( each_int.get_distance() )

		#print str( len(list_of_checked_interactions) )

	return list_of_checked_interactions

############################################################################################################

##### FUNCTION THAT REMOVES IONS FROMM ORIGINAL IONS LIST ##################################################

def removeIonsFromIonsList( list_of_ion_objects, list_of_checked_interactions ):
	# WE DECLARE A LIST OF IONS TO REMOVE
	list_of_ions_to_remove = []

	# WE DECLARE A LIST OF NAMES OF IONS TO REMOVE
	list_of_ion_names_to_remove =  []

	# REMOVE THE IONS THAT PARTICIPATE IN ALREADY CHECKED INTERACTIONS!!!
	# FOR EACH INTERACTION IN CHECKED INTERACTIONS
	for ea in list_of_checked_interactions:

		#print str( ea.__class__)

		for i in range (0, len( list_of_ion_objects ) ):
		
			#print str( list_of_ion_objects[i].__class__)

			at1 = ea.get_atom1()
			at2 = ea.get_atom2()
			temp_atoms_list = list_of_ion_objects[i].get_list_of_atoms_of_ion() 
			
			# IF ANY OF THE ATOMS OF THE CHECKED INTERACTION BELONGS TO THE LIST
			# OF ATOMS OF THE ION
			if ( (at1 in temp_atoms_list) or (at2 in temp_atoms_list) ):

				# ADD THAT ION TO THE LIST OF IONS TO BE REMOVED
				list_of_ions_to_remove.append( list_of_ion_objects[i] )

				# NAME OF THE ION OF THE FIRST ATOM
				name_of_ion_01 = at1.get_name_of_ion()

				# NAME OF THE ION OF THE SECOND ATOM
				name_of_ion_02 = at2.get_name_of_ion()
				
				if name_of_ion_01 not in list_of_ion_names_to_remove:

					list_of_ion_names_to_remove.append( name_of_ion_01 )

				if name_of_ion_02 not in list_of_ion_names_to_remove:

					list_of_ion_names_to_remove.append( name_of_ion_02 )



	#print str( len( list_of_ions_to_remove )) 
	print str( list_of_ion_names_to_remove )

	print "Length of Ion list before: " + str( len( list_of_ion_objects ) ) + "\n"
	#print str( len( list_of_atom_objects_of_interest ) ) + "\n"
	
	index_of_ion_to_delete = -1
	#index_of_atom_to_delete = -1

	for each_ion_name_to_remove in list_of_ion_names_to_remove:

		for i in range (0, len( list_of_ion_objects ) ):

			if each_ion_name_to_remove == list_of_ion_objects[i].get_name_of_ion():

				print each_ion_name_to_remove
				index_of_ion_to_delete = i
				time.sleep(3)

				#for j in range (0, len( list_of_atom_objects_of_interest ) ):

					#for k in range (0, len( list_of_ion_objects[i].get_list_of_atoms_of_ion() ) ):

						#if  list_of_atom_objects_of_interest[j] == list_of_ion_objects[i].get_list_of_atoms_of_ion()[k]:
						
							#index_of_atom_to_delete = j

							#print list_of_ion_objects[i].get_list_of_atoms_of_ion()[k].to_string()
							#time.sleep(2)

				#del list_of_atom_objects_of_interest[j]

		del list_of_ion_objects[index_of_ion_to_delete]

		
		
	print "Length of Ion list after: " + str( len( list_of_ion_objects ) ) + "\n"
	#print str( len( list_of_atom_objects_of_interest ) ) + "\n"

	len_of_all = 0

	for each_ion_object in list_of_ion_objects:

		for each_atom in each_ion_object.get_list_of_atoms_of_ion():
	
			len_of_all = len_of_all + 1
	
	print str( len_of_all )
	print str( len( list_of_atom_objects_of_interest ) )

	return list_of_ion_objects



############################################################################################################

def removesInteractionsFromInteractionsList( list_of_checked_interactions, list_of_interactions ):

	remove_index = -1

	for i in range (0, len( list_of_checked_interactions ) ):

		for j in range (0, len( list_of_interactions ) ):

			if list_of_checked_interactions[i] == list_of_interactions[j]:

				remove_index = j

		if remove_index != -1:

			del list_of_interactions[remove_index]

		remove_index = -1

	return list_of_interactions


###### FUNCTION THAT CHECKS IF THERE IS ANY UNCHECKED INTERACTIONS LEFT ####################################

def hasUncheckedInteractions( list_of_interactions ):

	has_unchecked_inters = False

	for each_one_inter in list_of_interactions:

		if each_one_inter.get_is_checked() == False:

			has_unchecked_inters = True

	return has_unchecked_inters


############################################################################################################



#### FUNCTION THAT FINDS GROUPS OF INTERACTIONS ############################################################

def findGroupsOfInteractions( list_of_interactions ): 

	list_of_results = []

	number_of_interactions_in_this_run = 0
	
	number_of_ions_involved = 0

	str_with_interactions_in_this_run = ""

	list_of_ions_in_this_run = []

	list_of_ions_itr_no_numbers = []

	

	first_interaction_in_this_run = None

	list_of_checked_interactions = []

	list_of_new_interactions = []

	# LETS SEARCH FOR THE FIRST UNCHECKED INTERACTION
	i = 0
	lenght_of_list = len ( list_of_interactions )

	while ( i < lenght_of_list  and first_interaction_in_this_run == None): #

		#showMeTheValue( "i = " + str( i ) )

		if list_of_interactions[i].get_is_checked() == False and list_of_interactions[i] != None:

			#showMeTheValue("Found first unchecked!");

			first_interaction_in_this_run = list_of_interactions[i]

			list_of_interactions[i].is_checked = True

			list_of_checked_interactions.append( first_interaction_in_this_run )

			list_of_new_interactions.append( first_interaction_in_this_run )

			# WE ALSO CHECK THE "CLONE" INTERACTION
			for j in range (0, len( list_of_interactions ) ):

				if sameInteraction( list_of_interactions[j], first_interaction_in_this_run):

					list_of_interactions[j].is_checked = True

				
		#first_interaction_in_this_run = None
		i = i + 1

	######################################

	# WE NOW HAVE THE STARTING POINT INTERACTION

	#run = 1

	# THIS LIST WILL KEEP THE NAMES OF IONS TO SEARCH
	name_of_specific_ions_to_search = []

	# FIRST WE SAVE THE NAME OF THE SECOND ION OF THE SECOND ATOM IN THE FIRST INTERACTION
	if first_interaction_in_this_run.get_atom2().get_name_of_ion() not in name_of_specific_ions_to_search:
		name_of_specific_ions_to_search.append( first_interaction_in_this_run.get_atom2().get_name_of_ion() )

	# WHILE NEW INTERACTIONS ARE FOUND
	while list_of_new_interactions:

		# THE PREVIOUS NEW INTERACTIONS DON'T MATTER SO WE RESET IT
		list_of_new_interactions = []

		#showMeTheValue( first_interaction_in_this_run.get_atom1().get_name_of_ion() )
		#showMeTheValue( str( name_of_specific_ions_to_search ) )
		#time.sleep( 1 ) 


		for each_int in list_of_interactions:

			if 	each_int.get_is_checked() == False and \
				each_int.get_atom1().get_name_of_ion() in name_of_specific_ions_to_search:

				each_int.is_checked = True

				# WE ALSO CHECK THE "CLONE" INTERACTION
				for j in range (0, len( list_of_interactions ) ):

					if sameInteraction( list_of_interactions[j], each_int):
				
						#showMeTheValue("Found clone unchecked!");

						list_of_interactions[j].is_checked = True


				list_of_checked_interactions.append( each_int )

				list_of_new_interactions.append( each_int )

				if each_int.get_atom2().get_name_of_ion() not in name_of_specific_ions_to_search:
			
					name_of_specific_ions_to_search.append( each_int.get_atom2().get_name_of_ion() )
			

		#showMeTheValue( str( len( list_of_new_interactions ) ) )
		#showMeTheValue( str( len( list_of_checked_interactions ) ) )

		first_interaction_in_this_run == None

	#########################
	list_of_checked_interactions = removeDuplicatesFromListOfInteractions( list_of_checked_interactions )
	print "\n"
	for each in list_of_checked_interactions:

		#print each.to_string()

		number_of_interactions_in_this_run = number_of_interactions_in_this_run + 1

		str_with_interactions_in_this_run += each.to_string() + "\n"

		temp_name_of_ion_1 = each.get_atom1().get_name_of_ion()
		temp_name_of_ion_2 = each.get_atom2().get_name_of_ion()

		if temp_name_of_ion_1 not in list_of_ions_in_this_run:

			list_of_ions_in_this_run.append( temp_name_of_ion_1 )

		if temp_name_of_ion_2 not in list_of_ions_in_this_run:

			list_of_ions_in_this_run.append( temp_name_of_ion_2 )

	print "\n"
	##########################

			
	#showMeTheValue( "end of findGroupsOfInteractions" )

	list_of_results.append( list_of_interactions )
	list_of_results.append( number_of_interactions_in_this_run )
	list_of_results.append( str_with_interactions_in_this_run )
	list_of_results.append( list_of_ions_in_this_run )

	for i in range (0, len( list_of_ions_in_this_run ) ):

		list_of_ions_itr_no_numbers.append( removeDigitsFromString( list_of_ions_in_this_run[i] ) )

	n_of_cations = 0
	n_of_anions = 0

	for each_ion in list_of_ions_itr_no_numbers:

		if each_ion == list_of_ions_itr_no_numbers[0]:

			n_of_cations += 1

		if each_ion == list_of_ions_itr_no_numbers[1]:

			n_of_anions += 1

	difference_between_anions = ""

	if n_of_cations > n_of_anions:

		difference_between_anions = str( ( n_of_cations - n_of_anions ) ) + "+"

	if n_of_anions > n_of_cations:

		difference_between_anions = str( ( n_of_anions - n_of_cations ) ) + "-"
		

	list_of_ions_itr_no_numbers = 	"[" + str( n_of_cations ) + str( list_of_ions_itr_no_numbers[0] ) + "+:" + \
					str( n_of_anions ) + str( list_of_ions_itr_no_numbers[1] ) + "-]" + difference_between_anions


	list_of_results.append( list_of_ions_itr_no_numbers )

	return list_of_results

############################################################################################################

###### FUNCTION THAT WRITES TO A RESULT FILE ###############################################################

def writesToFileWithTheResultsOf( str_original_data_file, string_to_write ):

	name_of_output_file = "results_" + str( str_original_data_file )
	
	text_file = open(name_of_output_file, "w")
	text_file.write(string_to_write)
	text_file.close()


############################################################################################################


	

##### MAIN PROGRAM #########################################################################################
############################################################################################################

print "\n################## Welcome to Cation-Anion Analyzer Program!####################"


#print "\nPlease insert (separated by spaces):\n - path to file\n - number of atoms you want analyzed in cation\n - number of atoms you want in analyze in anion"

try:

	print ""
	
	path = sys.argv[1]
	print "           The path to gromacs file is:   " + path
	
	n_atoms_for_cation = sys.argv[2]
	print "     The number of atoms for cation is:   " + n_atoms_for_cation

	n_atoms_for_anion = sys.argv[3]
	print "      The number of atoms for anion is:   " + n_atoms_for_anion

	max_distance_between_atoms = float( sys.argv[4] )
	print " The maximum distance between atoms is:   " + str(max_distance_between_atoms)

	cation_identifier = ""
	anion_identifier = ""

	# MATRIX OF STRINGS WITH THE NAMES OF CATION ATOMS OF INTEREST
	cation_atoms_of_interest = []

	# MATRIX OF STRINGS WITH THE NAMES OF ANION ATOMS OF INTEREST
	anion_atoms_of_interest = []

	# ASK THE USER TO INPUT NAMES OF CATIONS OF INTEREST AND STORE THEM
	cation_atoms_of_interest = fillWantedAtomsList( cation_atoms_of_interest, int(n_atoms_for_cation), "cation" )
	#showMeTheValue( str(cation_atoms_of_interest) )

	# ASK THE USER TO INPUT NAMES OF ANIONS OF INTEREST AND STORE THEM
	anion_atoms_of_interest = fillWantedAtomsList( anion_atoms_of_interest, int(n_atoms_for_anion), "anion" )
	#showMeTheValue( str(anion_atoms_of_interest) )
	
	print "\n			Thinking...\n"

	lines_read_from_gro = getLinesFromFile(path)

	lines_of_interest = getCleanLinesFromFile( lines_read_from_gro )

	lines_of_interest = removeSolventLines(lines_of_interest)

	matrixOfStrings = createAMatrixOfValues(lines_of_interest)

	atoms_to_compare = getAtomsToCompare( matrixOfStrings ) 

	list_of_atom_objects_of_interest = getListOfAtomsOfInterest( atoms_to_compare )

	names_of_ions = getNamesOfIons( matrixOfStrings )

	list_of_ion_objects = []
	list_of_ion_objects = createAllIons( names_of_ions, list_of_atom_objects_of_interest )

	list_of_interactions = []
	list_of_interactions = getListOfInteractions( list_of_atom_objects_of_interest )

	

	counters = []

	for i in range (0, 1000):

		counters.append( 0 )

	list_of_numbers_of_ion_clusters	= []

	for i in range (0, 1000):

		list_of_numbers_of_ion_clusters.append( 0 )
	
	str_for_final_results = ""

	# WHILE LIST STILL HAS UNCHECKED INTERACTIONS
	while hasUncheckedInteractions( list_of_interactions ):

		list_of_results_for_this_run = findGroupsOfInteractions( list_of_interactions )

		list_of_interactions = list_of_results_for_this_run[0]

		temp_number_of_interactions = list_of_results_for_this_run[1]

		temp_string_of_interactions = list_of_results_for_this_run[2]

		temp_list_of_ions = list_of_results_for_this_run[3]

		list_of_numbers_of_ion_clusters[ len( temp_list_of_ions ) ] = list_of_numbers_of_ion_clusters[ len( temp_list_of_ions ) ] + 1

		temp_list_of_ions_no_numbers = list_of_results_for_this_run[4]

		#print str( temp_list_of_ions )

		counters[temp_number_of_interactions] += 1
		

		#print str( temp_number_of_interactions ) 
		#print temp_string_of_interactions
		#print str( temp_list_of_ions )
		#print str( len( temp_list_of_ions ) )

		str_for_final_results +=	"################################################################################" + "\n\n" + \
						"n_ions: " + str( len( temp_list_of_ions ) ) + " \n" + \
						str( temp_list_of_ions ) + "\n" + \
						str( temp_list_of_ions_no_numbers ) + "\n\n" + \
						"n_interactions: " + str( temp_number_of_interactions ) + "\n\n" + \
						str( temp_string_of_interactions ) + "\n" + \
						"################################################################################" + "\n"

	
	#print str_for_final_results

	#print str( counters )

	#print str( len( list_of_interactions) )


	str_with_counts = "\n"

	for i in range(0, len( counters ) ):

		if counters[i] != 0:

			str_with_counts += str( i ) + " interactions :	  " + str( counters[i] ) + "\n"


	str_with_counts += "\n"

	print str_for_final_results
	print str_with_counts

	str_with_n_ion_cluster_counts = ""

	for i in range(0, len( list_of_numbers_of_ion_clusters ) ):

		if list_of_numbers_of_ion_clusters[i] != 0:

			str_with_n_ion_cluster_counts += "clusters of " + str( i ) + " ions: 	  " + str( list_of_numbers_of_ion_clusters[i] ) + "\n"

	print str_with_n_ion_cluster_counts

	writesToFileWithTheResultsOf( sys.argv[1], str_with_n_ion_cluster_counts + str_with_counts + str_for_final_results )


	#print str( list_of_numbers_of_ion_clusters )
	

	


except IndexError:

	print "\nPlease insert (separated by spaces):\n - path to file\n - number of atoms you want analyzed in cation\n - number of atoms you want in analyze in anion"
	print "\nExample of use: \n"
	print "python name_of_script.py path_of_file_to_analyse.gro number_of_cations number_of_anions minimum_distance\n"
	print "Please try again!\n"

	sys.exit()


print "\n########################### Thank you, have a nice day! ########################\n"
############################################################################################################
############################################################################################################

