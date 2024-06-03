"""
@author: Aidan Hazzard

This module contains highly specific functions to read and convert spreadsheet data of steam games into SQL insertion statements. The functions of this module always read spreadsheets in the folder above it and creates sql query files in
the same folder as itself. WARNING: This can make very large SQL query files that can cause MySQL to lag
"""

import csv
import tables

def read_and_convert_to_sql(num_of_entries: int = 100) -> None:
    """
    This function is a user friendly shell to call the two other functions that this module relies on.

    Reads steam game data from csvs titled steam.csv, steam_description_data.csv, and steam_requirements_data.csv
    located in the directory above, then converts the CSV data into SQL insertions and saves it to three files titled steamgames_load_game_data.sql,
    steamgames_load_aux_data.sql, and steamgames_load_intersection_data.sql. This function will overwrite files of the same name located in the directory

    Parameters:
    num_of_entries: int -> Number of rows to read from steam.csv, excluding the headers. -1 implies reading all available data

    Returns:
    None
    """
    _convert_data_to_SQL(_get_steam_data(num_of_entries))

def _get_steam_data(num_of_entries: int) -> dict:
    """
    Reads steam game data from csvs titled steam.csv, steam_description_data.csv, and steam_requirements_data.csv
    located in the directory above and saves the data into a dictionary using the steam app_id as keys.

    Parameters:
    num_of_entries: int -> Number of rows to read from steam.csv, excluding the headers. -1 implies reading all available data

    Returns:
    dict -> Dictionary of steam games gathered from the provided csv files, each game itself is a dictonary where each header from the csvs are keys
    """
    steam_csv_dict = {}
    headers = []

    # In some of the spreadsheets, we don't care about all of the data given. Instead of using headers, we'll copy the columns we want directly
    # if the csv's layout changes, update these constants to match
    SHORT_DESC_COL = 3
    APP_ID_COL = 0
    MIN_REQ_COL = 4
    REC_REQ_COL = 5

    # Create the initial data from steam csv
    with open('../steam.csv', errors='ignore') as c_file:
        reader = csv.reader(c_file, delimiter=',')
        lines = 0
        count = num_of_entries
        for row in reader:
            # first row of the csv contains the headers
            if lines == 0:
                headers = row
                lines += 1
            else:
                app_id = row[APP_ID_COL]
                steam_csv_dict[app_id] = {}
                for i in range(len(headers)):
                    steam_csv_dict[app_id][headers[i]] = row[i]
                count -= 1
                
                # Go until we hit the number of entries wanted, passing -1 as the num_of_entries parameter will cause this to read all entries
                if  count == 0:
                    break

    # Add description data
    with open('../steam_description_data.csv', errors='ignore') as c_file:
        reader = csv.reader(c_file, delimiter=',')
        lines = 0
        count = num_of_entries
        for row in reader:
            if lines == 0:
                # dont need the headers
                lines += 1
                continue
            else:
                # use the Steam APP_ID to link together the spreadsheets
                if row[APP_ID_COL] in steam_csv_dict:
                    steam_csv_dict[row[APP_ID_COL]]['description'] = row[SHORT_DESC_COL]
                    count -= 1
                    
            if count == 0:
                break

    # Add requirement data
    with open('../steam_requirements_data.csv', errors='ignore') as c_file:
        reader = csv.reader(c_file, delimiter=',')
        lines = 0
        count = num_of_entries

        for row in reader:
            if lines == 0:
                lines += 1
                continue
            else:
                if row[APP_ID_COL] in steam_csv_dict:
                    steam_csv_dict[row[APP_ID_COL]]['minimum'] = row[MIN_REQ_COL]
                    steam_csv_dict[row[APP_ID_COL]]['recommended'] = row[REC_REQ_COL]
                    count -= 1
                    
            if count == 0:
                break

    # Add steamspy tag data
    with open('../steamspy_tag_data.csv', errors='ignore') as c_file:
        reader = csv.reader(c_file, delimiter=',')
        lines = 0
        count = num_of_entries

        for row in reader:
            if lines == 0:
                lines += 1
                headers = row
                continue
            else:
                if row[APP_ID_COL] in steam_csv_dict:
                    steam_csv_dict[row[APP_ID_COL]]["tags"] = {}
                    for i in range(1, len(headers)):
                        if int(row[i]) > 0:
                            steam_csv_dict[row[APP_ID_COL]]['tags'][headers[i]] = row[i]
                    count -= 1
                    
            if count == 0:
                break

    return steam_csv_dict

