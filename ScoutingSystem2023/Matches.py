from DTO import Match


class Matches:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, match):
        self.conn.execute("""
                INSERT INTO Matches (GameNumber,Blue1,Blue2,Blue3,Red1,Red2,Red3) VALUES (?,?,?,?,?,?,?)
                """, [match.gameNumber, match.blue1, match.blue2, match.blue3, match.red1, match.red2, match.red3])

    def findTeams(self, matchNumber):
        c = self.conn.cursor()
        c = c.execute(""" SELECT* FROM Matches WHERE GameNumber =?   """, [matchNumber]).fetchone()
        return Match(*c)
