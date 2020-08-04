def percentage (val1, val2):
    total = val1 + val2
    percent_val1 = ((val1)/total)*100
    return  percent_val1

# Importing py-school-match
import py_school_match as psm
import pandas as pd
# school_file = pd.read_csv('schools.csv')
# student_file = pd.read_csv('students.csv')
# quota_file = 'country_quotas.csv'

sch = pd.read_csv('data/schools.csv')
std = pd.read_csv('data/students.csv')
# qta = pd.read_csv(quota_file)

student = []
schools = {}

for index, row in sch.iterrows():
    
    sc = psm.School(row['Seats'])
    schools[row['Name']] = sc
    
# # # Defining preferences (from most desired to least desired)
# Creating a criteria. This means 'vulnerable' is now a boolean.
# special_NL = psm.Criteria('special_NL', str)
special_CA = psm.Criteria('special_CA', str)
special_INT = psm.Criteria('special_INT', str)


# Assigning students with charecterstics
# student_newfoundland = psm.Characteristic(special_NL, 'NL')
student_canadian = psm.Characteristic(special_CA, 'CA')
student_international = psm.Characteristic(special_INT, 'INT')

for index, row in std.iterrows():
    st = psm.Student()
#     print(index)
    st.name = row['Student_Name']
    st.charac=row['Characteristics']
    st.preferences = [schools[row['Preference_1']], 
                      schools[row['Preference_2']], 
                      schools[row['Preference_3']]]

    if (row['Characteristics'] == 'CA'):
        st.add_characteristic(student_canadian)
    else:
        st.add_characteristic(student_international)
    student.append(st)

    
schools =  list(schools.values())


# # # Creating a lists with the students and schools defined above.

schools = schools
students = student

# #Defining a ruleset
ruleset = psm.RuleSet()

#assigning students with the ids in the dataframe
std_id = []
for r in students:

    st = r.id
    std_id.append(st)
std['std_id'] = std_id

#assigning schools with the ids in the dataframe
sch_id = []
for r in schools:
    sc = r.id
    sch_id.append(sc)
sch['sch_id'] = sch_id
#creating dictionary of names and schools
std_name = dict(zip(std['std_id'], std['Student_Name']))
sch_name = dict(zip(sch['sch_id'], sch['Name']))

# Defining a new rule from the criteria above.
# This time, a flexible quota is imposed.
# This means that each school should have at least 50% percent
# vulnerable students. The "flexible" part means that if there are
# no vulnerable students left, even if the quota is not met, the
# school can now accept non-vulnerable students.
# rule_NL = psm.Rule(special_NL, quota=0.2)
rule_CA = psm.Rule(special_CA, quota=0.3)
# rule_INT = psm.Rule(special_INT, quota=0.9)

# Adding the rule to the ruleset. This means that a 'vulnerable' student has a higher priority.
# Note that rules are added in order (from higher priority to lower priority)
# ruleset.add_rule(rule_NL)
ruleset.add_rule(rule_CA)
# ruleset.add_rule(rule_INT)

# Creating a social planner using the objects above.
planner = psm.SocialPlanner(students, schools, ruleset)


# Selecting an algorithm
algorithm = psm.SIC()

# # #Running the algorithm.
planner.run_matching(algorithm)

# inspecting the obtained assignation
assigned = []
unassigned = []
for student in students:
    if student.assigned_school is not None:
        assigned.append(student.id)
    else:
        unassigned.append(student.id)
          

#Counting number of assigned and unassigned students as per criteria            
assigned_character = []
unassigned_character = []
d = dict(zip(std['std_id'], std['Characteristics']))
for row in unassigned:
    st = d[row]
    unassigned_character.append(st)
for row in assigned:
    st = d[row]
    assigned_character.append(st)
CA_count_assigned = assigned_character.count('CA')  
INT_count_assigned = assigned_character.count('INT') 
CA_count_unassigned = unassigned_character.count('CA')  
INT_count_unassigned = unassigned_character.count('INT') 
#Calculating percentage distr
CA_assgn_per = percentage (CA_count_assigned, INT_count_assigned)
INT_assgn_per = 100 - CA_assgn_per 
CA_unassgn_per = percentage (CA_count_unassigned, INT_count_unassigned)
INT_unassgn_per = 100 - CA_unassgn_per
assigned_per=[CA_assgn_per, INT_assgn_per]
unassigned_per=[CA_unassgn_per, INT_unassgn_per]

# Creating pie chart for the allocation percentage in two categories
import matplotlib.pyplot as plt
fig, det = plt.subplots(1,2)
fig.set_figheight(7)
fig.set_figwidth(10)
font = {'family' : 'Lucida Grande',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
labels = ['Canadian', 'International']
det[0].pie(assigned_per, labels=labels, autopct='%1.2f%%', shadow=True)
det[0].set_title('Assigned Students Percentage Distribution')
det[1].pie(unassigned_per, labels=labels, autopct='%1.2f%%', shadow=True)
det[1].set_title('Unassigned Students Percentage Distribution')
# plt.show()
fig.savefig('allocation.png')
#creating output file with allocated students
assigned_std_name = []
assigned_sch_name = []
unassigned_std_name = []
unassigned_sch_name = []
final_unassigned = []
for student in students:
    if student.assigned_school:
        st = std_name[student.id]
        sc = sch_name[student.assigned_school.id]
        assigned_std_name.append(st)
        assigned_sch_name.append(sc) 
#         print(f'{std_name[student.id]} assigned to {sch_name[student.assigned_school.id]}')
    else:
#         print(f'{std_name[student.id]} not assigned')
        st = std_name[student.id]
        unassigned_std_name.append(st)
        unassigned_sch_name.append('None')
        
assign_dict = {
            'Name': assigned_std_name,
            'Assigned School': assigned_sch_name
                       
          }
for row_std in unassigned_std_name:
    assign_dict['Name'].append(row_std)
    
for row_sch in unassigned_sch_name:
    assign_dict['Assigned School'].append(row_sch)
    

# assign_dict['Name'].append(unassigned_std_name)
# assign_dict['School'].append(unassigned_sch_name)

df = pd.DataFrame(assign_dict)
df.to_csv(r'data/Assigned.csv', index = False)