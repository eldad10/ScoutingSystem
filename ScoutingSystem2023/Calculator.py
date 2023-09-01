from DTO import *
from Repository import Repository
import matplotlib.pyplot as plt


def printGraph(team, data, rowName, indexData, scatter=False, l=0):
    labelx = [x[0] for x in data]
    lately = [x[indexData] for x in data]
    plt.xlabel("match number")
    plt.ylabel(rowName)
    plt.title(rowName + " over the games of team " + str(team))
    if l == 0:
        plt.plot(labelx, lately)
    else:
        plt.plot(labelx, lately, label=l)


# constant
TeamNumber = 0
autoLow = 1
autoMid = 2
autoHigh = 3
teleopLow = 4
teleopMid = 5
teleopHigh = 6
teleopCones = 7
teleopCubs = 8
stringList = 9


def convertStartPos(pos):
    if pos == 'אמצע':
        return "MIDDLE\n"
    else:
        return "SIDE\n"


def convertAutoGP(autoGP):
    if autoGP == 'קוביות':
        return "ROBOT PUT CUBES\n"
    if autoGP == 'קונוסים':
        return "ROBOT PUT CONES\n"
    if autoGP == 'גם וגם':
        return "ROBOT PUT CUBES AND CONES\n"
    if autoGP == 'כלום':
        return "ROBOT NOT PUT PIECES\n"
    return "ROBOT NOT PUT PIECES\n"


def convertClimb(climb):
    if climb == 'כן - מאוזן':
        return "THE ROBOT WAS ENGAGED\n"
    if climb == 'כן - לא מאוזן':
        return "THE ROBOT WAS DOCKED\n"
    if climb == 'ניסה ולא הצליח':
        return "THE ROBOT TRIED TO CLIMB BUT DID NOT SUCCEED\n"
    if climb == 'לא ניסה':
        return "THE ROBOT DID NOT TRY TO CLIMB\n"


def convertTakenFrom(Tfrom):
    if Tfrom == 'רצפה':
        return "ROBOT TAKEN FROM THE FLOOR\n"
    if Tfrom == 'שחקן אנושי':
        return "ROBOT TAKEN FROM HUMAN PLAYER\n"
    if Tfrom == 'גם וגם':
        return "ROBOT TAKEN FROM THE FLOOR AND HUMAN PLAYER\n"
    if Tfrom == 'לא אסף':
        return "ROBOT NOT COLLECT PIECES\n"


def hasComment(c):
    return not (c == 'X')


def avgPrintStart(start):
    middle = 0
    side = 0
    for i in start:
        if i == 'אמצע':
            middle += 1
        else:
            side += 1
    return 100 * (middle / (middle + side))


def favoriteAuto(kind):
    cones = 0
    cubs = 0
    for i in kind:
        if i == 'קוביות':
            cubs += 1
        if i == 'קונוסים':
            cones += 1
        if i == 'גם וגם':
            cones += 1
            cubs += 1
    if cones > cubs:
        return "CONES\n"
    if cubs > cones:
        return "CUBS\n"
    return "BOTH\n"


def getClimbingData(climb):
    data = list()
    data.append(0)  # climbing %
    data.append(0)  # engage
    data.append(0)  # success
    for i in climb:
        if i == 'כן - מאוזן':
            data[0] += 1
            data[1] += 1
            data[2] += 1
        if i == 'כן - לא מאוזן':
            data[0] += 1
            data[2] += 1
        if i == 'לא ניסה':
            data[2] += 1
            data[1] += 1
        if i == 'ניסה ולא הצליח':
            data[1] += 1
    data[0] = 100 * (data[0] / len(climb))
    data[1] = 100 * (data[1] / len(climb))
    data[2] = 100 * (data[2] / len(climb))
    return data


def favoriteTeleop(cones, cubs):
    if cones > cubs:
        return "FAVORITE GAME PIECE IN TELEOP IS: CONES\n"
    if cubs > cones:
        return "FAVORITE GAME PIECE IN TELEOP IS: CUBS\n"
    return "FAVORITE GAME PIECE IN TELEOP IS: BOTH\n"


