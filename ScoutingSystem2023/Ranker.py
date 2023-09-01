from DTO import Rank


class Ranker:
    def __init__(self, repository):
        self.repo = repository

    def getData(self):
        data = self.repo.ranks.createRanks()
        fullData = list()
        for i in data:
            climb = self.repo.ranks.findClimbData(i[0])
            fullData.append(Rank(i[0], i[1], i[2], i[3], climb[1], climb[2]))
        return fullData

    def rank(self):
        self.repo.ranks.deleteAll()
        fullData = self.getData()
        print(
            "Rank      Team      AVERAGE POINTS      AVERAGE AUTO POINTS      AVERAGE TELEOP POINTS      AUTO CLIMB       TELEOP CLIMB")
        print(
            "====      =====     ==============      ===================      =====================      ==========       ============")
        for i in range(len(fullData)):
            print(
                "  " + str(i + 1).rjust(2, '0') + "      " + str(fullData[i].TeamNumber).rjust(4, ' ') + "      " + str(
                    round(fullData[
                              i].AvgPoints,
                          2)).ljust(14, ' ') +
                "      " + str(
                    round(fullData[i].avgAuto, 2)).ljust(19, ' ') + "      " + str(
                    round(fullData[i].avgTeleop, 2)).ljust(21, ' ') +
                "      " + str(round(fullData[i].autoClimb, 2)).ljust(11, ' ') + "      "
                + str(round(fullData[i].teleopClimb, 2)).ljust(12, ' '))
    def prepareMatch(self, number, p = True):
        self.repo.ranks.deleteAll()
        fullData = self.getData()
        teams = self.repo.matches.findTeams(number)
        blue = []
        red = []
        for i in fullData:
            if i.TeamNumber == teams.blue1 or i.TeamNumber == teams.blue2 or i.TeamNumber == teams.blue3:
                blue.append(i)
            if i.TeamNumber == teams.red1 or i.TeamNumber == teams.red2 or i.TeamNumber == teams.red3:
                red.append(i)
        blueTel = 0
        redTel = 0
        stri = ""
        stri = stri + "MATCH NUMBER: " + str(number)+"\n"
        stri = stri + "BLUE ALLIANCE:\n"
        stri = stri + "Rank   Team    AVERAGE POINTS   AVERAGE AUTO POINTS   AVERAGE TELEOP POINTS   AUTO CLIMB   TELEOP CLIMB\n"
        stri = stri + "====   =====   ==============   ===================   =====================   ==========   ============\n"
        for i in range(len(blue)):
            stri = stri +("  " + str(i + 1).rjust(2, '0') + "   " + str(blue[i].TeamNumber).rjust(4, ' ') + "    " + str(
                    round(blue[
                              i].AvgPoints,
                          2)).ljust(14, ' ') +"   " + str(
                    round(blue[i].avgAuto, 2)).ljust(19, ' ') + "   " + str(
                    round(blue[i].avgTeleop, 2)).ljust(21, ' ') +"   " + str(round(blue[i].autoClimb, 2)).ljust(11, ' ') + "   "+ str(round(blue[i].teleopClimb, 2)).ljust(12, ' ')+"\n")
            blueTel = blueTel + round(blue[i].AvgPoints, 2)
        stri = stri + "\n"
        stri = stri + "EXPECTED POINTS: " + str(round(blueTel, 2))
        stri = stri + "\n"
        stri = stri +"RED ALLIANCE:\n"
        stri = stri +"Rank   Team    AVERAGE POINTS   AVERAGE AUTO POINTS   AVERAGE TELEOP POINTS   AUTO CLIMB   TELEOP CLIMB\n"
        stri = stri +"====   =====   ==============   ===================   =====================   ==========   ============\n"
        for i in range(len(red)):
            stri = stri +"  " + str(i + 1).rjust(2, '0') + "   " + str(red[i].TeamNumber).rjust(4, ' ') + "    " + str(
                    round(red[
                              i].AvgPoints,
                          2)).ljust(14, ' ') +"   " + str(
                    round(red[i].avgAuto, 2)).ljust(19, ' ') + "   " + str(
                    round(red[i].avgTeleop, 2)).ljust(21, ' ') +"   " + str(round(red[i].autoClimb, 2)).ljust(11, ' ') + "   "+ str(round(red[i].teleopClimb, 2)).ljust(12, ' ')+"\n"
            redTel = redTel + round(red[i].AvgPoints, 2)
        stri = stri + "\n"
        stri = stri + "EXPECTED TELEOP POINTS: " + str(round(redTel, 2))
        stri = stri + "\n"
        if redTel > blueTel:
             value = (stri,"EXPECTED RED ALLIANCE WIN!\n")
        else:
            value = (stri,"EXPECTED BLUE ALLIANCE WIN!\n")
        if p:
            print (value[0])
            print(value[1])

        return value

