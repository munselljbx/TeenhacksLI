#Generate Schedules
from class_unit import ClassUnit
from statistics import mean, stdev
from math import ceil
from pathfinding import heres_a_distance_table_for_you_jeff
import random

#Calculate metrics/ mean dist b/w consecutive classes
def calc_metric(schedule, dist):
    #print(len(schedule))
    dists = []
    for idx in range(0, len(schedule)):
        if idx != 0:
            dists.append(dist[schedule[idx].room][schedule[idx-1].room])
    #print("distlen: " + str(len(dists)))
    return mean(dists) #dists[0]

#Find longest distance b/w consecutive classes for a schedule
def worstDist(schedule, dist):
    worstDist = 0
    worstDistIdx = 0;
    for idx in range(0, len(schedule)):
        if idx != 0:
           dist_inst = dist[schedule[idx].room][schedule[idx-1].room]
           #print(dist_inst)
           # print(dist)
           if dist_inst > worstDist:
                worstDistIdx = idx
                worstDist = dist_inst
    return worstDistIdx-1, worstDistIdx #Return first of two consecutive classes

#Find the key for the smallest value in a dictionary
def leastDictEl(dictionary):
    leastValue = 0
    leastKey = ""

    for key, value in dictionary.items():
        if value > leastValue:
            leastValue = value
            leastKey = key
    #print(leastValue)
    return leastKey


#Set initial schedules (semi randomly)
def initialize_class_units(class_units, rooms, num_periods, sectionAvail):
    for period in range(0, num_periods):
       # print(sectionAvail)
        for room in rooms:
            for course in room["courses"]:
                for section in courses[course]:
                    roomSet = False
                  #  print(section)
                    if sectionAvail[section] == 1:
                        sectionAvail[section] = 0
                        #currentClass.fill(room["id"], course, period, section)
                        class_units.append(ClassUnit(room["id"], course, period, section))
                        #print('add unit')
                        roomSet = True
                        break
                if roomSet:
                    break

def initialize_schedules(class_units, num_periods, section_enroll):
    schedules = []
    for student in students:
        schedule = []
        for period in range(0, num_periods):
            for course in student["courses"]:
                for class_unit in class_units:
                    classSet = False
                    if class_unit.period == period:
                        if section_enroll[class_unit.section] < max_enroll:
                            if class_unit.course == course:
                                section_enroll[class_unit.section] +=1
                                schedule.append(class_unit)
                                classSet = True
                                break
            if classSet:
                break


        schedules.append(schedule)
    #print([len(schedule) for schedule in schedules])
    return schedules

def closest_course(class_in, free_space = False):
    period = class_in.period
    course = class_in.course

    closest_unit = class_in
    if free_space == False:
        closest_unit_dist = 99999
        for class_unit in class_units:
           # print(class_unit.period)
            if class_unit != class_in:
                if class_unit.period == period:
                    if class_unit.course == course:
                        classDist = dist[class_in.room][class_unit.room]
                        if classDist < closest_unit_dist:
                            closest_unit_dist = classDist
                            closest_unit = class_unit
    else:
        closest_unit_dist = 99999
        for class_unit in class_units:
            if class_unit.period == period:
                if class_unit.course == course:
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
        print(leastKey)
        currentSchedule = schedules[leastKey]
        worstIdx, worstIdx2 = worstDist(currentSchedule, dist)
        print(schedules[leastKey][worstIdx].section)
        #print(worstIdx)
        #worstPeriod = currentSchedule[worstIdx]
        period = currentSchedule[worstIdx].period
        #print(currentSchedule[worstIdx].section)
        closest_unit = closest_course(currentSchedule[worstIdx])
        #print(closest_unit.section)

        section_enroll[currentSchedule[worstIdx2].section] -= 1

        if section_enroll[closest_unit.section] < max_enroll:
            section_enroll[closest_unit.section] += 1
            currentSchedule[worstIdx2] = closest_unit
        else:
            top_metric = 0
            for studentID in schedules:
                if schedules[studentID][period] == closest_unit:
                    if metrics[studentID] > top_metric:
                        top_metric = metrics[studentID]
                        best_student = studentID
                        #print(best_student)

            #Closest same course with space for best_student
            closest_unit_best = closest_course(closest_unit, free_space = True)
            section_enroll[schedules[best_student][period].section] -= 1
            section_enroll[closest_unit_best.section] += 1
            schedules[best_student][period] = closest_unit_best
            print('hey')
            section_enroll[closest_unit.section] += 1
            currentSchedule[worstIdx2] = closest_unit

        schedules[leastKey] = currentSchedule
        print(schedules[leastKey][worstIdx].section)

        for studentID in schedules:
            metrics[studentID] = calc_metric(schedules[studentID], dist)
       # print(metrics)
        print(stdev(metrics.values()))
        print(mean(metrics.values()))
        if itr == 0:
            startMean = mean(metrics.values())
            startSTD = stdev(metrics.values())
        elif itr == max_itr-1:
            endMean = mean(metrics.values())
            endSTD = stdev(metrics.values())

        itr += 1
    return startMean, startSTD, endMean, endSTD

