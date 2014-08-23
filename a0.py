"""Helper function to determine the gpa in respect of the score"""def get_gpa(score):
	#Convert the type into integer
	score = int(score)
	if score >= 85:
		return 4.0
	elif score >= 80:
		return 3.7
	elif score >= 77:
		return 3.3
	elif score >= 73:
		return 3.0
	elif score >= 70:
		return 2.7
	elif score >= 67:
		return 2.3
	elif score >= 63:
		return 2.0
	elif score >= 60:
		return 1.7
	elif score >= 57:
		return 1.3
	elif score >= 53:
		return 1.0
	elif score >= 50:
		return 0.7
	else:
		return 0.0

"""Validate the course by checking whether the department code match"""
def is_valid(course):
	catelog = ['BIO','PSC','CHM','CSC','MAT','STA','ENG','MGA','MGF','MGH','MGM','PSY','COG']
	if course in catelog:
		return True
	return False

"""Takes a course record as input such as 'XXXA01,75'
   Returns a list of two elements ['XXXA01','75']
"""
def script_format(course_transcript):
	return course_transcript.split(",")

"""Calculate the average GPA given the transcript list of courses code and grade, expect input to be a list of String items in the form of ['XXXA01,75','YYYB03,84']"""
def calculate_gpa(transcript):
	#check if transcript empty, return 0.0 if no courses were taken
	if not len(transcript):
		return 0

	count = 0.0
	total_gpa = 0.0
	for entry in transcript:
		cleanscript = script_format(entry)
		#check if the course code is valid
		if is_valid(cleanscript[0][0:3].upper()):
			count += 1
			total_gpa += get_gpa(cleanscript[1])
		else:
			#print "entry",entry,"not valid"
			pass
	#check if no valid courses
	if count > 0:
		return total_gpa / count
	else:
		return 0



"""Return the course list of a given department, if department doesn't exist return an empty list"""
def get_course(department):
	if department == "Biology":
		return ['BIO','PSC']
	elif department == "Chemistry":
		return ['CHM','PSC']
	elif department == "Computer Science":
		return ['CSC','MAT','STA']
	elif department == "English":
		return ['ENG']
	elif department == "Management":
		return ['MGA','MGF','MGH','MGM']
	elif department == "Psychology":
		return ['PSY','COG']
	else:
		return []


"""Calculate the average GPA of course that only in the students' major """
def calculate_dgpa(transcript, major):
	#check if transcript empty, return 0.0 if no courses were taken
	if not len(transcript):
		return 0

	#Get the course list of the corresponding major
	course_list = get_course(major)

	#if no major was found, return 0
	if not course_list:
		#print "No such major was found!"
		return 0

	count = 0.0
	total_gpa = 0.0
	#Loop throught the transcipt to get  dgpa
	for entry in transcript:
		cleanscript = script_format(entry)
		#check if course is in the list
		if cleanscript[0][0:3].upper() in course_list:
			count += 1
			total_gpa += get_gpa(cleanscript[1])

	#check if there is no major course taken
	if count > 0:
		return total_gpa / count
	else:
		print 1
		return 0

"""Calculate the weighted deparment GPA for a student"""
def calculate_weighted_dgpa(transcript, major, weight=1):
	#check if transcript empty, return 0.0 if no courses were taken
		if not len(transcript):
			return 0

		#Get the course list of the corresponding major
		course_list = get_course(major)

		#if no major was found, return 0
		if not course_list:
			print "No such major was found!"
			return 0

		count = 0.0
		total_gpa = 0.0
		#Loop throught the transcipt to get  dgpa
		for entry in transcript:
			cleanscript = script_format(entry)
			#check if course is in the list
			if cleanscript[0][0:3].upper() in course_list:
				#check if course is subject to weight adjustments
				if cleanscript[0][3].upper() in ['C','D']:
					count += 1 * weight
					total_gpa += get_gpa(cleanscript[1]) * weight
				else:
					count += 1
					total_gpa += get_gpa(cleanscript[1])

		#check if there is no major course taken
		if count > 0:
			return total_gpa / count
		else:
			return 0