class Calculetor:
    def __init__(self, repository):
        self.repo = repository

    def printMatchInfo(self, teamNumber, matchNumber, printing=True):
        teamInfo = self.repo.teamInformation.findData(teamNumber, matchNumber)
        stri = ""
        stri = stri + "MATCH NUMBER " + str(teamInfo.matchNumber) + " ON TEAM " + str(teamInfo.teamNumber) + ":\n"
        stri = stri + "----------------------------------\n"
        stri = stri + "--AUTONOMOUS MODE:\n"
        stri = stri + "ROBOT STARTED FROM THE " + str(convertStartPos(teamInfo.startSide))
        stri = stri + convertAutoGP(teamInfo.autoKindGP)
        if teamInfo.autoLowGP > 0:
            stri = stri + str(teamInfo.autoLowGP) + " GAME PIECES IN THE LOW\n"
        if teamInfo.autoMidGP > 0:
            stri = stri + str(teamInfo.autoMidGP) + " GAME PIECES IN THE MID\n"
        if teamInfo.autoHighGP > 0:
            stri = stri + str(teamInfo.autoHighGP) + " GAME PIECES IN THE HIGH\n"
        stri = stri + str(teamInfo.autoHighGP + teamInfo.autoMidGP + teamInfo.autoLowGP) + " IN TOTAL\n"
        stri = stri + convertClimb(teamInfo.autoClimb)
        stri = stri + "--TELEOP MODE:\n"
        if teamInfo.teleopCons > 0:
            stri = stri + "ROBOT SCORED " + str(teamInfo.teleopCons) + " CONES\n"
        if teamInfo.teleopCubs > 0:
            stri = stri + "ROBOT SCORED " + str(teamInfo.teleopCubs) + " CUBES\n"
        if teamInfo.teleopLowGP > 0:
            stri = stri + str(teamInfo.teleopLowGP) + " IN THE LOW\n"
        if teamInfo.teleopMidGP > 0:
            stri = stri + str(teamInfo.teleopMidGP) + " IN THE MID\n"
        if teamInfo.teleopHighGP > 0:
            stri = stri + str(teamInfo.teleopHighGP) + " IN THE HIGH\n"
        stri = stri + str(teamInfo.teleopCons + teamInfo.teleopCubs) + " IN TOTAL\n"
        stri = stri + convertTakenFrom(teamInfo.takenFrom)
        stri = stri + convertClimb(teamInfo.teleopClimb)
        if printing:
            stri = stri + "--COMMENTS\n"
            if hasComment(teamInfo.commentsIntake):
                stri = stri + "INTAKE COMMENTS: " + teamInfo.commentsIntake + "\n"
            if hasComment(teamInfo.commentsField):
                stri = stri + "FIELD COMMENTS: " + teamInfo.commentsField + "\n"
            if hasComment(teamInfo.commentsDefense):
                stri = stri + "DEFENSE COMMENTS: " + teamInfo.commentsDefense + "\n"
            if hasComment(teamInfo.commentsClimb):
                stri = stri + "CLIMB COMMENTS: " + teamInfo.commentsClimb + "\n"
            stri = stri + "OTHER COMMENTS: " + teamInfo.comments + "\n"
            print(stri)
        return stri

    def printTeamFullInfo(self, teamNumber, printing=True):
        matches = self.repo.teamInformation.findAll(teamNumber)
        data = list()
        for info in matches:
            data.append(self.printMatchInfo(info.teamNumber, info.matchNumber,printing))
            if printing:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        data.append(self.printAverage(teamNumber,printing))
        return data

        #self.showGraph(teamNumber)

    def printAverage(self, teamNumber, printing=True):
        data = self.repo.teamInformation.find_avg(teamNumber)
        text = data[stringList]
        start = list()
        aclimb = list()
        tclimb = list()
        kind = list()
        for i in text:
            start.append(i[0])
            aclimb.append(i[2])
            tclimb.append(i[3])
            kind.append(i[1])
        autoClimb = getClimbingData(aclimb)
        teleopClimb = getClimbingData(tclimb)
        stri = ""

        stri = stri +"AVERAGE DATA ON TEAM " + str(data[TeamNumber]) + ":\n"
        stri = stri +"----------------------------------\n"
        stri = stri +"--AUTONOMOUS MODE:\n"
        stri = stri +"STARTING FROM THE MIDDLE IN " + str(avgPrintStart(start)) + "% OF THE TIME\n"
        stri = stri +"TOTAL GAME PIECES IN AUTO: " + str(data[autoLow] + data[autoMid] + data[autoHigh])+"\n"
        stri = stri +str(round(data[autoLow], 2)) + " IN THE LOW\n"
        stri = stri +str(round(data[autoMid], 2)) + " IN THE MID\n"
        stri = stri +str(round(data[autoHigh], 2)) + " IN THE HIGH\n"
        stri = stri +"AUTO CLIMB " + (str(autoClimb[0]) + "%. " + str(autoClimb[1]) + "% OF THE TIME WAS ENGAGED. AND "+ str(autoClimb[2]) + "% SUCCESS\n")
        stri = stri +("FAVORITE GAME PIECE IN AUTO: " + favoriteAuto(kind))
        stri = stri + ("--TELEOP MODE\n")
        temp = ("TOTAL GAME PIECES IN TELEOP: " + str(data[teleopLow] + data[teleopMid] + data[teleopHigh])+"\n")

        stri = stri + temp
        temp = str(round(data[teleopLow], 2)) + " IN THE LOW\n"
        stri = stri + temp
        temp = str(round(data[teleopMid], 2)) + " IN THE MID\n"
        stri = stri + temp
        temp = str(round(data[teleopHigh], 2)) + " IN THE HIGH\n"
        stri = stri + temp
        temp = "CONES IN TELEOP " + str(data[teleopCones])+"\n"
        stri = stri + temp
        temp = "CUBS IN TELEOP " + str(data[teleopCubs])+"\n"
        stri = stri + temp
        temp = favoriteTeleop(data[teleopCones], data[teleopCubs])
        stri = stri + temp
        temp = "TELEOP CLIMB " + str(teleopClimb[0]) + "%. " + str(teleopClimb[1]) + "% OF THE TIME WAS ENGAGED. AND "+ str(teleopClimb[2]) + "% SUCCESS\n"
        stri = stri + temp
        if printing:
            print(stri)
        return stri
        # starting side average
        # total avg gp in auto
        # gp in every level
        # climbing %
        # engaed %
        # climbing success
        # favorite gp (if possible)
        # total gp in teleop
        # gp in every level
        # cones and cubs %
        # climbing %
        # engaed %
        # climbing success

    def showGraph(self, teamNumber,printing = True):
        data = self.repo.teamInformation.getGraphInfo1(teamNumber)
        printGraph(teamNumber, data, "Auto Game Pieces", 1, l="Low")
        printGraph(teamNumber, data, "Auto Game Pieces", 2, l="Mid")
        printGraph(teamNumber, data, "Auto Game Pieces", 3, l="High")
        plt.legend()
        if printing:
            plt.show()
        else:
            t = str(teamNumber) + "1.png"
            plt.savefig(t)
            plt.clf()
        data = self.repo.teamInformation.getGraphInfo2(teamNumber)
        printGraph(teamNumber, data, "Teleop Game Pieces", 1, l="Low")
        printGraph(teamNumber, data, "Teleop Game Pieces", 2, l="Mid")
        printGraph(teamNumber, data, "Teleop Game Pieces", 3, l="High")
        plt.legend()
        if printing:
            plt.show()
        else:
            t = str(teamNumber) + "2.png"
            plt.savefig(t)
            plt.clf()

        data = self.repo.teamInformation.getGraphInfo3(teamNumber)
        printGraph(teamNumber, data, "Teleop cones and cubs", 1, l="Cones")
        printGraph(teamNumber, data, "Teleop cones and cubs", 2, l="Cubs")
        plt.legend()
        if printing:
            plt.show()
        else:
            t = str(teamNumber) + "3.png"
            plt.savefig(t)
            plt.clf()

    def compareGraph(self, team1, team2):
        data1 = self.repo.teamInformation.getCompareData(team1)
        data2 = self.repo.teamInformation.getCompareData(team2)
        printGraph(str(team1) + " And " + str(team2), data1, "Auto Game Pieces", 1, l=str(team1))
        printGraph(str(team1) + " And " + str(team2), data2, "Auto Game Pieces", 1, l=str(team2))
        plt.legend()
        plt.show()

        printGraph(str(team1) + " And " + str(team2), data1, "Teleop Game Pieces", 2, l=str(team1))
        printGraph(str(team1) + " And " + str(team2), data2, "Teleop Game Pieces", 2, l=str(team2))
        plt.legend()
        plt.show()

    def getComments(self, teamNumber):
        val = {'intake':list(),'field':list(),'climb':list(),'defence':list(),'other':list()}
        data = self.repo.teamInformation.getComments(teamNumber)
        for i in data:
            if not(i[1] == 'X'):
                txt = str(i[0]) + "- " + str(i[1])
                val['intake'].append(txt)
            if not (i[2] == 'X'):
                txt = str(i[0]) + "- " + str(i[2])
                val['field'].append(txt)
            if not (i[3] == 'X'):
                txt = str(i[0]) + "- " + str(i[3])
                val['climb'].append(txt)
            if not (i[4] == 'X'):
                txt = str(i[0]) + "- " + str(i[4])
                val['defence'].append(txt)
            if not (i[5] == 'X'):
                txt = str(i[0]) + "- " + str(i[5])
                val['other'].append(txt)
        return val






