import sys
import time


def createTestFileText():

    # VARIABLES
    number_of_lines     = 1000
    fill_in_string      = "this is line "
    line_breaker        = "\n"
    all_text_of_file    = ""

    # CREATE DUMMY TEXT FOR TEST FILE
    for i in range( 0, number_of_lines ):

        all_text_of_file += fill_in_string + str( ( i + 1) ) + line_breaker

    # RETURN DUMMY TEXT FOR TEST FILE
    return all_text_of_file


def writesToFile( chosen_prefix, original_name_of_file, string_to_write ):

    # NAME OF OUTPUT FILE
	name_of_output_file = chosen_prefix + str( original_name_of_file )
	
    # CREATES AND WRITES TO FILE
	text_file = open(name_of_output_file, "w")
	text_file.write(string_to_write)
	text_file.close()

def appendToFile( path_to_file, string_to_append ):

    with open( path_to_file, "a") as myfile:

        myfile.write( string_to_append )

def convertsListToString( list ):

    str_to_return = ""

    for str in list:

        str_to_return += str + "\n"
    
    return str_to_return



def getLinesFromFile(path):
    
	with open(path) as f:

		lines = f.read().splitlines()

	return lines


def getLinesToKeep( original_lines, how_many_lines_to_keep_from_start ):

    lines_of_interest = ""

    for i in range ( 0, how_many_lines_to_keep_from_start ):

        lines_of_interest += original_lines[i] + "\n"

    return lines_of_interest


def removeLines( original_lines, number_of_lines_to_remove_from_start ):

    del original_lines[0:number_of_lines_to_remove_from_start]

    shaved_lines = original_lines

    return shaved_lines


def getIndexesForStarAndEnd( lines ):

    line_before_beginning_part  = "MODEL"
    line_after_end_part         = "TER"

    all_start_and_end_indexes = []

    start_and_end_index = []

    lines_length = len( lines )

    for i in range( 0, lines_length ):

        # GET BEGINNING INDEX
        if line_before_beginning_part in lines[i]:

            start_and_end_index.append( i + 1 )

        # GET ENDING INDEX
        if line_after_end_part in lines[i]:

            start_and_end_index.append( i - 1 )

            # AFTER GETTING THE ENDING INDEX, WE ADD IT TO ALL INDEXES
            # AND CLEAN THE TEMP LIST
            all_start_and_end_indexes.append( start_and_end_index )
            start_and_end_index = []

    return all_start_and_end_indexes


def getInfoOfInterestOneFrame( lines_to_process, start_index, last_index ):

    lines_this_frame = []

    start_frame_index = start_index - 5

    last_frame_index_plus_1 = last_index + 3

    for i in range( start_frame_index, last_frame_index_plus_1 ):

        lines_this_frame.append( lines_to_process[i] )

    return lines_this_frame












# EXAMPLE OF USE: python3.7 line_cleaner.py test_3frames.pdb 18231 672

print( "Line Cleaner Started!")

# writesToFile( "", "test_file.txt", createTestFileText() )


path_to_file                = sys.argv[1]
nlines_to_keep_from_start   = int( sys.argv[2] )
nlines_to_delete_after_that = int( sys.argv[3] )

name_of_results_file = "processed_" + path_to_file


lines       = getLinesFromFile( path_to_file )

indexes_for_star_and_end = getIndexesForStarAndEnd( lines )

length_indexes_for_star_and_end = len( indexes_for_star_and_end )


lines_of_interest_this_frame    = []
header_part                     = []
footer_part                     = []
part_of_interest_of_only_tuples = []

for i in range( 0, length_indexes_for_star_and_end ):

    lines_of_interest_this_frame = getInfoOfInterestOneFrame( lines, indexes_for_star_and_end[i][0], indexes_for_star_and_end[i][1] )

    #print( str( lines_of_interest_this_frame[0 + 5] ) ) 
    #print( str( lines_of_interest_this_frame[len(lines_of_interest_this_frame) - 1 - 2] ) ) 

    header_part = lines_of_interest_this_frame[0:5]
    #print( str( header_part ) )
    appendToFile( name_of_results_file, convertsListToString( header_part ) )

    only_tuples = lines_of_interest_this_frame[5:len(lines_of_interest_this_frame)-2]
    #print( str(only_tuples[0]) )
    #print( str(only_tuples[len(only_tuples)-1]) )
    #print( str( len( only_tuples) ) )

    part_of_interest_of_only_tuples = only_tuples[0:nlines_to_keep_from_start]
    #print( str( len( part_of_interest_of_only_tuples ) ) )
    #print( str( part_of_interest_of_only_tuples[0] ) )
    #print( str( part_of_interest_of_only_tuples[len(part_of_interest_of_only_tuples)-1] ) )
    appendToFile( name_of_results_file, convertsListToString( part_of_interest_of_only_tuples ) )


    footer_part = lines_of_interest_this_frame[len(lines_of_interest_this_frame)-2:len(lines_of_interest_this_frame)]
    #print( str(footer_part) )
    appendToFile( name_of_results_file, convertsListToString( footer_part ) )
    



print( "Line Cleaner Ended!")