"""
    def prepareMatch(self, number):
        self.repo.ranks.deleteAll()
        fullData = self.getData()
        teams = self.repo.matches.findTeams(number)
        blue = []
        red = []
        for i in fullData:
            if i.TeamNumber == teams.blue1 or i.TeamNumber == teams.blue2 or i.TeamNumber == teams.blue3:
                blue.append(i)
            if i.TeamNumber == teams.red1 or i.TeamNumber == teams.red2 or i.TeamNumber == teams.red3:
                red.append(i)
        blueTel = 0
        redTel = 0
        print("MATCH NUMBER: " + str(number))
        print("BLUE ALLIANCE:")
        print(
            "Rank      Team      AVERAGE POINTS      AVERAGE AUTO POINTS      AVERAGE TELEOP POINTS      AUTO CLIMB       TELEOP CLIMB")
        print(
            "====      =====     ==============      ===================      =====================      ==========       ============")
        for i in range(len(blue)):
            print(
                "  " + str(i + 1).rjust(2, '0') + "      " + str(blue[i].TeamNumber).rjust(4, ' ') + "      " + str(
                    round(blue[
                              i].AvgPoints,
                          2)).ljust(14, ' ') +
                "      " + str(
                    round(blue[i].avgAuto, 2)).ljust(19, ' ') + "      " + str(
                    round(blue[i].avgTeleop, 2)).ljust(21, ' ') +
                "      " + str(round(blue[i].autoClimb, 2)).ljust(11, ' ') + "      "
                + str(round(blue[i].teleopClimb, 2)).ljust(12, ' '))
            blueTel = blueTel + round(blue[i].AvgPoints, 2)
        print()
        print("EXPECTED POINTS: " + str(round(blueTel, 2)))
        print()
        print("RED ALLIANCE:")
        print(
            "Rank      Team      AVERAGE POINTS      AVERAGE AUTO POINTS      AVERAGE TELEOP POINTS      AUTO CLIMB       TELEOP CLIMB")
        print(
            "====      =====     ==============      ===================      =====================      ==========       ============")
        for i in range(len(red)):
            print(
                "  " + str(i + 1).rjust(2, '0') + "      " + str(red[i].TeamNumber).rjust(4, ' ') + "      " + str(
                    round(red[
                              i].AvgPoints,
                          2)).ljust(14, ' ') +
                "      " + str(
                    round(red[i].avgAuto, 2)).ljust(19, ' ') + "      " + str(
                    round(red[i].avgTeleop, 2)).ljust(21, ' ') +
                "      " + str(round(red[i].autoClimb, 2)).ljust(11, ' ') + "      "
                + str(round(red[i].teleopClimb, 2)).ljust(12, ' '))
            redTel = redTel + round(red[i].AvgPoints, 2)
        print()
        print("EXPECTED TELEOP POINTS: " + str(round(redTel, 2)))
        print()
        if redTel > blueTel:
            print("EXPECTED RED ALLIANCE WIN!")
        else:
            print("EXPECTED BLUE ALLIANCE WIN!")
            
            
            """


