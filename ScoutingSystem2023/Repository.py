import sqlite3
import sys

from Alliances import Alliances
from Matches import Matches
from TeamInformations import TeamInformations
from Ranks import Ranks


class Repository:
    def __init__(self):
        self.conn = sqlite3.connect("RoboActive.db")
        self.alliances = Alliances(self.conn)
        self.matches = Matches(self.conn)
        self.teamInformation = TeamInformations(self.conn)
        self.ranks = Ranks(self.conn)

    def close(self):
        self.conn.commit()
        self.conn.close()

    def creatTables(self):
        self.conn.executescript("""
                CREATE TABLE IF NOT EXISTS Matches (
                GameNumber INT PRIMARY KEY,
                Blue1 INT,
                Blue2 INT,
                Blue3 INT,
                Red1 INT,
                Red2 INT,
                Red3 INT
                );
                CREATE TABLE IF NOT EXISTS Alliances(
                TeamNumber INT,
                MatchNumber INT,
                Alliance TEXT,
                PRIMARY KEY(TeamNumber,MatchNumber)
                );
                CREATE TABLE IF NOT EXISTS TeamInformations(
                TeamNumber INT,
                MatchNumber INT,
                Name TEXT,
                startSide TEXT,
                autoLowGP INT,
                autoMidGP INT,
                autoHighGP INT,
                autoKindGP TEXT,
                autoClimb TEXT,
                teleopLowGP INT,
                teleopMidGp INT,
                teleopHighGP INT,
                teleopCons INT,
                teleopCubs INT,
                takenFrom TEXT,
                teleopClimb TEXT,
                commentsIntake TEXT,
                commentsField TEXT,
                commentsDefense TEXT,
                commentsClimb TEXT,
                Comments TEXT,
                PRIMARY KEY(TeamNumber,MatchNumber)
                );  
                CREATE TABLE IF NOT EXISTS Ranker(
                TeamNumber INT,
                points INT,
                autoPoints INT,
                teleopPoints INT,
                autoClimb INT,
                teleopClimb INT,
                PRIMARY KEY(TeamNumber)
                );             
                """)
