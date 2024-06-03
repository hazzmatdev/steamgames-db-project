/********************************************
*	CS 364 Final Project: Steam Games db	*
*	Aidan Hazzard							*
********************************************/

DROP SCHEMA IF EXISTS steamgames;
CREATE SCHEMA steamgames;
USE steamgames;


-- As all tables are many to many, table creation order doesn't matter as long as the intersection tables come afterwards
CREATE TABLE Game (
	ID							INT 			NOT NULL	AUTO_INCREMENT,
    SteamAppID					INT				NOT NULL,
    Title						VARCHAR(64) 	NOT NULL,
    ReleaseDate 				DATETIME,
    AchievementCount			INT				NOT NULL	DEFAULT 0,
    InEnglish					BOOL			NOT NULL	DEFAULT FALSE,
    PositiveRatingCount 		INT				NOT NULL 	DEFAULT 0,
    NegativeRatingCount 		INT				NOT NULL 	DEFAULT 0,
    AvePlayTime					INT				DEFAULT NULL,
    MedPlayTime					INT				DEFAULT NULL,
    OwnerCountLowerBound 		INT				DEFAULT NULL,
    OwnerCountUpperBound		INT				DEFAULT NULL,
    Price						DECIMAL(5,2) 	NOT NULL	DEFAULT 0.00,
    Description					VARCHAR(1024)	DEFAULT "",
    MinimumRequirements			VARCHAR(2048)	DEFAULT "",
    RecommendedRequirements		VARCHAR(1024)	DEFAULT "",
    
    PRIMARY KEY(ID),
    UNIQUE(SteamAppID)
);


CREATE TABLE Developer (
	ID				INT 		NOT NULL 	AUTO_INCREMENT,
    Name 			VARCHAR(32) NOT NULL,
    
    PRIMARY KEY(ID)
);


CREATE TABLE Publisher (
	ID				INT 		NOT NULL 	AUTO_INCREMENT,
    Name 			VARCHAR(32) NOT NULL,
    
    PRIMARY KEY(ID)
);


CREATE TABLE Rating (
	ID				INT			NOT NULL	AUTO_INCREMENT,
    Name 			VARCHAR(16)	NOT NULL,
    RatingSystem	VARCHAR(8) 	NOT NULL,
    
    PRIMARY KEY(ID),
    UNIQUE(Name, RatingSystem)
);


CREATE TABLE Platform (
	ID				INT			NOT NULL	AUTO_INCREMENT,
    Name			VARCHAR(16)	NOT NULL,
    
    PRIMARY KEY(ID),
    UNIQUE(Name)
);


CREATE TABLE Category (
	ID				INT			NOT NULL	AUTO_INCREMENT,
    Name			VARCHAR(32) NOT NULL,
    
    PRIMARY KEY(ID),
    UNIQUE(Name)
);


CREATE TABLE Genre (
	ID				INT			NOT NULL	AUTO_INCREMENT,
    Name			VARCHAR(32) NOT NULL,
    
    PRIMARY KEY(ID),
    UNIQUE(Name)
);


-- Intersection Tables
CREATE TABLE GameDevelopers (
	GameID		INT		NOT NULL,
    DeveloperID	INT		NOT NULL,
    
    PRIMARY KEY(GameID, DeveloperID),
    FOREIGN KEY(GameID) REFERENCES Game(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(DeveloperID) REFERENCES Developer(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE GamePublishers (
	GameID		INT		NOT NULL,
    PublisherID	INT		NOT NULL,
    
    PRIMARY KEY(GameID, PublisherID),
    FOREIGN KEY(GameID) REFERENCES Game(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(PublisherID) REFERENCES Publisher(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE GameRatings (
	GameID		INT		NOT NULL,
    RatingID	INT		NOT NULL,
    
    PRIMARY KEY(GameID, RatingID),
    FOREIGN KEY(GameID) REFERENCES Game(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(RatingID) REFERENCES Rating(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE GamePlatforms (
	GameID		INT		NOT NULL,
    PlatformID	INT		NOT NULL,
    
    PRIMARY KEY(GameID, PlatformID),
    FOREIGN KEY(GameID) REFERENCES Game(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(PlatformID) REFERENCES Platform(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE GameCategories (
	GameID		INT		NOT NULL,
    CategoryID	INT		NOT NULL,
    
    PRIMARY KEY(GameID, CategoryID),
    FOREIGN KEY(GameID) REFERENCES Game(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(CategoryID) REFERENCES Category(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE GameTags (
	GameID		INT		NOT NULL,
    GenreID		INT		NOT NULL,
    TagCount	INT		NOT NULL 	DEFAULT 1,
    
    PRIMARY KEY(GameID, GenreID),
    FOREIGN KEY(GameID) REFERENCES Game(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(GenreID) REFERENCES Genre(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE GameGenres (
	GameID		INT		NOT NULL,
    GenreID		INT		NOT NULL,
    
    PRIMARY KEY(GameID, GenreID),
    FOREIGN KEY(GameID) REFERENCES Game(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(GenreID) REFERENCES Genre(ID)
		ON DELETE CASCADE
        ON UPDATE CASCADE
);

    