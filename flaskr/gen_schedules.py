#Generate Schedules
from "class_unit.py" import ClassUnit
from statistics import mean

#Calculate metrics/ mean dist b/w consecutive classes
def calc_metric(schedule, dist):
    dists = []
    for idx in enumerate(schedule):
        if idx != 0:
            dists.append(dist[schedule[idx].room][schedule[idx-1].room])
    return mean(dists)

#Find longest distance b/w consecutive classes for a schedule
def worstDist(schedule, dist):
    worstDist = 0
    worstDistIdx = 0;
    for idx in enumerate(schedule):
        if idx != 0:
            dist = dist[schedule[idx].room][schedule[idx-1].room]
            if dist > worstDist:
                worstDistIdx = idx
                worstDist = dist
    return worstDistIdx-1 #Return first of two consecutive classes

#Find the key for the smallest value in a dictionary
def leastDictEl(dictionary):
    leastValue = 9999999
    leastKey = ""

    for key, value in dictionary:
        if value < least:
            least = value
            leastKey = key
    return leastKey


#Set initial schedules (semi randomly)
def initialize_class_units(class_units, rooms, num_periods, sectionAvail):
    for period in range(0, num_periods):
        for room in rooms:
            for courses in room["courses"]:
                for section in courses:
                    if sectionAvail[section] == 1:
                        sectionAvail[section] = 0
                        #currentClass.fill(room["id"], course, period, section)
                        class_units.append(ClassUnit(room["id"], course, period, section))

def initialize_schedules(class_units, num_periods, section_enroll):
    schedules = []
    for student in students:
        schedule = []
        for period in range(0, num_periods):
            for course in student["courses"]:
                for class_unit in class_units:
                    if class_unit.period == period:
                        if section_enroll[class_unit.section] < max_enroll:
                            if class_unit.course == course:
                                section_enroll[class_unit.section] +=1
                                schedule.append(class_unit)
        schedules.append(schedule)
    return schedules

def closest_course(class_in, free_space = False):
    period = class_in.period
    course = class_in.course

    if free_space == False:
        closest_unit_dist = 99999
        for class_unit in class_units:
            if class_unit.period = period:
                if class_unit.course = course:
                    classDist = dist[class_in.room][class_unit.room]
                    if classDist < closest_unit_dist:
                        closest_unit_dist = classDist
                        closest_unit = class_unit
    else:
        closest_unit_dist = 99999
        for class_unit in class_units:
            if class_unit.period = period:
                if class_unit.course = course:
                    if section_enroll[closest_unit.section] < max_enroll:
                        classDist = dist[class_in.room][class_unit.room]
                        if classDist < closest_unit_dist:
                            closest_unit_dist = classDist
                            closest_unit = class_unit

    return closest_unit

#Optimize schedules by equalizing metric
def optimize(metrics, schedules, max_itr, class_units, section_enroll, dist):
    itr = 0
    while itr < max_itr:
        leastKey = leastDictEl(metrics)
        currentSchedule = schedules[leastKey]
        worstIdx = worstDist(currentSchedule, dist)
        #worstPeriod = currentSchedule[worstIdx]
        period = currentSchedule[worstIdx].period
        course = currentSchedule[worstIdx].course

        closest_unit = closest_course(currentSchedule[worstIdx])

        section_enroll[currentSchedule[worstIdx].section] -= 1

        if section_enroll[closest_unit.section] < max_enroll:
            section_enroll[closest_unit.section] += 1
            currentSchedule[worstIdx] = closest_unit
        else:
            top_metric = 0
            for studentID, schedule in schedules:
                if schedule[period] == closest_unit:
                    if metrics[studentID] > top_metric:
                        top_metric = metrics[studentID]
                        best_student = studentID

            #Closest same course with space for best_student
            closest_unit_best = closest_course(closest_unit, free_space = True)
            section_enroll[schedules[studentID][period].section] -= 1
            section_enroll[closest_unit_best.section] += 1
            schedules[studentID][period] = closest_unit_best

        schedules[leastKey] = currentSchedule

        itr += 1

#Read JSON
#List of students
# students = load()
# rooms = load()
# dist = load()

num_periods = len(students[0]["courses"]) #Number of periods in the day

max_enroll = 33

courseIDs = []
course_counts = []
for student in students:
    for course in student["courses"]:
        if course in courseIDs:
            course_counts[courseIDs.index(course)] += 1
        else:
            courseIDs.append(course)
            course_counts.append(1)

sorted_sections = []
unsorted_sections = []
for count in course_counts:
    section = []
    for itr in xrange(count):
        section.append("courseIds" + str(itr))
        unsorted_sections.append("courseIds" + str(itr))
    sorted_sections.append(section)

courses = {k:v for k, v in zip(courseIDs, sorted_sections)} #load() list of courses and how many sections of each

section_enroll = {k:v for k, v in zip(courses.keys(), [0]*len(courses))} #section:students enrolled. Inialize to zero
sectionAvail = {k:v for k, v in zip(unsorted_sections, [1]*len(unsorted_sections))} #availability of section

max_itr = 1 #max number of iterations of optimization

studentIds = [student["id"] for student in students]

class_units = []
initialize_class_units(class_units, rooms, num_periods, sectionAvail)
schedules = initialize_schedules(class_units, num_periods, section_enroll)
schedules = {k:v for k, v in zip(studentIds, schedules)}

metrics = {}
for studentID in schedules:
    metrics[studentID] = calc_metric(schedules[studentID], dist)

optimize(metrics, schedules, max_itr, class_units, section_enroll, dist)
