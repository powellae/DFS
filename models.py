#Import packages
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, DateTime

#Establish Tables
Base = declarative_base()
class Teams(Base):
    __tablename__ = 'Teams'

    TeamId = Column(Integer, Sequence('TeamId_seq'), primary_key=True)
    TeamName = Column(String)
    LeagueId = Column(Integer)
    StadiumId = Column(Integer)

    def __repr__(self):
        return "<Team(name='%s')>" % (self.TeamName)

class Games(Base):
    __tablename__ = 'Games'

    GameId = Column(Integer, Sequence('GameId_seq'), primary_key=True)
    HomeTeamId = Column(Integer)
    AwayTeamId = Column(Integer)
    HomeTeamScore = Column(Integer)
    AwayTeamScore = Column(Integer)
    GameStatusId = Column(String)
    GameTypeId = Column(String)
    GameDate = Column(DateTime)
    GameLink = Column(String)

    def __repr__(self):
        return "<Game(%s at %s)" % (self.HomeTeamId, self.AwayTeamId)