def _convert_data_to_SQL(steam_csv_dict: dict) -> None:
    """
    Converts a dictionary of steamgames into a SQL file with insert statements for the steamgames database as described by steamgames_schema.sql

    Parameters:
    steam_csv_dict: dict -> Dictionary of steam games gathered from the provided csv files, each game itself is a dictonary where each header from the csvs are keys. Each entry
    of the dictionary must contain the following keys: 'name', 'release_date', 'achievements', 'english', 'positive_ratings', 'negative_ratings', 'average_playtime', 'median_playtime', 'owners', and 'price'

    Returns:
    None
    """

    # Instantiate the intersection tables
    gamedevs_table = tables.IntersectionTable("Game", "Developer")
    gamepubs_table = tables.IntersectionTable("Game", "Publisher")
    gameplat_table = tables.IntersectionTable("Game", "Platform")
    gameratings_table = tables.IntersectionTable("Game", "Rating")
    gamecategories_table = tables.IntersectionTable("Game", "Category")
    gamegenres_table = tables.IntersectionTable("Game", "Genre")
    gametags_table = tables.IntersectionTable("Game", "Genre")

    tables.Game.game_list = {}

    for app_id in steam_csv_dict:
        game = steam_csv_dict[app_id]
        # owners represents the lower and upper bounds of owners of the game, split into the 2 numbers to insert into the database
        owners = game['owners'].split('-')
        if 'description' not in game:
            game['description'] = ''
        if 'minimum' not in game:
            game['minimum'] = ''
        if 'recommended' not in game:
            game['recommended'] = ''

        # This has a bug, if any table after game rejects the entry, the entry will remain in prior tables without required relationships such as
        # "a game must have a developer"
        try:
            # These attribute headers should be set as constants
            new_game = tables.Game(
                int(app_id), 
                game['name'], 
                game['release_date'], 
                game['achievements'],
                bool(game['english']),
                int(game['positive_ratings']),
                int(game['negative_ratings']),
                int(game['average_playtime']),
                int(game['median_playtime']),
                int(owners[0]),
                int(owners[1]),
                float(game['price']),
                game['description'],
                game['minimum'],
                game['recommended']
            )

            # secondary delimiter should be variable
            # These following loops could be a single function to reduce code duplication
            developers = game['developer'].split(';')
            for dev in developers:
                if tables.DeveloperTable.__contains__(dev):
                    dev_id = tables.DeveloperTable.index(dev) + 1
                else:
                    new_dev = tables.DeveloperTable(dev)
                    dev_id = new_dev.id
                
                gamedevs_table.add_entry(new_game.id, dev_id)
            
            publishers = game['publisher'].split(';')
            for pub in publishers:
                if tables.PublisherTable.__contains__(pub):
                    pub_id = tables.PublisherTable.index(pub) + 1
                else:
                    new_pub = tables.PublisherTable(pub)
                    pub_id = new_pub.id
                
                gamepubs_table.add_entry(new_game.id, pub_id)
            
            platforms = game['platforms'].split(';')
            for plat in platforms:
                if tables.PlatformTable.__contains__(plat):
                    plat_id = tables.PlatformTable.index(plat) + 1
                else:
                    new_plat = tables.PlatformTable(plat)
                    plat_id = new_plat.id

                gameplat_table.add_entry(new_game.id, plat_id)

            rating = game['required_age']
            if tables.RatingTable.__contains__(rating):
                rating_id = tables.RatingTable.index(rating) + 1
            else:
                new_rating = tables.RatingTable(rating)
                rating_id = new_rating.id

            gameratings_table.add_entry(new_game.id, rating_id)

            categories = game['categories'].split(';')
            for cat in categories:
                if tables.CategoryTable.__contains__(cat):
                    cat_id = tables.CategoryTable.index(cat) + 1
                else:
                    new_cat = tables.CategoryTable(cat)
                    cat_id = new_cat.id

                gamecategories_table.add_entry(new_game.id, cat_id)

            genres = game['genres'].split(';')
            for genre in genres:
                if tables.GenreTable.__contains__(genre):
                    genre_id = tables.GenreTable.index(genre) + 1
                else:
                    new_genre = tables.GenreTable(genre)
                    genre_id = new_genre.id

                gamegenres_table.add_entry(new_game.id, genre_id)
            
            steamspy_tags = game['tags']
            for tag in steamspy_tags:
                if tables.GenreTable.__contains__(tag):
                    genre_id = tables.GenreTable.index(tag) + 1
                else:
                    new_genre = tables.GenreTable(tag)
                    genre_id = new_genre.id
                
                gametags_table.add_entry(new_game.id, genre_id, steamspy_tags[tag])
        except ValueError:
            # If theres any error with the data that causes it to not be able to be in the database, skip the entry
            continue
    
    # Create three different files to reduce amount that MySQL workbench lags when opening them up. These files can get large
    with open("steamgames_load_game_data.sql", "w") as f:
        f.write('USE steamgames;\n\n')
        for id in tables.Game.game_list:
            f.write(tables.Game.game_list[id].to_sql_insert() + '\n')

    with open("steamgames_load_aux_data.sql", "w") as f:
        f.write('USE steamgames;\n\n')
        for e in tables.DeveloperTable.table:
            f.write(e.to_sql_insert() + '\n')

        f.write('\n')

        for e in tables.PublisherTable.table:
            f.write(e.to_sql_insert() + '\n')

        f.write('\n')

        for e in tables.RatingTable.table:
            f.write(e.to_sql_insert() + '\n')
        
        f.write('\n')

        for e in tables.PlatformTable.table:
            f.write(e.to_sql_insert() + '\n')
        
        f.write('\n')

        for e in tables.CategoryTable.table:
            f.write(e.to_sql_insert() + '\n')
        
        f.write('\n')

        for e in tables.GenreTable.table:
            f.write(e.to_sql_insert() + '\n')
        
    with open("steamgames_load_intersection_data.sql", "w") as f:
        f.write('USE steamgames;\n\n')
        f.write(gamedevs_table.to_sql_insert())
        f.write(gamepubs_table.to_sql_insert())
        f.write(gameplat_table.to_sql_insert())
        f.write(gameratings_table.to_sql_insert())
        f.write(gamecategories_table.to_sql_insert())
        f.write(gamegenres_table.to_sql_insert())
        f.write(gametags_table.to_sql_insert(include_val=True))
            


            


        