"""

        data = self.repo.teamInformation.getDataToGraphHighAuto(teamNumber)
        printGraph(teamNumber, data, "High Auto Balls")
        plt.show()

        val = self.repo.teamInformation.getDataToGraphClimb(teamNumber)
        data = [moveClimbToGraph(x) for x in val]
        printGraph(teamNumber, data, "climbing level", True)
        plt.show()
"""
"""
    graphs-----------
    graph 1 ---> auto game pieces in every stage over the games
    graph 2 ---> teleop game pieces in every stage over the games
    graph 3 ---> teleop cones and cubs over the games



    def compareGraph(self, team1, team2):
        data = self.repo.teamInformation.getDataToGraphHighTel(team1)
        labelx = [x[0] for x in data]
        lately = [x[1] for x in data]
        plt.xlabel("match number")
        plt.ylabel("High Teleop Balls")
        plt.title("High Teleop Balls" + " over the games of teams " + str(team1) + " and " + str(team2))
        plt.plot(labelx, lately, label=team1)
        data = self.repo.teamInformation.getDataToGraphHighTel(team2)
        labelx = [x[0] for x in data]
        lately = [x[1] for x in data]
        plt.plot(labelx, lately, label=team2)
        plt.legend()
        plt.show()

        data = self.repo.teamInformation.getDataToGraphHighAuto(team1)
        labelx = [x[0] for x in data]
        lately = [x[1] for x in data]
        plt.xlabel("match number")
        plt.ylabel("High Auto Balls")
        plt.title("High Auto Balls" + " over the games of teams " + str(team1) + " and " + str(team2))
        plt.plot(labelx, lately, label=team1)
        data = self.repo.teamInformation.getDataToGraphHighAuto(team2)
        labelx = [x[0] for x in data]
        lately = [x[1] for x in data]
        plt.plot(labelx, lately, label=team2)
        plt.legend()
        plt.show()

        val = self.repo.teamInformation.getDataToGraphClimb(team1)
        data = [moveClimbToGraph(x) for x in val]
        labelx = [x[0] for x in data]
        lately = [x[1] for x in data]
        plt.xlabel("match number")
        plt.ylabel("climbing level")
        plt.title("climbing level" + " over the games of teams " + str(team1) + " and " + str(team2))
        plt.plot(labelx, lately, 'o', label=team1)
        val = self.repo.teamInformation.getDataToGraphClimb(team2)
        data = [moveClimbToGraph(x) for x in val]
        labelx = [x[0] for x in data]
        lately = [x[1] for x in data]
        plt.plot(labelx, lately, 'o', label=team2)
        plt.legend()
        plt.show()
    """
