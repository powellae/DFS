import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import sessionmaker
from models import Teams, Games
import numpy as np

class DL_Game:
    def __init__(self, session, hometeamid, hometeamscore, awayteamid, awayteamscore, gamestatus, gametype, gamedate, link):
        self.HomeTeamId = hometeamid
        self.HomeTeamScore = hometeamscore
        self.AwayTeamId = awayteamid
        self.AwayTeamScore = awayteamscore
        self.GameStatusId = str(gamestatus)
        self.GameTypeId = str(gametype)
        self.GameDate = gamedate
        self.GameLink = link
        self.Session = session

    def CheckGameExists(self, link):
        game = self.Session.query(Games).filter(Games.GameLink==link).first()
        if hasattr(game, 'GameId'):
            self.Exists = 1
        else:
            self.Exists = 0

    def AddNewGame(self):
        game_new = Games(HomeTeamId=self.HomeTeamId, HomeTeamScore=self.HomeTeamScore,
                            AwayTeamId=self.AwayTeamId, AwayTeamScore=self.AwayTeamScore,
                            GameStatusId=self.GameStatusId, GameTypeId=self.GameTypeId,
                            GameDate=self.GameDate, GameLink=self.GameLink)
        self.game_new = game_new

    def UploadGame(self):
        self.CheckGameExists(self.GameLink)
        if not self.Exists:
            self.Session.add(self.game_new)
