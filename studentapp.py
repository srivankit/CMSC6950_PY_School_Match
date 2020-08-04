import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# school_file = pd.read_csv('schools.csv')
# student_file = pd.read_csv('students.csv')
# quota_file = 'country_quotas.csv'
count_ca = 0
count_in = 0
sch = pd.read_csv('data/schools.csv')
std = pd.read_csv('data/students.csv')
for row in std['Characteristics']:
        if row =='CA':
                    count_ca += 1
        else:
                    count_in += 1

                    # print(count_ca)
                    # print(count_in)
fig, det = plt.subplots()
fig.set_figheight(7)
fig.set_figwidth(10)
font = {'family' : 'Lucida Grande',
        'weight' : 'bold',
        'size'   : 25}

plt.rc('font', **font)
objects = ('Canadian', 'International')
y_pos = np.arange(len(objects))
count = [count_ca, count_in]

plt.bar(y_pos, count, align='center')
plt.xticks(y_pos, objects)
plt.ylabel('Number of Students')
plt.title("Student's Application Distribution")
fig.savefig('StudentApplication')
