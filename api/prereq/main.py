
from CourseCompass.api.prereq.init import TokenType
from tokenize import Tokenize
from CourseCompass.api.prereq.clean import Clean
from CourseCompass.api.prereq.api import API
from CourseCompass.api.prereq.postgres import DB
import json

DB = DB()
TERM = 1245

DB.createPrereqsTable()
DB.createInternalTable()

SUBJECTS = DB.checkInternalDataExist("subjects") # List of subjects --> [CS, MATH, ...]
if not(SUBJECTS):
    SUBJECTS = API.subjects()
    DB.insertInternal("subjects", SUBJECTS)

else:
    SUBJECTS = SUBJECTS.data

CODES = [] # List of all subject codes --> [335, 341, ...]
COURSES = [] # List of all course in JSON format --> [{"subject": "CS", "codes": [335, 341, ...]}, ...]

coursesExist = DB.checkInternalDataExist("courses")
if coursesExist: COURSES = [json.loads(course) for course in coursesExist]

for subject in SUBJECTS:
    print(subject)
    subjectExistsInCourses = False

    if coursesExist:
        for course in COURSES:
            if course["subject"] == subject:
                subjectExistsInCourses = True
                break

    if not(coursesExist) or not(subjectExistsInCourses):
        subjectCodes = API.subjectCodes({'term': TERM, 'subject': subject})
        COURSES.append({"subject": subject, "codes": subjectCodes})

DB.deleteInternalData("courses")
DB.insertInternalData("courses", [json.dumps(course) for course in COURSES])

#     result = DB.checkCourseExist(subject)
#     if not(result):
#         subjectCodes = API.subjectCodes({'term': TERM, 'subject': subject})
#         prereq = {} # <<----- Prasing

#         DB.insertCourse(subject, subjectCodes, prereq)
#         COURSES.extend({"subject": subject, "codes": subjectCodes, "prereq": prereq})

#     else:
#         COURSES.extend(result)

#     if not(codesExist):
#         CODES.extend(result.codes)

# if not(codesExist): 
#     DB.insertInternal("codes", CODES)
# else:
#     CODES = codesExist.data



# tokenizer = Tokenize(CODES, SUBJECTS)

# for row in courses:
#     if row.subject == "CS":
#         j = 0
#         for code in row.codes:
#             if code == "335":
#                 print(code)
#                 prereq_string = API.requirementsDescription({'term': TERM, 'subject': "CS", 'catalog-number': code})

#                 clean_prereq_string = Clean.full_clean(prereq_string)
#                 print(clean_prereq_string)


#                 tokenization = tokenizer.tokenize(clean_prereq_string)
#                 if tokenization:
#                     none = 0
#                     for token in tokenization:
#                         if token.type == TokenType.NONE:
#                             print("warning")
#                             none = 1
                    
#                     if none:
#                         print(clean_prereq_string)

#                     for token in tokenization:
#                         print(token.token, token.type)

#                     tokenization = tokenizer.clean_None(tokenization)
#                     for token in tokenization:
#                         print(token.token, token.type)
