class Match:
    def __init__(self, gameNumber, blue1, blue2, blue3, red1, red2, red3):
        self.gameNumber = gameNumber
        self.blue1 = blue1
        self.blue2 = blue2
        self.blue3 = blue3
        self.red1 = red1
        self.red2 = red2
        self.red3 = red3


class Alliance:
    def __init__(self, teamNumber, matchNumber, alliance):
        self.teamNumber = teamNumber
        self.matchNumber = matchNumber
        self.alliance = alliance


class TeamInformation:
    def __init__(self, teamNumber, matchNumber, scouterName,startSide,autoLowGP,autoMidGP,autoHighGP,autoKindGP,
                 autoClimb,teleopLowGP,teleopMidGP,teleopHighGP,teleopCons,teleopCubs,takenFrom,teleopClimb,
                 commentsIntake,commentsField,commentsDefense,commentsClimb,comments):
        self.teamNumber = teamNumber
        self.matchNumber = matchNumber
        self.scouterName = scouterName
        self.startSide = startSide
        self.autoLowGP = autoLowGP
        self.autoMidGP = autoMidGP
        self.autoHighGP = autoHighGP
        self.autoKindGP = autoKindGP
        self.autoClimb = autoClimb
        self.teleopLowGP = teleopLowGP
        self.teleopMidGP = teleopMidGP
        self.teleopHighGP = teleopHighGP
        self.teleopCons = teleopCons
        self.teleopCubs = teleopCubs
        self.takenFrom = takenFrom
        self.teleopClimb = teleopClimb
        self.commentsIntake = commentsIntake
        self.commentsField = commentsField
        self.commentsDefense = commentsDefense
        self.commentsClimb = commentsClimb
        self.comments = comments


class Rank:
    def __init__(self, teamNumber, avgPoints, avgAuto, avgTeleop, autoClimb,teleopClimb):
        self.TeamNumber = teamNumber
        self.AvgPoints = avgPoints
        self.avgAuto = avgAuto
        self.avgTeleop = avgTeleop
        self.autoClimb = autoClimb
        self.teleopClimb = teleopClimb
