from DTO import Alliance


class Alliances:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, alliance):
        self.conn.execute("""
        INSERT INTO Alliances (TeamNumber,MatchNumber,Alliance) VALUES (?,?,?)
        """, [alliance.teamNumber, alliance.matchNumber, alliance.alliance])

    def findRed(self, matchNum):
        return self.findTeams(matchNum, "Red")

    def findBlue(self, matchNum):
        return self.findTeams(matchNum,"Blue")

    def findTeams(self,matchNum,alliance):
        c = self.conn.cursor()
        c = c.execute("""
                        SELECT TeamNumber FROM Alliances WHERE (Alliance = ? AND MatchNumber = ?)  
                    """, [alliance, matchNum]).fetchall()
        return c
