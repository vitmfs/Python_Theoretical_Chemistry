#!/usr/bin/python

from decimal import *
import csv

# list of energies (strings) that should be in lines of interest
energies = [

		"Coulombic Energy                ",
		"Internuclear Repulsion          ",
		"Electrostatic Energy            ",
		"Landshoff's  Delta (DL) JBP(31) ",
		"First Order Exchange E^(10)_ex  ",
		"First Order Exchange(S^2)       ",
		"FOExch - FOExch(S^2)            ",
		"Delta 4 Correction (D4) JBP(31) ",
		"E_HL = FOEnergy - D4 - DL       ",
		"Total First Order Energy        ",
		"e1(CCSD) K2u term (A)           ",
		"e1(CCSD) K2u term (B)           ",
		"K2F for monomer A (CCSD)        ",
		"K2F for monomer B (CCSD)        ",
		"K11u for monomer A     (CCSD)",
		"K11u for monomer B     (CCSD)",
		"Total e120+e102 exchange (CCSD) ",
		"Total e111 exchange       (CCSD)",
		"e200 exch - ind  B ---> A       ",
		"e200 exch - ind  A ---> B       ",
		"e200 exch - ind (sum)           ",
		"e200 exch - disp                ",
		"e200 Dispersion energy          ",
		"e210 Dispersion Energy          ",
		"e201 Dispersion Energy          ",
		"Total E21 Dispersion            ",
		"Total e211 Dispersion Energy    ",
		"e220 disp Singles               ",
		"e220 disp Doubles               ",
		"e220 disp Quadruples            ",
		"e220 disp Triples               ",
		"Total e220 (S+D+Q)              ",
		"Total e220 (S+D+T+Q)            ",
		"e202 disp Singles               ",
		"e202 disp Doubles               ",
		"e202 disp Quadruples            ",
		"e202 disp Triples               ",
		"Total e202 (S+D+Q)              ",
		"Total e202 (S+D+T+Q)            ",
		"Total e220 induction            ",
		"Total e202 induction            ",
		"Induction of A ---> B Type      ",
		"Induction of B ---> A Type      ",
		"Total e200 Induction Energy - R ",
		"e200 exch - ind  B ---> A       ",
		"e200 exch - ind  A ---> B       ",
		"e200 exch - ind (sum) - Resp    ",
		"e120 pol energy                 ",
		"e102 pol energy                 ",
		"Total e120 + e102 Pol Energy-R  ",
		"Total e130 Pol Energy-R  ",
		"Total e103 Pol Energy-R  ",
		"Total e130 + e103 polarization-R",
		"E^{HF}_{AB}        ",
		"E^{HF}_{A}         ",
		"E^{HF}_{B}         ",
		"E^{HF}_{int}           ",
		"E^{(10)}_{elst}       ",
		"E^{(10)}_{exch}     ",
		"E^{(10)}_{exch}{S^2}",
		"E^{(10)}_{exch}-S^2 ",
		"E^{(20)}_{ind,resp} ",
		"E^{(20)}_{ex-ind}  ",
		"E^{(20)}_{ex-ind,r}  ",
		"SAPT SCF_{resp} ^b  ",
		"\delta^{HF}_{int,r}   ",
		"E^{(12)}_{elst,resp}   ",
		"E^{(13)}_{elst,resp}   ",
		"\eps^{(1)}_{elst,r}(k) ",
		"\eps^{(1)}_{exch}(CCSD)",
		"^tE^{(22)}_{ind}       ",
		"^tE^{(22)}_{ex-ind}*   ",
		"E^{(20)}_{disp}     ",
		"E^{(21)}_{disp}    ",
		"E^{(22)}_{disp}      ",
		"\eps^{(2)}_{disp}(k)   ",
		"E^{(2)}_{disp}(k)   ",
		"E^{(20)}_{exch-disp}",
		"SAPT_{corr}         ",
		"SAPT_{corr,resp}    ",
		"SCF+SAPT_{corr}     ",
		"SCF+SAPT_{corr,resp}"

]

