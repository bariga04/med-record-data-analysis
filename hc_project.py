import sqlite3
import matplotlib.pyplot as plt
import pandas as pd 


 
connector = sqlite3.connect('healthcare.db')

cursor = connector.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS hc_data(
        Age INTEGER,
        Sex TEXT,
        BMI REAL,
        Children INTEGER,
        Smoker INTEGER,
        Region TEXT,
        Cost INTEGER
    )
    ''')


connector.commit()

#insert specific path to csv file
dataframe = pd.read_csv('medical_costs.csv')
dataframe.to_sql('hc_data', connector, if_exists = 'replace', index = False)


cursor.execute('''
                SELECT AVG([Medical Cost])
                FROM hc_data
                WHERE Smoker = 1;
               '''
               )

smoker_avg = round(cursor.fetchone()[0], 2)

print('\nAverage annual medical cost of smokers: $' + str(smoker_avg))

cursor.execute('''
                SELECT AVG([Medical Cost])
                FROM hc_data
                WHERE Smoker = 0;
               '''
               )

nonsmoker_avg = round(cursor.fetchone()[0], 2)

print('Average annual medical cost of non-smokers: $' + str(nonsmoker_avg))

if smoker_avg > nonsmoker_avg:
    print('\n Based off the dataset, on average, smokers have higher annual medical costs than non-smokers\n')
elif nonsmoker_avg > smoker_avg:
    print('\n Based off the dataset, on average, non-smokers have higher annual medical costs than smokers\n')


cursor.execute('''
                SELECT AVG([Medical Cost])
                FROM hc_data
                WHERE Region = 'Northeast';
               '''
               )

ne_avg = round(cursor.fetchone()[0], 2)

print('\nAverage annual medical cost of residents in the Northeast U.S: $' + str(ne_avg))

cursor.execute('''
                SELECT AVG([Medical Cost])
                FROM hc_data
                WHERE Region = 'Northwest';
               '''
               )

nw_avg = round(cursor.fetchone()[0], 2)

print('Average annual medical cost of residents in the Northwest U.S: $' + str(nw_avg))

cursor.execute('''
                SELECT AVG([Medical Cost])
                FROM hc_data
                WHERE Region = 'southeast';
               '''
               )

se_avg = round(cursor.fetchone()[0], 2)

print('Average annual medical cost of residents in the Southeast U.S: $' + str(se_avg))

cursor.execute('''
                SELECT AVG([Medical Cost])
                FROM hc_data
                WHERE Region = 'southwest';
               '''
               )

sw_avg = round(cursor.fetchone()[0], 2)

print('Average annual medical cost of residents in the Southwest U.S: $' + str(sw_avg))

if max(ne_avg, nw_avg, se_avg, sw_avg) == ne_avg:
    print('\n Based off the data set, on average, people who reside in the Northeast U.S have higher medical costs compared to residents in other regions of the U.S\n')
elif max(ne_avg, nw_avg, se_avg, sw_avg) == nw_avg:
    print('\n Based off the data set, on average, people who reside in the Northwest U.S have higher medical costs compared to residents in other regions of the U.S\n')
elif max(ne_avg, nw_avg, se_avg, sw_avg) == se_avg:
    print('\n Based off the data set, on average, people who reside in the Southeast U.S have higher medical costs compared to residents in other regions of the U.S\n')
elif max(ne_avg, nw_avg, se_avg, sw_avg) == sw_avg:
    print('\n Based off the data set, on average, people who reside in the Southwest U.S have higher medical costs compared to residents in other regions of the U.S\n')

def message_output(cf):
    if -1 <= cf < -0.8:
        return 'There is a very strong negetive correlation between these two variables.'
    elif -0.8 <= cf < -0.6:
        return 'There is a strong negetive correlation between these two variables.'
    elif -0.6 <= cf < -0.4:
        return 'There is moderate negetive correlation between these two variables.'
    elif -0.4 <= cf <= -0.2:  
        return 'There is a weak negetive correlation between these two variables.'
    elif -0.2 < cf < 0.2:
        return 'There is a very weak correlation between these two variables.'
    elif 0.2 <= cf <= 0.4:
        return 'There is a weak positive correlation between these two variables.'
    elif 0.4 < cf <= 0.6:
        return 'There is a moderate positive correlation between these two variables'
    elif 0.6 < cf <= 0.8:
        return 'There is a strong positive correlation between these two variables'
    elif 0.8 < cf <= 1:
        return 'There is a very strong positive correlation between these two variables'
    else:
        return 'error'


age_cf = dataframe['Age'].corr(dataframe['Medical Cost'])
print('\nThe correlation coefficient between the age of a person and their annual medical cost is approximately ' + str(round(age_cf,2)) + '. ' + message_output(age_cf))

children_cf = dataframe['Children'].corr(dataframe['Medical Cost'])
print('\nThe correlation coefficient between the number of children a person has and their annual medical cost is approximately ' + str(round(children_cf, 2)) + '. ' + message_output(children_cf))

#Graphs of Data:

figure = plt.figure(figsize = (6, 6))

sub1 = figure.add_subplot(2, 1, 1)
sub1.bar(['Smoker', 'Non-Smoker'], [smoker_avg, nonsmoker_avg],
         color =['purple', 'blue'])
sub1.set_title('Average Medical Costs for Smokers and Non-Smokers')
sub1.set_ylabel('Average Annual Medical Cost (USD)')

sub2 = figure.add_subplot(2, 1, 2)
sub2.bar(['Northeast', 'Northwest', 'Southeast', 'Southwest'], [ne_avg, nw_avg, se_avg, sw_avg],
         color  = ['grey'])                                                                                              
sub2.set_title('Average Medical Costs For Different U.S. Regions')
sub2.set_ylabel('Average Annual Medical Cost (USD)')
sub2.set_ylim(11000)
sub2.set_xlabel('Region of U.S')


figure.tight_layout()
plt.show()

connector.commit()

connector.close()