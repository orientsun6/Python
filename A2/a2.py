import csv
import sqlite3 as sql


'''Read the four provided csv files and construct a database of student data'''


def read_csv_data(file1, file2, file3, file4):
    # database connection
    conn = sql.connect('SORI.db')
    conn.text_factory = str
    cursor = conn.cursor()
    cursor.execute('SELECT name from sqlite_master WHERE type="table"')
    data = cursor.fetchall()
    if (not len(data)):
        # processing files
        for files in [file1, file2, file3, file4]:
            # test the first line of the first to determine file type
            line = files.readline()
            if (line == 'Last,First,Student Number,Department\n'):
                process_enrolment(cursor, files)
            elif (line == 'Student Number, Course ID, Grade\n'):
                process_grades(cursor, files)
            elif (line == 'Name, Office, Department, Faculty ID\n'):
                process_faculty(cursor, files)
            elif (line == 'Faculty ID, Course ID\n'):
                process_teaches(cursor, files)
    conn.commit()
    conn.close()
    

'''Check if the table is already created in the database'''


def is_created(cursor, tablename):
    for row in cursor.execute('SELECT name from sqlite_master WHERE type="table"'):
        if row == (tablename,):
            return True
    return False
    

'''Helper function to create tables and populate data'''


def process_enrolment(cursor, files):
    if not is_created(cursor, 'student'):
        cursor.execute("CREATE TABLE student(student_id INT, last_name TEXT, first_name TEXT, department TEXT)")	
    student_reader = csv.reader(files)
    for row in student_reader:
        if (row == ["Last", "First", "Student Number", "Department"]):
            continue
        cursor.execute('INSERT INTO student Values(?, ?, ?, ?)' ,(int(row[2]), row[0], row[1], row[3]))

def process_grades(cursor, files):
    if not is_created(cursor, 'grade'):
        cursor.execute("CREATE TABLE grade(student_id INT, course_id TEXT, grade INT)")
    grade_reader = csv.reader(files)
    for row in grade_reader:
        if (row == ["Student Number", "Course ID", "Grade"]):
            continue
        cursor.execute('INSERT INTO grade Values(?, ?, ?)' ,(int(row[0]), row[1], int(row[2])))

def process_faculty(cursor, files):
    if not is_created(cursor, 'faculty'):
        cursor.execute("CREATE TABLE faculty(faculty_id INT, name TEXT, department TEXT, office TEXT)")
    faculty_reader = csv.reader(files)
    for row in faculty_reader:
        if (row == ["Name", "Office", "Department", "Faculty ID"]):
            continue
        cursor.execute('INSERT INTO faculty Values(?, ?, ?, ?)', (int(row[3]), row[0], row[2], row[1]))


def process_teaches(cursor, files):
    if not is_created(cursor, 'teaches'):
        cursor.execute("CREATE TABLE teaches(faculty_id INT, course_id TEXT)")    
    teaches_reader = csv.reader(files)
    for row in teaches_reader:
        if (row == ["Faculty ID", "Course ID"]):
            continue
        cursor.execute('INSERT INTO teaches Values(?, ?)' ,(int(row[0]), row[1]))

'''Add the data consists of tuple of strings to the specific talbe in the
database'''


def add_record(cursor, tablename, data):
    # sanity check
    tables = {'student': 4, 'faculty': 4, 'grade': 3, 'teaches': 2}
    if (tablename not in tables.keys()):
        # print("The table does not exist in the database")
        return 0
    else:
        col_num = tables[tablename]
        import ast
        data = ast.literal_eval(data)
        if len(data) != col_num:
            # print("The data provided is insufficient, Please check again")
            return -1
        else:
            try:
                cursor.execute('INSERT INTO '+ tablename + ' Values' + str(data))
            except:
		# print('Something is wrong with the order of the data')
                return -2
            return 1
"""Return the course list of a given department, if department doesn't exist return an empty list"""

	    
def get_course(department):
    if department == "Biology":
        return ['BIO', 'PSC']
    elif department == "Chemistry":
        return ['CHM', 'PSC']
    elif department == "Computer Science":
        return ['CSC', 'MAT', 'STA']
    elif department == "English": 
        return ['ENG']
    elif department == "Management":
        return ['MGA', 'MGF', 'MGH', 'MGM']
    elif department == "Psychology":
        return ['PSY', 'COG']
    else:
        return []


'''Return the DGPA of the student with studentId from the database'''


