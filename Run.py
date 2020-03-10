#Import packages
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import datetime as dt
import pymssql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import sessionmaker
from models import Teams, Games
from downloader import DL_Game

#Set up database engine
engine = sqlalchemy.create_engine('mssql+pymssql://petewitty@sycamore1500:1723MarceeL@ne@sycamore1500.database.windows.net/DFS_GOLD')
engine.connect()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

def FindTeamId(teamname):
    team = session.query(Teams).filter(Teams.TeamName==str(teamname)).first()
    return(team.TeamId)

def GetTeamName(html, iswinner):
    if iswinner == 1:
        team = 'winner'
    else:
        team = 'loser'
    club = html.find('tr', {'class': team})
    club_name = str(club.findAll('a')[0]).split('>')[1][:-3]
    club_score = str(club.find('td', {'class': 'right'})).split('>')[1][:-4]
    ishome = len(club.findAll('td', {'class': 'right gamelink'}))
    return(club_name, club_score, ishome)

def CheckDate(link, month, day, year):
    if link[0:8] == '/allstar':
        return(0)
    valid_link = link[14:-7]
    valid_link_year = valid_link[0:4]
    valid_link_month = valid_link[4:6]
    valid_link_day = valid_link[6:8]

    if (int(valid_link_year) == year) & (int(valid_link_month) == month) & (int(valid_link_day) == day):
        return(1)
    else:
        return(0)

def GetGameDayData(month, day, year):
    url = "https://www.baseball-reference.com/boxes/?month=" + str(month) + "&day=" + str(day) + "&year=" + str(year)

    page = urlopen(url)
    soup = bs(page, "lxml")

    games = soup.findAll('div', {'class': 'game_summary nohover'})

    for game in games:
        gamelink = game.find('td', {'class': 'right gamelink'})
        link = str(gamelink.find('a')).split('"')[1]

        if CheckDate(link, month, day, year):
            if len(game.findAll('tr', {'class': 'date'})) > 0:
                playoffs = 1
            else:
                playoffs = 0

            winner = GetTeamName(game, 1)
            loser = GetTeamName(game, 0)

            if winner[2]:
                hometeamname = winner[0]
                hometeamscore = winner[1]
                hometeamid = FindTeamId(hometeamname)
                awayteamname = loser[0]
                awayteamscore = loser[1]
                awayteamid = FindTeamId(awayteamname)
            else:
                hometeamname = loser[0]
                hometeamscore = loser[1]
                hometeamid = FindTeamId(hometeamname)
                awayteamname = winner[0]
                awayteamscore = winner[1]
                awayteamid = FindTeamId(awayteamname)

            gamestatus = np.where((int(hometeamscore)+int(awayteamscore))>0,'P','S')
            playoffgame = np.where(playoffs>0,'Y','S')
            gamedate = str(year) + '-' + str(month) + '-' + str(day)

            dg = DL_Game(session=session, hometeamid=hometeamid, hometeamscore=hometeamscore, awayteamid=awayteamid, awayteamscore=awayteamscore, gamestatus=gamestatus,
                         gametype=playoffgame, gamedate=gamedate, link=link)
            dg.AddNewGame()
            dg.UploadGame()

    if len(session.new) > 0:
        print(str(month)+'-'+str(day)+'-'+str(year)+':', str(len(session.new))+' Games')
        session.commit()
    else:
        print(str(month)+'-'+str(day)+'-'+str(year)+':', 'No Games To Upload')


GetGameDayData(7,14,2018)
