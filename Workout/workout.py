import os
import smtplib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from fpdf import FPDF
from fuzzywuzzy import fuzz
from email.message import EmailMessage
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta


class Workout():
    

    def __init__(self):
        self.date = datetime.now().strftime('%m-%d-%Y')
        self.cwd  = os.getcwd()
        self.reported = False
    
    def questions(self):
        quests, days = [], ['Push', 'Pull', 'Leg', 'Run']
        data = {'Push' : {'Bench Press' : {'Primary' : 'Chest', 'Secondary' : 'Tricep'}, 'Dumbell Press' : {'Primary' : 'Chest', 'Secondary' : 'Tricep'},
                          'Military Press' : {'Primary' : 'Shoulder', 'Secondary' : 'Tricep'}, 'Incline Press' : {'Primary' : 'Chest', 'Secondary' : 'Shoulder'},
                          'Decline Bench Press' : {'Primary' : 'Lower Chest', 'Secondary' : 'Tricep'}, 'Over-Head Tricep Press' : {'Primary' : 'Tricep', 'Secondary' : 'Lower Back'},
                          'Tricep Press' : {'Primary' : 'Tricep', 'Secondary' : 'Shoulder'}, 'Tricep Extension' : {'Primary' : 'Tricep', 'Secondary' : 'Shoulder'},
                          'Flys' : {'Primary' : 'Chest', 'Secondary' : 'Shoulder'}, 'Dumbell Fly' : {'Primary' : 'Chest', 'Secondary' : 'Shoulder'},
                          'Bent-Over Rear-Delt Raise' : {'Primary' : 'Shoulder', 'Secondary' : 'Back'}},
                'Pull' : {'Barbell Row' : {'Primary' : 'Back', 'Secondary' : 'Bicep'}, 'Upright Barbell Row' : {'Primary' : 'Shoulder', 'Secondary' : 'Back'}, 
                          'Dumbell Row' : {'Primary' : 'Back', 'Secondary' : 'Bicep'}, 'Cable Row' : {'Primary' : 'Back', 'Secondary' : 'Bicep'}, 
                          'Lat Pull-Down' : {'Primary' : 'Back', 'Secondary' : 'Bicep'}, 'Barbell Curls' : {'Primary' : 'Bicep', 'Secondary' : 'Forearm'}, 
                          'Dumbell Curls' : {'Primary' : 'Bicep', 'Secondary' : 'Forearm'}, 'Hammer Curls' : {'Primary' : 'Bicep', 'Secondary' : 'Forearm'},
                          'Shrugs' : {'Primary' : 'Shoulder', 'Secondary' : 'Traps'}, 'Isolated High Row' : {'Primary' : 'Back', 'Secondary' : 'Bicep'}},
                'Leg' : {'Calf Raises' : {'Primary' : 'Calf', 'Secondary' : ''}, 'Leg Extensions' : {'Primary' : 'Quad', 'Secondary' : ''},
                         'Laying-Down Leg Curls' : {'Primary' : 'Hamstring', 'Secondary' : 'Calf'}, 'Kneeling Leg Curls' : {'Primary' : 'Hamstring', 'Secondary' : 'Calf'},
                         'Leg Curls' : {'Primary' : 'Hamstring', 'Secondary' : 'Calf'}, 'Leg Press' : {'Primary' : 'Quad', 'Secondary' : 'Glute'},
                         'Incline Sled Press' : {'Primary' : 'Quad', 'Secondary' : 'Glute'}, 'Squats' : {'Primary' : 'Glute', 'Secondary' : 'Quad'}, 
                         'Kettleball Squats' : {'Primary' : 'Glute', 'Secondary' : 'Quad'}, 'Lunges' : {'Primary' : 'Glute', 'Secondary' : 'Quad'}}}

        print('What day was it? E.g. Push - Pull - Leg - Run')
        inp = input()
        ppl = days[np.argmax([fuzz.ratio(inp, x) for x in days])]

        while inp != 'exit':
            if ppl == 'Push':
                push_exercises = ['Bench Press', 'Dumbell Press', 'Military Press', 'Incline Press', 'Decline Bench Press', 'Over-Head Tricep Press', 'Tricep Press', 'Tricep Extension', 'Flys', 'Dumbell Flys', 'Bent-Over Rear-Delt Raise']
                print('\nWhat exercise did you do? E.g. Bench/Dumbell/Military/Incline/Tricep Press - Tricep Extension - Flys\n  Format: W-W-WxR-R-R')
                inp = input()
                exercise = push_exercises[np.argmax([fuzz.token_sort_ratio(inp.split(' ')[:-1], x) for x in push_exercises])]
                try:
                    weight, rep = inp.split(' ')[-1].split('x')
                except ValueError:
                    print('\nYour weight/reps are off. Try again:')
                    continue

            elif ppl == 'Pull':
                pull_exercises = ['Barbell Row', 'Upright Barbell Row', 'Dumbell Row', 'Cable Row', 'Lat Pull-Down', 'Barbell Curls', 'Dumbell Curls', 'Hammer Curls', 'Shrugs', 'Isolated High Row']
                print('\nWhat exercise did you do? E.g. Barbell/Dumbell/Cable Row - Barbell/Dumbell/Hammer Curls - Shrugs\n  Format: W-W-WxR-R-R')
                inp = input()
                exercise = pull_exercises[np.argmax([fuzz.token_set_ratio(inp.split(' ')[:-1], x) for x in pull_exercises])]
                try:
                    weight, rep = inp.split(' ')[-1].split('x')
                except ValueError:
                    print('\nYour weight/reps are off. Try again:')
                    continue

            elif ppl == 'Leg':
                leg_exercises = ['Calf Raises','Leg Extensions', 'Leg Curls', 'Laying-Down Leg Curls', 'Kneeling Leg Curls', 'Leg Press', 'Incline Sled Press', 'Squats', 'Kettleball Squats', 'Lunges']
                print('\nWhat exercise did you do? E.g. Calf Raises - Leg Extensions/Curls/Press - Laying-Down Leg Curl - Kettleball Squats - Squats - Lunges\n  Format: W-W-WxR-R-R')
                inp = input()
                exercise = leg_exercises[np.argmax([fuzz.partial_ratio(inp.split(' ')[:-1], x) for x in leg_exercises])]
                try:
                    weight, rep = inp.split(' ')[-1].split('x')
                except ValueError:
                    print('\nYour weight/reps are off. Try again:')
                    continue

            elif ppl == 'Run':
                print('\nHow far did you run? E.g. 1.5')
                inp = input()
                exercise = 'Running'
                weight, rep   =  '0', str(inp)

            if inp == 'exit':
                break
            else:

                iq, set = [], 1
                for w, r in zip(weight.split('-'), rep.split('-')):
                    data_dict = {}
                    data_dict['date']     = self.date
                    data_dict['day_type'] = ppl
                    data_dict['exercise'] = exercise
                    data_dict['weight']   = w
                    data_dict['reps']     = r
                    data_dict['set']      = set
                    set += 1
                    iq.append(data_dict)

                print(pd.DataFrame(iq))
                print('Correct? (y)es/(n)o')
                inp = input()
                if inp == 'y':
                    print('Saved it!')
                    quests += iq
                else:
                    print('Edit? (y)es/(n)o')
                    inp = input()
                    if inp == 'y':
                        print('Which? E.g. 1,2,3')
                        inp = input()
                        while True:
                            try:
                                quests[inp]
                                break
                            except:
                                print('Just input a number dude. Try again')
                    else:
                        print("Didn't save it, try again:")
        
        return quests

    def make_report(self):

        print('Compile Report? (y)es/(n)o')
        inp = input()
        if inp == 'y':
            # Checking if assets folder exists, create if not
            if not os.path.exists(self.cwd + '\\report_assets'):
                os.mkdir(self.cwd + '\\report_assets')
            
            # Do the necessary data manipulation
            today               = datetime.now()
            one_ago, two_ago    = today - timedelta(weeks = 1), today - timedelta(weeks = 2)
            data                = pd.read_csv(self.cwd + '\\workout.csv')
            data['date']        = pd.to_datetime(data['date'], format = '%m/%d/%Y')
            data                = data[data['date'] > two_ago]
            data['volume']      = data['weight'] * data['reps']
            data['week']        = np.where(data['date'] < one_ago, 'one', 'two')
            exercises_in_common = list(set(data[data['week'] == 'one']['exercise']) & set(data[data['week'] == 'two']['exercise']))

            # Creating the PDF template
            pdf = FPDF('P', 'mm', 'A4')

            pdf.add_page()
            pdf.set_font('times', '', 20)
            pdf.cell(0, 10, f"{two_ago.strftime('%B %d')}-{one_ago.strftime('%d')} vs {one_ago.strftime('%B %d')}-{today.strftime('%d')}", ln = True, align = 'C')

            # Creating the content based on the workout day e.g. Push/Pull/Leg
            for day in data['day_type'].unique().tolist():
                try:
                    # Get the data pertaining to the workout day
                    exercise_data = data[(data['day_type'] == day) & (data['exercise'].isin(exercises_in_common))]
                    if len(exercises_in_common) > 1:
                        col_wrap_length = 2
                    else:
                        col_wrap_length = 1
                    print(exercise_data)

                    # Create/save/load the plot to put it in the pdf
                    plot = sns.catplot(x = 'week', y = 'volume', hue = 'set', col = 'exercise', col_wrap = col_wrap_length, kind = 'bar', data = exercise_data)
                    plt.savefig(f'{self.cwd}\\report_assets\\{day}_plot.png')

                    # Getting image dimensions
                    w, h = Image.open(f'{self.cwd}\\report_assets\\{day}_plot.png').size
                    ratio = h/w
                    print(ratio)
                    pdf.set_font('times', '', 15)
                    pdf.cell(0, 10, f"{day}:", ln = True)
                    if 200*ratio > 100:
                        w, h = 200*.75, (200*ratio)*.75
                        pdf.image(f'{self.cwd}\\report_assets\\{day}_plot.png', w=w, h=h, x = (210-w)/2)
                    else:
                        pdf.image(f'{self.cwd}\\report_assets\\{day}_plot.png', w=200, h=200*ratio, x = (210-200)/2)
                except ValueError:
                    print(f"{day} day errored out.")

            pdf.output(f"{self.cwd}\\workout_report_{today.strftime('%m-%d-%y')}.pdf")
            print('Report Saved!')
            self.reported = True
        else:
            print("Didn't compile report.")


    def make_csv(self):
        data = self.questions()

        df   = pd.DataFrame(data)

        if os.path.exists(self.cwd + '\\workout.csv'):
            old_df = pd.read_csv(self.cwd + '\\workout.csv')
            df     = pd.concat([old_df, df])
        else:
            print("Didn't find the file so I'll make it")

        print()
        print(pd.DataFrame(data))
        print('Save? (y)es/(n)o')
        inp = input()
        if inp == 'y':
            df.to_csv(self.cwd + '\\workout.csv', index = False)
        
        return df

    def make_email(self):
        print()
        print('Email this to yourself? (y)es/(n)o')
        inp = input()
        if inp == 'y':
            # Uses the dotenv package to load in environment variables
            load_dotenv(find_dotenv())
            USER, PASSWORD = os.getenv('ADDRESS'), os.getenv('PASSWORD')

            msg = EmailMessage()
            msg['subject'] = f"Spreadsheet {self.date}"
            msg['From'] = USER
            msg['To'] = USER

            with open(self.cwd + '\\workout.csv', 'rb') as f:
                csv = f.read()

            msg.add_attachment(csv, maintype = 'application', subtype = 'octet-stream', filename = 'workout.csv')

            if self.reported == True:
                print('Added the report!')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(USER, PASSWORD)
                smtp.send_message(msg)

            print('Emailed it!')
        else:
            print("Didn't email it.")





    def implementer(self):

        self.make_csv()

        self.make_report()

        self.make_email()




if __name__ == '__main__':
    w = Workout()
    w.implementer()