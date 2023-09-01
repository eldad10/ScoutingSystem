from DTO import TeamInformation


class TeamInformations:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, teamInformation):
        self.conn.execute("""
                INSERT INTO TeamInformations (TeamNumber,MatchNumber,Name,startSide,autoLowGP,autoMidGP,autoHighGP
                ,autoKindGP,
                autoClimb,teleopLowGP,teleopMidGp,teleopHighGP,teleopCons,teleopCubs,takenFrom,teleopClimb,
                commentsIntake,commentsField,commentsDefense,commentsClimb,comments) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, [teamInformation.teamNumber, teamInformation.matchNumber, teamInformation.scouterName,
                      teamInformation.startSide, teamInformation.autoLowGP, teamInformation.autoMidGP
            , teamInformation.autoHighGP,
                      teamInformation.autoKindGP, teamInformation.autoClimb, teamInformation.teleopLowGP,
                      teamInformation.teleopMidGP,
                      teamInformation.teleopHighGP, teamInformation.teleopCons, teamInformation.teleopCubs,
                      teamInformation.takenFrom, teamInformation.teleopClimb, teamInformation.commentsIntake,
                      teamInformation.commentsField, teamInformation.commentsDefense, teamInformation.commentsClimb,
                      teamInformation.comments])

    def findData(self, teamNum, matchNum):
        c = self.conn.cursor()
        c = c.execute("""
                        SELECT * FROM TeamInformations WHERE (TeamNumber = ? AND MatchNumber = ?)  
                    """, [teamNum, matchNum]).fetchone()
        return TeamInformation(*c)

    def findAll(self, teamNum):
        c = self.conn.cursor()
        c = c.execute("""
                        SELECT * FROM TeamInformations WHERE TeamNumber = ? ORDER BY MatchNumber  
                    """, [teamNum]).fetchall()
        a = []
        for i in c:
            a.append(TeamInformation(*i))
        return a

    def deleteAll(self):
        self.conn.execute("""
        DELETE FROM TeamInformations
        """)

    def isExist(self, teamNum, matchNum):
        c = self.conn.cursor()
        c = c.execute("""
                        SELECT * FROM TeamInformations WHERE (TeamNumber = ? AND MatchNumber = ?)  
                    """, [teamNum, matchNum]).fetchall()
        return len(c) == 0

    def find_avg(self, teamNum):
        c = self.conn.cursor()
        c = c.execute("""
        SELECT TeamNumber, AVG(TeamInformations.autoLowGP),AVG(TeamInformations.autoMidGP),avg(TeamInformations.autoHighGP),avg(TeamInformations.teleopLowGP),avg(TeamInformations.teleopMidGP),avg(TeamInformations.teleopHighGP),avg(TeamInformations.teleopCons),avg(TeamInformations.teleopCubs)
        FROM TeamInformations
        GROUP BY TeamNumber
        HAVING TeamNumber = ?
        """, [teamNum]).fetchone()
        a = list()
        for i in c:
            a.append(i)
        c = self.conn.cursor()
        c = c.execute("""SELECT startSide,autoKindGP, autoClimb,teleopClimb
        FROM TeamInformations
        WHERE TeamNumber = ?
        """, [teamNum]).fetchall()
        b = list()
        for i in c:
            b.append(i)
        a.append(b)
        return a

    # need to add more functions for the graphs.
    def getGraphInfo1(self, teamNumber):
        c = self.conn.cursor()
        c = c.execute("""
        SELECT MatchNumber,autoLowGP,autoMidGP,autoHighGP
        FROM TeamInformations   
        WHERE TeamNumber = ?
        """, [teamNumber]).fetchall()
        return c

    def getGraphInfo2(self, teamNumber):
        c = self.conn.cursor()
        c = c.execute("""
        SELECT MatchNumber,teleopLowGP,teleopMidGp,teleopHighGP
        FROM TeamInformations
        WHERE TeamNumber = ?
        """, [teamNumber]).fetchall()
        return c

    def getGraphInfo3(self, teamNumber):
        c = self.conn.cursor()
        c = c.execute("""
        SELECT MatchNumber,teleopCons,teleopCubs
        FROM TeamInformations
        WHERE TeamNumber = ?
        """, [teamNumber]).fetchall()
        return c

    def getCompareData(self, teamNumber):
        c = self.conn.cursor()
        c = c.execute("""
        SELECT MatchNumber,autoLowGP+autoMidGP+autoHighGP,teleopLowGP+teleopMidGp+teleopHighGP
        FROM TeamInformations
        WHERE TeamNumber = ?
        """, [teamNumber]).fetchall()
        return c

    def getComments(self, teamNumber):
        c = self.conn.cursor()
        c = c.execute("""
        SELECT  MatchNumber, commentsIntake, commentsField, commentsClimb, commentsDefense, Comments
        FROM TeamInformations
        WHERE TeamNumber = ?
        """, [teamNumber]).fetchall()
        return c
