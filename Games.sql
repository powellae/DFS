CREATE TABLE Games (
	GameId INT IDENTITY(1,1) NOT NULL,
	HomeTeamId INT NOT NULL,
	AwayTeamId INT NOT NULL,
	HomeTeamScore INT NULL,
	AwayTeamScore INT NULL,
	GameStatusId VARCHAR(1) NULL,
	GameTypeId VARCHAR(1) NULL,
	GameDate DATE NULL,
	GameLink VARCHAR(50) NULL,
	PRIMARY KEY (GameId)
)