"""Start the interview to get student input and interactions for their GPA, DGPA etc"""
def interview():
	print "Welcome to U of Scarborough Info System"
	#username = raw_input('Please Enter Your Name: ')
	#student_num = raw_input('Please Enter Your Student Number: ')
	print "Great, let's get some work done! How can I help?"
	#Keep track of the input
	input_transcipt = []

	while True:
		#Invoke user to input options
		print 'You can: \n 1. Input or Edit Your Transcript Information\n 2. Calculate Your GPA \n 3. Calculate Your DGPA \n 4. Calculate Your Weighted DGPA \n 5. Quit \n 6. Clear Input Data'
		option = raw_input('Please enter the option number (e.g Enter "2" for your GPA): ')

		#Test the option input
		try:
	   		val = int(option)
		except ValueError:
	   		print("Please enter a valid option between 1 and 6: ")
			option = raw_input('Please enter the option number (e.g Enter "2" for your GPA): ')

		#Check the validity of the option
		if int(option) not in range(1,7):
			print("Please enter a valid option between 1 and 6: ")
			option = raw_input('Please enter the option number (e.g Enter "2" for your GPA): ')

		#Different cases on the value of options input
		if option == "1":
		   if (input_transcipt == []):
		   	  input_transcipt = get_input_transcript(input_transcipt)
		   else:
			  print input_transcipt
			  response = raw_input("Do You want to modify your transcript data? Type 'Y/y' for Yes, anything else for No")
			  if response.upper() == 'Y':
				 input_transcipt = []
				 input_transcipt = get_input_transcript(input_transcipt)


		#The user quits
		elif option  == "5":
		   exit("Bye Bye!")

		elif option == "6":
		   input_transcipt = []
		   print "User data cleared!"

		else:
			if option == "2":
				print "You choosed to calculate your GPA!"
				if not len(input_transcipt):
					input_transcript = get_input_transcript(input_transcipt)

				gpa = calculate_gpa(input_transcipt)
				print "Your GPA is", gpa
				response = raw_input("Press enter to Continue, press 'q' to quit: ")

				if response == 'q':
					exit('Have a lovely Day!')


			elif option == "3":
				print "You choosed to calculate your Department GPA(DGPA)!"
				if not len(input_transcipt):
					input_transcript = get_input_transcript(input_transcipt)
					#already input major
				major = raw_input("Please enter your Department (eg. Business) : ")
				dgpa = calculate_dgpa(input_transcipt, major)

				print "Your DGPA is", dgpa
				response = raw_input("Press enter to Continue, press 'q' to quit: ")
				if response == 'q':
					exit('Ciao!')


			elif option == "4":
				print "You choosed to calculate your Weighted DGPA!"
				if not len(input_transcipt):
					input_transcript = get_input_transcript(input_transcipt)
					#already input major
				major = raw_input("Please enter your Department (eg. Business) : ")
				weight = raw_input("Plese enter the adjustment rate :")
				if not weight:
					weight = 1
				wdgpa = calculate_weighted_dgpa(input_transcipt, major, float(weight))

				print "Your Weighted DGPA is", wdgpa
				response = raw_input("Press enter to Continue, press 'q' to quit: ")
				if response == 'q':
					exit('Adios!')
	#quit = False
	#while not quit:
	#	break
"""Helper function to clean up the user input"""
def clean_input(userinput):
	if userinput == "":
		return

	inputlist = userinput.split(",")
	if (len(inputlist)) < 2:
		return -1

	output = ""
	for index in range(0,2):
		#Get rid of whitespaces in front or at the back
		item = inputlist[index].strip(" ")
		output = output +item + ','
		#check the grade is a number
		if index:
			try:
			  val = int(item)
			except ValueError:
			  return 0; #error code
	return output[:-1]

def get_input_transcript(input_transcipt):
	print "In order for me to do so please enter your course code and grade as instructed"
	print "Please enter your course code followed by your grade, seperated by a comma like\n this 'CSCA20,99', when you are done press Enter to continue"
	print "Type 'check' to view the transcript, type 'delete' to remove the most recent entry "
	while True:
		inputs = raw_input("Enter Here, Press Enter for another course: ")
		if inputs:
			cleaned_input = clean_input(inputs)
			if inputs.strip(" ").lower() == 'check': #check command typed
				print input_transcipt
			elif inputs.strip(" ").lower() == 'delete': #delete command typed
				if len(input_transcipt):
				   input_transcipt.pop(-1)
				   print input_transcipt
			elif cleaned_input == -1: #input insufficient
				print "OOPS! Seems like something's missing!"
			elif cleaned_input == 0: #grade is not a number
				print "Please enter a number for you grade!"
			else:
				#check if there is repetive entry, ask permission to overwrite
				input_transcipt.append(cleaned_input)
				print "Course added."
				print input_transcipt

		else:
			return input_transcipt #test




if __name__ == "__main__":
	interview()
	#print clean_input('DS   ,SD,  43')
	#print get_gpa(30)
	#print get_gpa(90)
	#print get_gpa(73)
	#print get_gpa(67)
	#print script_format('XXXA01,75')
	#my_input = []
	#my_input =['CSCA01,75','YYYB03,84',"CSCA08,90","PSYB003,23"]
	#my_input = ['mgaA20,90','CsCA01,77','MaTB03,78', 'CScC04,74','STAD05,92']
	#my_input1 = ['MGAA20,90','CSCA01,77','MATB03,78', 'CSCC04,74','STAD05,92']
	#print calculate_dgpa(my_input1,"Computer Science")
	#print calculate_dgpa(my_input,"Computer Science")
	#print calculate_weighted_dgpa(my_input1, "Computer Science", 1.5)
	#print calculate_weighted_dgpa(my_input, "Computer Science")
	#print get_course('')
