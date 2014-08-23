
import csv

# student data = {"1234567890": ["Harrington", "Brian", "Computer Science",
# ("CSCA01",99), ("CSCA02",97), ("ENGA01",53)],"9876543210":["Smith","A
# lice","English",("ENGA01",87), ("PSYD03",85)] }

'''Take a dictionary of student data,  student number , last name, first name
student number and the department, if the stundent is not in the system, the
record will be added otherwise the record will be updated'''


def add_student(student_data, last_name, first_name, student_id, department):
    if (student_id in student_data.keys()):
        student_data[student_id][0] = last_name
        student_data[student_id][1] = first_name
        student_data[student_id][2] = department
    else:
        student_data[student_id] = [last_name, first_name, department]


'''Return the name of the student from the dictionary that matched the
student_id if the student is not found it will return "No such student"'''


def get_name(student_data, student_id):
    if (student_id in student_data.keys()):
        first_name = student_data[student_id][1]
        last_name = student_data[student_id][0]
        return first_name + ' ' + last_name
    else:
        return "No such student"


'''Takes the student data as a dictionary, stundent number, course and grade
to add or update the grade of the course of that student with the student
number'''


def add_grade(student_data, student_id, course, grade):
    if (student_id in student_data.keys()):
        grades_list = student_data[student_id][3:]
        for grades in grades_list:
            if (grades[0] == course):
                student_data[student_id].remove((grades[0], grades[1]))
        student_data[student_id].append((course, grade))


'''Takes a dictionary of student data, the student number and the course code
and clearreturn the grade of the course that student received, if no such
student exists the student didn't take course, it will return a value of  -1'''


def get_grade(student_data, student_id, course):
    # no such student exists
    if (student_id not in student_data.keys()):
        return -1
    else:
        grades = student_data[student_id][3:]
        for grade in grades:
            if (grade[0] == course):
                return grade[1]
        return -1


'''Takes two csv files, file1 formatted like enrolment.csv and file2 formatted
grades.csv to generate the dictionary of the students info'''


def read_student_data(file1, file2):
    student_data = {}
    # processing enrolnment info file
    for files in [file1, file2]:
        # test the first line of the first to determine file type
        line = files.readline()
        if (line == 'Last,First,Student Number,Department\n'):
            process_enrolment(student_data, files)
        elif (line == 'Student Number,Course Code,Mark\n'):
            process_grades(student_data, files)
    return student_data

'''Helper function to load the enrolment infomation to the database'''


def process_enrolment(student_data, filein):
    enrol_reader = csv.reader(filein)
    for row in enrol_reader:
        if (row == ['Last', 'First', 'Student Number', 'Department']):
            continue
        student_id = row.pop(2)
        student_data[student_id] = row

'''Helper function to load the grades infomation to the database'''


def process_grades(student_data, filein):
    grade_reader = csv.reader(filein)
    for row in grade_reader:
        if (row == ["Student Number", "Course Code", "Mark"]):
            continue
        if (row[0] in student_data.keys()):
            student_data[row[0]].append((row[1], int(row[2])))


'''Helper function to help load data from command line'''


def load_data():
    files = input('''Please specify the TWO csv files that you want to load
one should be containing the enrolment information and the other should contain
the grade info, separeted by a comma, with no space.
eg. enrolment.csv,grades.csv.\n''')
    if (files):
        input_file = files.strip().split(',')
        with open(input_file[0], 'r') as file1, open(input_file[1], 'r') as file2:
            student_data = read_student_data(file1, file2)
            # success
            print("Files loaded.")
            return student_data
    else:
        print("Something wrong with the input. Please check and reload.")
        # failure
        return 0


def interview():
    print("Hello! Welcome to University of Scarborough Enrolment System 2.0!")
    student_data = {}
    print(len(student_data), "of student records available now.")
    while True:
        if (len(student_data) == 0):
            decision = input('''It seems that there is no records existing records
available at the moment, would like to load data from csv files.
Type 'y' for yes and 'n' to continue working with a blank database.\n''')
            if (decision.lower() == 'y'):
                while True:
                    student_data = load_data()
                    if (student_data):
                        print(len(student_data), "of student records available now.")
                        break
        option = input('''Please choose from the following options:
1. Add a student
2. Get the name of a student
3. Add grade to a student
4. Get grade of a student by course code
5. Reload databases from files
6. Exit
eg. Type 1 to add a student\n''')
        option.strip()
        # add a student
        if (option == '1'):
            # last_name, first_name, student_id, department
            info = input('''Please enter the info of the student in following
order last name,first name,student number,department separated by comma
eg. Donald,Carl,,18832138,Computer Science.\n''')
            info_list = info.strip().split(',')
            if (len(info_list) != 4):
                print('Info not complete!')
            else:
                add_student(student_data, info_list[0], info_list[1],
                            info_list[2], info_list[3])
                print('student record added or updated.')
                print(len(student_data), "of student records available now.")

        # get student name
        if (option == '2'):
            info = input('Please enter the student number of the student.\n')
            print(get_name(student_data, info.strip()))
        # add grade
        if (option == '3'):
            info = input('''Please enter the info of the student in following
order student number,course code, and grade separated by comma eg. 18832138,
CSCA20,90.\n''')
            info_list = info.strip().split(',')
            if (len(info_list) != 3):
                print('Info not complete!')
            else:
                add_grade(student_data, info_list[0], info_list[1],
                          int(info_list[2]))
        # get grade of student by course
        if (option == '4'):
            info = input('''Please enter the info of the student in following order
student number,course code,separated by comma eg. 18832138,CSCA20.\n''')
            info_list = info.strip().split(',')
            if (len(info_list) != 2):
                print('Info not complete!')
                break
            if (get_grade(student_data, info_list[0], info_list[1]) == -1):
                print('No such student exists or specified course not taken')
            else:
                print(get_grade(student_data, info_list[0], info_list[1]))
        # reload data
        if (option == '5'):
            student_data = load_data()
            print(len(student_data), "of student records available now.")
        # exit
        if (option == '6'):
            exit('Bye Bye!')
if (__name__ == "__main__"):
    interview()