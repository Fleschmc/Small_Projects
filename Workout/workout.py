import os
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from datetime import datetime
class workout():
    
    def __init__(self):
        self.date = datetime.now().strftime('%m-%d-%Y')
    
    def questions(self):
        quests, days = [], ['Push', 'Pull', 'Leg', 'Run']

        print('What day was it? E.g. Push - Pull - Leg - Run')
        inp = input()
        ppl = days[np.argmax([fuzz.ratio(inp, x) for x in days])]

        while inp != 'exit':
            if ppl == 'Push':
                push_exercises = ['Bench Press', 'Dumbell Press', 'Military Press', 'Incline Press', 'Tricep Press', 'Tricep Extension', 'Flys', 'Dumbell Flys', 'Bent-Over Rear-Delt Raise']
                print('\nWhat exercise did you do? E.g. Bench/Dumbell/Military/Incline/Tricep Press - Tricep Extension - Flys\n  Format: W-W-WxR-R-R')
                inp = input()
                exercise = push_exercises[np.argmax([fuzz.partial_ratio(inp.split(' ')[:-1], x) for x in push_exercises])]
                try:
                    weight, rep = inp.split(' ')[-1].split('x')
                except ValueError:
                    print('\nYour weight/reps are off. Try again:')
                    continue

            elif ppl == 'Pull':
                pull_exercises = ['Barbell Row', 'Dumbell Row', 'Cable Row', 'Lat Pull-Down', 'Barbell Curls', 'Dumbell Curls', 'Hammer Curls', 'Shrugs']
                print('\nWhat exercise did you do? E.g. Barbell/Dumbell/Cable Row - Barbell/Dumbell/Hammer Curls - Shrugs\n  Format: W-W-WxR-R-R')
                inp = input()
                exercise = pull_exercises[np.argmax([fuzz.partial_ratio(inp.split(' ')[:-1], x) for x in pull_exercises])]
                try:
                    weight, rep = inp.split(' ')[-1].split('x')
                except ValueError:
                    print('\nYour weight/reps are off. Try again:')
                    continue

            elif ppl == 'Leg':
                leg_exercises = ['Calf Raises','Leg Extensions', 'Leg Curls', 'Laying-Down Leg Curls', 'Leg Press', 'Squats', 'Kettleball Squats', 'Lunges']
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

                iq = []
                for w, r in zip(weight.split('-'), rep.split('-')):
                    data_dict = {}
                    data_dict['date']     = self.date
                    data_dict['day_type'] = ppl
                    data_dict['exercise'] = exercise
                    data_dict['weight']   = w
                    data_dict['reps']     = r
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

    def make_report():
        pdf = PDF('P', 'mm', 'Letter')

        pdf.add_page()
        pdf.set_font('times', '', 15)
        self.cell(0, 10, '', align = 'C')

    def make_csv(self):
        cwd = os.getcwd()
        data = self.questions()

        df = pd.DataFrame(data)

        if os.path.exists(cwd + '\\workout.csv'):
            old_df = pd.read_csv(cwd + '\\workout.csv')
            df = pd.concat([old_df, df])
        print()
        print(pd.DataFrame(data))
        print('Save? (y)es/(n)o')
        inp = input()
        if inp == 'y':
            df.to_csv(os.getcwd() + '\\workout.csv', index = False)
        
        if datetime.now().strftime('%A') == 'Friday':
            print('Compile Report? (y)es/(n)o')
            inp = input()
            if inp == 'y':
                from fpdf import FPDF
                self.make_report()
                print('Report Saved!')
            else:
                print("Didn't compile report.")
        
        return df

if __name__ == '__main__':
    w = workout()
    w.make_csv()