#Read JSON
#List of students
# students = load()
# rooms = load()
# dist = load()

#students = [{'id':'Jeffrey', 'courses':['Bio', 'Chem']}, {'id':'Jacob', 'courses':['Bio', 'Physics']}, {'id':'Jared', 'courses':['Physics', 'Chem']}]
#rooms = [{'id':1, 'courses':['Chem']}, {'id':2, 'courses':['Bio']}, {'id':3, 'courses':['Physics']}, {'id':4, 'courses':['Bio']}]
dist = heres_a_distance_table_for_you_jeff()
print("DIST " + str(len(dist)))
rooms = []

itr = 0
for el in dist:
    room = {'id': el, 'courses':["Subj" + str(itr//6)]}
    itr += 1
    rooms.append(room)

students = []
for i in range(0, 100):
    student = {'id': i, 'courses': ["Subj" + str(random.randint(0, 8)), "Subj" + str(random.randint(0, 8)), "Subj" + str(random.randint(0, 8)), "Subj" + str(random.randint(0, 8))]}
    students.append(student)
#print(dist)

num_periods = len(students[0]["courses"]) #Number of periods in the daya

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

#print(courseIDs)

sorted_sections = []
unsorted_sections = []
for idx in range(0, len(course_counts)):
    section = []
    for itr in range(int(ceil(course_counts[idx]/max_enroll))): #change 1 back to max_enroll
        section.append(courseIDs[idx] + str(itr))
        unsorted_sections.append(courseIDs[idx] + str(itr))
    sorted_sections.append(section)

courses = {k:v for k, v in zip(courseIDs, sorted_sections)} #load() list of courses and how many sections of each

#print(courses)

section_enroll = {k:v for k, v in zip(unsorted_sections, [0]*len(unsorted_sections))} #section:students enrolled. Inialize to zero
sectionAvail = {k:v for k, v in zip(unsorted_sections, [1]*len(unsorted_sections))} #availability of section
print(section_enroll)
max_itr = 1000 #max number of iterations of optimization

studentIds = [student["id"] for student in students]

class_units = []
initialize_class_units(class_units, rooms, num_periods, sectionAvail)
schedules = initialize_schedules(class_units, num_periods, section_enroll)
schedules = {k:v for k, v in zip(studentIds, schedules)}

#print(schedules)

metrics = {}
for studentID in schedules:
    metrics[studentID] = calc_metric(schedules[studentID], dist)

#print(metrics)

start_mean, start_std, end_mean, end_std = optimize(metrics, schedules, max_itr, class_units, section_enroll, dist)
print("Complete")
print("Starting Mean: " + str(start_mean))
print("Ending Mean: " + str(end_mean))
print("Starting STD: " + str(start_std))
print("Ending STD: " + str(end_std))

# print(schedules['Jacob'][0].course)
# print(schedules['Jacob'][1].course)
# print(rooms)
# print([class_unit.period for class_unit in class_units])
# print(num_periods)
