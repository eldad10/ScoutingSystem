import pandas as pd

from DTO import *


class Initializer:
    def __init__(self, repository):
        self.repo = repository

    def validFile(self,row):
        x1 = row['כמה חלקי משחק הניח בנמוך?'] + row['כמה חלקי משחק הניח באמצעי?'] + row['כמה חלקי משחק הניח בגבוה?']
        x2 = row['כמה קונוסים הוא הניח?'] + row['כמה קוביות הוא הניח?']
        if self.repo.teamInformation.isExist(row['מספר קבוצה'], row['מספר משחק']):
            return (x1==x2 , "file of match " + str(row['מספר משחק']) + " of team " + str(row['מספר קבוצה'])
                    + " by " + str(row['שם הסקאוטר']) + "\nfile dose not submitted well:\nfirst entered " +
                    str(x1) + " and also " + str(x2))
        return (False,"file of match " + str(row['מספר משחק']) + " of team " + str(row['מספר קבוצה'])
                    + " by " + str(row['שם הסקאוטר']) + "\nentered twice")


    def creating_tables(self):
        self.repo.creatTables()

    def insertMatches(self):
        match = int(input("if you want to stop Enter -1 else Enter match number"))
        while match != -1:
            b1 = int(input("Enter Blue 1 position"))
            b2 = int(input("Enter Blue 2 position"))
            b3 = int(input("Enter Blue 3 position"))
            r1 = int(input("Enter Red 1 position"))
            r2 = int(input("Enter Red 2 position"))
            r3 = int(input("Enter Red 3 position"))
            m = Match(*[match, b1, b2, b3, r1, r2, r3])
            self.repo.matches.insert(m)
            self.repo.alliances.insert(Alliance(*[b1, match, "Blue"]))
            self.repo.alliances.insert(Alliance(*[b2, match, "Blue"]))
            self.repo.alliances.insert(Alliance(*[b3, match, "Blue"]))
            self.repo.alliances.insert(Alliance(*[r1, match, "Red"]))
            self.repo.alliances.insert(Alliance(*[r2, match, "Red"]))
            self.repo.alliances.insert(Alliance(*[r3, match, "Red"]))
            match = int(input("if you want to stop Enter -1 else Enter match number"))

    def insertInfo(self):
        self.repo.teamInformation.deleteAll()
        df = pd.read_excel(r'charge up 2023 data.xlsx')
        for index, row in df.iterrows():
            if not (pd.isnull(row[0])):
                valid = self.validFile(row)
                if valid[0]:
                    try:

                        x = TeamInformation(*[row['מספר קבוצה'], row['מספר משחק'], row['שם הסקאוטר'],
                                              row['מאיזה צד התחיל?'],
                                              row['כמה חלקי משחק הניח בשורה הנמוכה?'],
                                              row['כמה חלקי משחק הניח בשורה האמצעית?'],
                                              row['כמה חלקי משחק הניח בשורה הגבוהה?'],
                                              row['איזה חלק משחק הניח?'],
                                              row['האם טיפס באוטונומי?'],
                                              row['כמה חלקי משחק הניח בנמוך?'],
                                              row['כמה חלקי משחק הניח באמצעי?'],
                                              row['כמה חלקי משחק הניח בגבוה?'],
                                              row['כמה קונוסים הוא הניח?'],
                                              row['כמה קוביות הוא הניח?'],
                                              row['מאיפה אסף חלקי משחק?'],
                                              row['האם טיפס בטלאופ?'],
                                              row['הערות: איסוף'],
                                              row['הערות: התנהלות במשחק'],
                                              row['הערות: הגנה'],
                                              row['הערות: טיפוס'],
                                              row['הערות נוספות']])
                        self.repo.teamInformation.insert(x)
                    except Exception:
                        print(Exception.__context__)
                else:
                    print(valid[1])



