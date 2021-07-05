import numpy as np
import os
# from p1_one.models import Constants

#os.getcwd()
os.chdir('/Users/snunnari/Documents/GitHub/otree_number_classification')

subjects = 200
mean = 55
sd_high = 20
sd_low = np.sqrt(20)
minimum = 11
maximum = 99
num_trials = 150

matrix_high = []

for s in range(subjects):
    trials = np.empty(0,dtype=int)
    while len(trials) < num_trials:
        number = np.round(np.random.normal(loc=mean, scale=sd_high, size=1),0).astype(int)
        while number == 55 or number < minimum or number > maximum:
            number = np.round(np.random.normal(loc=mean, scale=sd_high, size=1),0).astype(int)
        trials = np.append(trials,number)

    matrix_high.append(trials)

matrix_low = []

for s in range(subjects):
    trials = np.empty(0,dtype=int)
    while len(trials) < num_trials:
        number = np.round(np.random.normal(loc=mean, scale=sd_low, size=1),0).astype(int)
        while number == 55 or number < minimum or number > maximum:
            number = np.round(np.random.normal(loc=mean, scale=sd_low, size=1),0).astype(int)
        trials = np.append(trials,number)

    matrix_low.append(trials)

np.savetxt("numbers_high.csv", matrix_high, fmt='%i', delimiter=",")
np.savetxt("numbers_low.csv", matrix_low, fmt='%i', delimiter=",")