# function that
# reads file into list of lines
def getValuesFromFile(path):

	with open(path) as f:
		lines = f.read().splitlines();

	#create a list for every "type" of energy
	energies_type_1 = []
	energies_type_2 = []
	energies_type_3 = []

	for line in lines:
		for energy in energies:
			if energy in line:
				edited_line = line.strip()
				# searc criteria for "type 1 energies"
				if ":" in line and ("D" in line or "E" in line) and "." in line and "0" in line:
					
					wordsOfLine = line.split(":")
					lineNameOfEnergy = wordsOfLine[0]
					lineValueOfEnergy = wordsOfLine[1]
					lineValueOfEnergy = lineValueOfEnergy.split()
					lineValueOfEnergy = lineValueOfEnergy[0]
					editedLine = lineNameOfEnergy + ":" + lineValueOfEnergy
					energies_type_1.append(editedLine)
					#print edited_line
					break
				elif "hartrees" in line:
					edited_line = line[:53]
					edited_line = edited_line.strip()
					energies_type_2.append(edited_line)
					#print edited_line
					break
				else:
					edited_line = line[:43]
					edited_line = edited_line.strip()
					if "+ E^{(20)}_{ind,resp} + E^{(" not in edited_line:
						energies_type_3.append(edited_line)
						print edited_line

			

	print len(energies_type_1)
	print len(energies_type_2)
	print len(energies_type_3)

	
	for line_energy_1 in energies_type_1:
		print #line_energy_1

	print ""

	for line_energy_2 in energies_type_2:
		print #line_energy_2

	print ""

	#energies_type_3.pop()
	for line_energy_3 in energies_type_3:
		print #line_energy_3

	
	names_of_energies = []
	str_val_of_energies = []
	dbl_val_of_energies = []

	for ed_line1 in energies_type_1:

		temp_list = ed_line1.split(":")
		temp_name = temp_list[0]
	
		temp_value = temp_list[1]
		if "E" in temp_value:
			dbl_value = float(temp_value)
			#print dbl_value
		if "D" in temp_value:
			temp_value = temp_value.replace("D", "E")
			dbl_value = float(temp_value)
			#print dbl_value

		names_of_energies.append(temp_name)
		str_val_of_energies.append(temp_value)
		dbl_val_of_energies.append(dbl_value)


	for ed_line2 in energies_type_2:
		temp_list2 = ed_line2.split()
		temp_name2 = temp_list2[0]
		temp_value2 = temp_list2[1]
		dbl_value2 = Decimal(temp_value2)

		names_of_energies.append(temp_name2)
		str_val_of_energies.append(temp_value2)
		dbl_val_of_energies.append(dbl_value2)

		#print temp_name2 + " " + temp_value2 + " " + str(dbl_value2)
		
	for ed_line3 in energies_type_3:
		if "SAPT SCF_{resp} ^b" in ed_line3:
			list_line3 = ed_line3.split()

			ed_line3 = list_line3[0] + list_line3[1] + list_line3[2] + " " + list_line3[3]
			#print ed_line3
		#print ed_line3
		
		temp_list3 = ed_line3.split()
		temp_name3 = temp_list3[0]
		temp_value3 = temp_list3[1]
		#print temp_name3 + " " + temp_value3
		
		dbl_value3 = Decimal(temp_value3)

		names_of_energies.append(temp_name3)
		str_val_of_energies.append(temp_value3)
		dbl_val_of_energies.append(dbl_value3)

		#print temp_name3 + "   " + temp_value3 + " " + str(dbl_value3)


	file_values = [names_of_energies, str_val_of_energies, dbl_val_of_energies]
	return file_values


valuesFromFile1 = getValuesFromFile("HF2.out.gfortran")

valuesFromFile2 = getValuesFromFile("HF2.out.sunf90")

strToWrite = ""

print len(valuesFromFile1)


for i in range(0, len(valuesFromFile1[0])):
	strToWrite += valuesFromFile1[0][i] + ";" + valuesFromFile1[1][i] + ";" + valuesFromFile2[1][i] + ";" + str(valuesFromFile1[2][i]) +";" + str(valuesFromFile2[2][i]) + ";" + str(valuesFromFile1[2][i] - valuesFromFile2[2][i]) + "\n"

print strToWrite

text_file = open("HF2.out.gfortran.sunf90.csv", "w")
text_file.write(strToWrite)
text_file.close()

