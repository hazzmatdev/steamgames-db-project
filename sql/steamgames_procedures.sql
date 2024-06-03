/**********************************************************************************
* Final Project: Steam DB and SteamSpy                                            *
* View and Triggers                                                               *
*                                                                                 *
* Aidan Hazzard 2024                                                              *
*                                                                                 *
* This file contains script to create a view and 2 triggers, one on Game Update   *
* another for Game Insert                                                         *
***********************************************************************************/

USE steamgames; 

DROP VIEW IF EXISTS TagPopularityByYear;
CREATE VIEW TagPopularityByYear as
	SELECT genre.Name "SteamSpy Tag", year(game.ReleaseDate) Year, SUM(gametags.TagCount) "Times Tagged in Year", MAX(game.Title) "Game Most Tagged"
    FROM genre 
    JOIN gametags ON genre.ID = gametags.GenreID
    JOIN game ON game.ID = gametags.GameID
    GROUP BY year(game.ReleaseDate), genre.Name
    ORDER BY Year DESC, `Times Tagged in Year` DESC;
	
DROP TRIGGER IF EXISTS Game_INSERT;
DELIMITER //
CREATE TRIGGER Game_INSERT
BEFORE INSERT ON Game
	FOR EACH ROW
	BEGIN
		IF NEW.AchievementCount < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "AchievementCount cannot be negative";
		END IF;
        
		IF NEW.PositiveRatingCount < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "PositiveRatingCount cannot be negative";
		END IF;
        
		IF NEW.NegativeRatingCount < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "NegativeRatingCount cannot be negative";
		END IF;
        
		IF NEW.AvePlayTime < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "AvePlayTime cannot be negative";
		END IF;
        
		IF NEW.MedPlayTime < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "MedPlayTime cannot be negative";
		END IF;
        
		IF NEW.OwnerCountLowerBound < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "OwnerCountLowerBound cannot be negative";
		END IF;
        
		IF NEW.OwnerCountUpperBound < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "OwnerCountUpperBound cannot be negative";
		END IF;
        
		IF NEW.Price < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "Price cannot be negative";
		END IF;
        
        SET NEW.MinimumRequirements = REGEXP_REPLACE(NEW.MinimumRequirements, "[[:blank:]]{2,}", " ");
        SET NEW.RecommendedRequirements = REGEXP_REPLACE(NEW.RecommendedRequirements, "[[:blank:]]{2,}", " ");
    END;
//
DELIMITER ;
	
    
DROP TRIGGER IF EXISTS Game_UPDATE;
DELIMITER //
CREATE TRIGGER Game_UPDATE
BEFORE UPDATE ON Game
	FOR EACH ROW
	BEGIN
		IF NEW.AchievementCount < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "AchievementCount cannot be negative";
		END IF;
        
		IF NEW.PositiveRatingCount < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "PositiveRatingCount cannot be negative";
		END IF;
        
		IF NEW.NegativeRatingCount < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "NegativeRatingCount cannot be negative";
		END IF;
        
		IF NEW.AvePlayTime < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "AvePlayTime cannot be negative";
		END IF;
        
		IF NEW.MedPlayTime < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "MedPlayTime cannot be negative";
		END IF;
        
		IF NEW.OwnerCountLowerBound < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "OwnerCountLowerBound cannot be negative";
		END IF;
        
		IF NEW.OwnerCountUpperBound < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "OwnerCountUpperBound cannot be negative";
		END IF;
        
		IF NEW.Price < 0 THEN
			SIGNAL SQLSTATE "45000"
			SET MESSAGE_TEXT = "Price cannot be negative";
		END IF;
        
        SET NEW.MinimumRequirements = REGEXP_REPLACE(NEW.MinimumRequirements, "[[:blank:]]{2,}", " ");
        SET NEW.RecommendedRequirements = REGEXP_REPLACE(NEW.RecommendedRequirements, "[[:blank:]]{2,}", " ");
    END;
//
DELIMITER ;