def find_my_dpga(cursor, studentId):
    cursor.execute('Select department from student where student_id = %d' %int(studentId));
    department = cursor.fetchone()
    if not department:
        return 0
    course_code = get_course(department[0])
    #SELECT avg(G.grade) as dgpa, count(*) as count from student S join grade G
    #ON S.student_id = G.student_id WHERE S.student_id = 1791137187  and G.course_id like "PSC%" Group by S.student_id;  
    total_score = 0
    count = 0
    for course in course_code:
        cursor.execute('''SELECT sum(G.grade) AS dgpa, count(*) AS count FROM student S join grade G
ON S.student_id = G.student_id WHERE S.student_id = ? and G.course_id LIKE ?''' , (int(studentId), (course + '%')))
        res = cursor.fetchall()
        total_score += res[0][0]
        count += res[0][1]
    if not count:
        return 0
    return float(total_score)/ count 


'''Return the string of lecturers that have given lectures to the
student with the studentId'''


def find_lecturers(cursor, studentId):
    # SELECT DISTINCT F.name FROM grade G JOIN teaches T ON G.course_id = T.course_id 
    # JOIN faculty F ON F.faculty_id = T.faculty_id WHERE G.student_id = 1791137187;
    cursor.execute('''SELECT DISTINCT F.name FROM grade G JOIN teaches T ON G.course_id = T.course_id 
JOIN faculty F ON F.faculty_id = T.faculty_id WHERE G.student_id = %d''' %int(studentId))
    teacher_set = ()
    for row in cursor.fetchall():
        teacher_set += (row[0],)
    return teacher_set

'''Return the average of the all courses taught by the lecturer'''


def lecturer_avg(cursor, lecturer):
    # SELECT avg(G.grade) FROM grade G JOIN teaches T ON G.course_id = T.course_id 
    # JOIN faculty F ON F.faculty_id = T.faculty_id WHERE F.faculty_id = 605566;
    cursor.execute('''SELECT avg(G.grade) FROM grade G JOIN teaches T ON G.course_id = T.course_id 
JOIN faculty F ON F.faculty_id = T.faculty_id WHERE F.name = "%s"''' %lecturer)
    average = cursor.fetchone()[0]
    if average:
        return average
    else:
        return 0


'''Function to interact with users'''


def interview():
    print("Hello! Welcome to University of Scarborough Enrolment System 3.0!")
    with open('enrolment.csv', 'r') as file1, open('faculty.csv') as file2:
	    with open('grades.csv', 'r') as file3, open('teaches.csv','r') as file4:
	        read_csv_data(file1, file2, file3, file4)

    # database connection
    conn = sql.connect('SORI.db')
    conn.text_factory = str
    cursor = conn.cursor()  		
    
    while True:
        option = input('''Please choose from the following options:
	1. Add a Record
	2. Find a Student's DGPA
	3. Find s Student's Lectures
	4. Find the Average Scores of a Lecture 
	5. Quit
	eg. Type 1 to add a record\n''')
        option.strip()

        # Add a record to the database
        if (option == '1'):
            info = input('''Please enter the tablename and the data
	    to be inserted in tuples and separated by a semicolon
	    eg. student; (193123213; "Dorsy","Jack","Management" )\n''')        
            info.strip()
            info_list = info.split(';')
            print(info_list)
            if (len(info_list)== 2):
                res = add_record(cursor, info_list[0].strip(), info_list[1].strip())
                if (res == 1):
                    print('Record has been successfully added!')
                elif (res == 0):
                    print('The table does not exist in the database!')
                elif (res == -1):
                    print('The data provided is insufficient, Please check again!')
                elif (res == -2):
                    print('Something is wrong with the order of the data!')		
            else:
                print("Your data seems invalid!")
        # Find the DGPA of a student
        if (option == '2'):
            info = input('''Please enter a student number to find
	    the DGPA of the student\n''')
            info.strip()
            print(find_my_dpga(cursor, info))

	# Find all lectures of a student
        if (option == '3'):
            info = input('''Please enter a student number to find 
            the list of all lectures\n''')   
            info.strip()
            print(find_lecturers(cursor, info))

        # Find the average score for a lecturer
        if (option == '4'):
            info = input('''Please enter the name of the lecturer
	to find the average score of all courses that are taught 
	eg.Mr.T Phillips \n''')   
            info.strip()
            print(lecturer_avg(cursor, info))

	# exit
        if (option == '5'):
            conn.commit()
            conn.close()
            exit('Bye Bye!')

if (__name__ == "__main__"):
    interview()