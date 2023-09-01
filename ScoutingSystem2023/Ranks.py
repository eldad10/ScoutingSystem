from DTO import Rank
def getClimbingDataAuto(climb):
    sum = 0
    for i in climb:
        if i == 'כן - מאוזן':
            sum += 12
        if i == 'כן - לא מאוזן':
            sum += 8
    return sum/len(climb)
def getClimbingDataTel(climb):
    sum = 0
    for i in climb:
        if i == 'כן - מאוזן':
            sum += 10
        if i == 'כן - לא מאוזן':
            sum += 6
    return sum/len(climb)



class Ranks:
    def __init__(self, conn):
        self.conn = conn

    def createRanks(self):
        c = self.conn.cursor()
        c = c.execute("""
                        select TeamNumber, avg(autoLowGP)*3 +avg(autoMidGP)*4 + avg(autoHighGP)*6 +avg(teleopLowGP)*2+avg(teleopMidGP)*3+avg(teleopHighGP)*5 as points,avg(autoLowGP)*3 +avg(autoMidGP)*4 + avg(autoHighGP)*6 as autoPoints,avg(teleopLowGP)*2+avg(teleopMidGP)*3+avg(teleopHighGP)*5 as teleopPoints
                        FROM TeamInformations
                        GROUP BY TeamNumber
                        ORDER BY points DESC
                        """).fetchall()
        c1 = c
        return c1

    def deleteAll(self):
        self.conn.execute("""
        DELETE FROM RANKER
        """)

    def findClimbData(self,teamNumber):
        c = self.conn.cursor()
        c = c.execute("""
        select TeamNumber,autoClimb,teleopClimb
        from TeamInformations
        WHERE TeamNumber = ?
        """,[teamNumber]).fetchall()
        auto = [i[1] for i in c]
        teleop = [i[2] for i in c]
        return (c[0][0],getClimbingDataAuto(auto),getClimbingDataTel(teleop))
