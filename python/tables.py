"""
@author: Aidan Hazzard

This module contains classes to represent final tables of the steamgames database. In practice it acts similarly to an ORM such as SQLAlchemy, where each table is a class that keeps track of its members and each element of a table is an object of the
same class. The exception to this are intersection tables, where each member of the class is itself a table. If any entry has unsupported values (such as too long names), then the entry should be rejected with a ValueError
"""
from abc import ABC, abstractmethod

LONG_STRING_LIMIT = 2048 # Same as the limitations in the MySQL Database

class SimpleTable(ABC):
    """
    Base abstract class for all tables except for intersection tables. Each class that inherits SimpleTable represents a table and each member of that class is a row in the table.

    Attributes:
        id:int -> MySQL primary index, 1 indexed
        name:str -> Name of the table element, eg Title of a game or Name of a Developer

    Methods:
        to_sql_insert(self): str -> Converts a member of a class that inherits SimpleTable into a SQL insert statement
    """
    def __init__(self, name, id, name_char_limit = 32):
        """
        Inititalizes a member of a SimpleTable. Raises ValueError if length of name is greater than name_char_limit.

        Parameters:
            name:str -> Name of the table element, eg Title of a game or Name of a Developer
            id:int -> MySQL primary index, 1 indexed
            name_char_limit:int -> Maximum allowable length of the name parameter

        Returns:
            None
        """
        if (len(name) > name_char_limit):
            print(f"{name} not added to table, title is greater than {name_char_limit} characters long")
            raise ValueError

        self.id = id
        self.name = name.replace('"', '\\"') # Strings in the SQL inserts with use double quotes, so we want to escape any double quotes that are in the data

    # All tables should have a way to convert their entries to SQL
    @abstractmethod
    def to_sql_insert(self) -> str:
        """
        Converts self into an SQL insert statement
        """
        pass


class Game(SimpleTable):
    """
    Class that represents the Game table of the steamgames db, each member of the class represents a row
    of the table

    Class Variables:
        game_list: dict -> Class wide dictionary to store each member of the class keyed by app_id

    Attributes:
        id: int -> MySQL primary index
        name: str -> Title of the game
        app_id: int -> Steam app_id of the game
        release_date: str -> Release date of the game
        achieve_count: int -> Number of achievements the game has
        in_eng: bool -> Indicates whether the game is in english
        positives: int -> Number of positive ratings of the game
        negatives: int -> Number of negative ratings of the game
        ave_play_time: int -> Average play time of the game
        med_play_time: int -> Median play time of the game
        owner_low: int -> Lower bound of owners of the game
        owner_high: int -> Upper bound of owners of the game
        price: float -> Price of the game
        desc: str -> Description of the game
        min_reqs: str -> The game's minimum system requirements
        rec_reqs: str -> The game's recommended system requirements

    Methods:
        to_sql_insert(self): str ->  Converts a member of a class into a SQL insert statement
    """
    game_list = {}

    def __init__(self, app_id, title, release_date = None, achieve_count = 0, 
                 in_eng = False, positives = 0, negatives = 0, ave_play_time = None, 
                 med_play_time = None, owner_low = None, owner_high = None, price = 0.00, 
                 desc = "", min_reqs = "", rec_reqs = ""):
        """
        Initializes an instance of the Game class and adds it to the game_list class variable keyed by app_id

        Parameters:
            app_id: int -> Steam app_id of the game
            title: str -> Title of the game
            release_date: str -> Release date of the game
            achieve_count: int -> Number of achievements the game has
            in_eng: bool -> Indicates whether the game is in english
            positives: int -> Number of positive ratings of the game
            negatives: int -> Number of negative ratings of the game
            ave_play_time: int -> Average play time of the game
            med_play_time: int -> Median play time of the game
            owner_low: int -> Lower bound of owners of the game
            owner_high: int -> Upper bound of owners of the game
            price: float -> Price of the game
            desc: str -> Description of the game
            min_reqs: str -> The game's minimum system requirements
            rec_reqs: str -> The game's recommended system requirements

        Returns:
            None

        Raises:
            ValueError on invalid data
        """

        # Check for valid data, return the errors
        if (app_id in Game.game_list):
            print(f"{title} already exists in game list, game with appid:{app_id} not added")
            raise ValueError
        
        if (len(desc) > 1024):
            print(f"{title} not added, description is greater than 1024 characters long")
            raise ValueError
        
        if (len(min_reqs) > LONG_STRING_LIMIT):
            print(f"{title} not added, Minimum Requirements is greater than {LONG_STRING_LIMIT} characters long")
            raise ValueError
        
        if (len(rec_reqs) > 1024):
            print(f"{title} not added, Recommended Requirements is greater than 1024 characters long")
            raise ValueError
        
        # MySQL IDs are 1 indexed
        super().__init__(title, len(Game.game_list)+1, 64)
        self.app_id = app_id
        self.release_date = release_date
        self.achieve_count = achieve_count 
        self.in_eng = in_eng
        self.positives = positives
        self.negatives = negatives
        self.ave_play_time = ave_play_time
        self.med_play_time = med_play_time
        self.owner_low = owner_low
        self.owner_high = owner_high
        self.price = price
        # Strings in the SQL inserts with use double quotes, so we want to escape any double quotes that are in the data
        self.desc = desc.replace('"', '\\"')
        self.min_reqs = min_reqs.replace('"', '\\"')
        self.rec_reqs = rec_reqs.replace('"', '\\"')

        Game.game_list[app_id] = self

    def to_sql_insert(self) -> str:
        """
        Converts self into an SQL insert statement

        Returns:
            str -> SQL insert statement
        """
        return f"INSERT INTO Game(ID,SteamAppID,Title,ReleaseDate,AchievementCount,InEnglish,PositiveRatingCount,NegativeRatingCount,AvePlayTime,MedPlayTime,OwnerCountLowerBound,OwnerCountUpperBound,Price,Description,MinimumRequirements,RecommendedRequirements) VALUES({self.id},{self.app_id},\"{self.name}\",\"{self.release_date}\",{self.achieve_count},{self.in_eng},{self.positives},{self.negatives},{self.ave_play_time},{self.med_play_time},{self.owner_low},{self.owner_high},{self.price},\"{self.desc}\",\"{self.min_reqs}\",\"{self.rec_reqs}\");"
    

class DeveloperTable(SimpleTable):
    """
    Class that represents the Developer table of the steamgames db, each member of the class represents a row
    of the table

    Class Variables:
        table: array -> Class wide array to store each member of the class

    Attributes:
        id: int -> MySQL primary index
        name: str -> Name of the Developer

    Methods:
        to_sql_insert(self): str ->  Converts a member of a class into a SQL insert statement

    Class Methods:
        __contains__(cls, str): bool -> Returns whether str is in the table
        def index(cls, str): int -> Returns the index of str in the table if it exists, raises value error otherwise
    """
    table = []
    def __init__(self, name):
        """
        Initializes an instance of the developer class and appends it to the table class variable

        Parameters:
            name: str -> Name of the developer

        Returns:
            None

        Raises:
            ValueError on invalid data
        """
        id = len(DeveloperTable.table) + 1
        super().__init__(name, id)
        DeveloperTable.table.append(self)
    
    def to_sql_insert(self):
        """
        Converts self into an SQL insert statement

        Returns:
            str -> SQL insert statement
        """
        return f"INSERT INTO Developer(ID, Name) VALUES({self.id},\"{self.name}\");"
    
    @classmethod
    def __contains__(cls, str):
        """
        Returns whether the given string a name of an element in the table
        
        Parameters:
            str: str -> Name of rating to find existence of
        
        Returns:
            bool -> Returns True if str is the name of an element in the table, False otherwise
        """
        # This method doesn't work like a magic method as intended, have to call it directly. Should change to another method name
        for e in cls.table:
            # Compare lowercase values to be case-insensitive
            if e.name.lower() == str.lower():
                return True
        return False
    
    @classmethod
    def index(cls, str):
        """
        Returns the index of the developer with the same name as the given string in the table. Raises a ValueError if str is not a name of an element of the table
        
        Parameters:
            str: str -> Name of developer to search for index
        
        Returns:
            int -> Index of str in the table
            
        Raises:
            ValueError if str is not found in the table
        """
        for i in range(len(cls.table)):
            if cls.table[i].name.lower() == str.lower():
                return i
        raise ValueError


class PublisherTable(SimpleTable):
    """
    Class that represents the Publisher table of the steamgames db, each member of the class represents a row
    of the table

    Class Variables:
        table: array -> Class wide array to store each member of the class

    Attributes:
        id: int -> MySQL primary index
        name: str -> Name of the Publisher

    Methods:
        to_sql_insert(self): str ->  Converts a member of a class into a SQL insert statement

    Class Methods:
        __contains__(cls, str): bool -> Returns whether str is in the table
        def index(cls, str): int -> Returns the index of str in the table if it exists, raises value error otherwise
    """
    table = []
    def __init__(self, name):
        """
        Initializes an instance of the publisher class and appends it to the table class variable

        Parameters:
            name: str -> Name of the publisher

        Returns:
            None

        Raises:
            ValueError on invalid data
        """
        id = len(PublisherTable.table) + 1
        super().__init__(name, id)
        PublisherTable.table.append(self)
    
    def to_sql_insert(self):
        """
        Converts self into an SQL insert statement

        Returns:
            str -> SQL insert statement
        """
        return f"INSERT INTO Publisher(ID, Name) VALUES({self.id},\"{self.name}\");"
    
    @classmethod
    def __contains__(cls, str: str):
        """
        Returns whether the given string a name of an element in the table
        
        Parameters:
            str: str -> Name of rating to find existence of
        
        Returns:
            bool -> Returns True if str is the name of an element in the table, False otherwise
        """
        for e in cls.table:
            if e.name.lower() == str.lower():
                return True
        return False
    
    @classmethod
    def index(cls, str):
        """
        Returns the index of the publisher with the same name as the given string in the table. Raises a ValueError if str is not a name of an element of the table
        
        Parameters:
            str: str -> Name of publisher to search for index
        
        Returns:
            int -> Index of str in the table
            
        Raises:
            ValueError if str is not found in the table
        """
        for i in range(len(cls.table)):
            if cls.table[i].name.lower() == str.lower():
                return i
        raise ValueError


class RatingTable(SimpleTable):
    """
    Class that represents the Rating table of the steamgames db, each member of the class represents a row
    of the table

    Class Variables:
        table: array -> Class wide array to store each member of the class

    Attributes:
        id: int -> MySQL primary index
        name: str -> Name of the rating

    Methods:
        to_sql_insert(self): str ->  Converts a member of a class into a SQL insert statement

    Class Methods:
        __contains__(cls, str): bool -> Returns whether str is in the table
        def index(cls, str): int -> Returns the index of str in the table if it exists, raises value error otherwise
    """
    table = []
    def __init__(self, name):
        """
        Initializes an instance of the rating class and appends it to the table class variable

        Parameters:
            name: str -> Name of the rating

        Returns:
            None

        Raises:
            ValueError on invalid data
        """
        id = len(RatingTable.table) + 1
        super().__init__(name, id, 16)
        RatingTable.table.append(self)
    
    def to_sql_insert(self):
        """
        Converts self into an SQL insert statement

        Returns:
            str -> SQL insert statement
        """
        # Currently the spreadsheet only has ratings in PEGI, but this class could be amended to handle other game rating system
        return f"INSERT INTO Rating(ID, Name, RatingSystem) VALUES({self.id},'{self.name}','PEGI');"
    
    @classmethod
    def __contains__(cls, str):
        """
        Returns whether the given string a name of an element in the table
        
        Parameters:
            str: str -> Name of rating to find existence of
        
        Returns:
            bool -> Returns True if str is the name of an element in the table, False otherwise
        """
        for e in cls.table:
            if e.name.lower() == str.lower():
                return True
        return False
    
    @classmethod
    def index(cls, str):
        """
        Returns the index of the rating with the same name as the given string in the table. Raises a ValueError if str is not a name of an element of the table
        
        Parameters:
            str: str -> Name of rating to search for index
        
        Returns:
            int -> Index of str in the table
            
        Raises:
            ValueError if str is not found in the table
        """
        for i in range(len(cls.table)):
            if cls.table[i].name.lower() == str.lower():
                return i
        raise ValueError


class PlatformTable(SimpleTable):
    """
    Class that represents the Platform table of the steamgames db, each member of the class represents a row
    of the table

    Class Variables:
        table: array -> Class wide array to store each member of the class

    Attributes:
        id: int -> MySQL primary index
        name: str -> Name of the platform

    Methods:
        to_sql_insert(self): str ->  Converts a member of a class into a SQL insert statement

    Class Methods:
        __contains__(cls, str): bool -> Returns whether str is in the table
        def index(cls, str): int -> Returns the index of str in the table if it exists, raises value error otherwise
    """
    table = []
    def __init__(self, name):
        """
        Initializes an instance of the platform class and appends it to the table class variable

        Parameters:
            name: str -> Name of the platform

        Returns:
            None

        Raises:
            ValueError on invalid data
        """
        id = len(PlatformTable.table) + 1
        super().__init__(name, id, 16)
        PlatformTable.table.append(self)
    
    def to_sql_insert(self):
        """
        Converts self into an SQL insert statement

        Returns:
            str -> SQL insert statement
        """
        return f"INSERT INTO Platform(ID, Name) VALUES({self.id},'{self.name}');"
    
    @classmethod
    def __contains__(cls, str):
        """
        Returns whether the given string a name of an element in the table
        
        Parameters:
            str: str -> Name of rating to find existence of
        
        Returns:
            bool -> Returns True if str is the name of an element in the table, False otherwise
        """
        for e in cls.table:
            if e.name.lower() == str.lower():
                return True
        return False
    
    @classmethod
    def index(cls, str):
        """
        Returns the index of the platform with the same name as the given string in the table. Raises a ValueError if str is not a name of an element of the table
        
        Parameters:
            str: str -> Name of platform to search for index
        
        Returns:
            int -> Index of str in the table
            
        Raises:
            ValueError if str is not found in the table
        """
        for i in range(len(cls.table)):
            if cls.table[i].name.lower() == str.lower():
                return i
        raise ValueError


class CategoryTable(SimpleTable):
    """
    Class that represents the Category table of the steamgames db, each member of the class represents a row
    of the table

    Class Variables:
        table: array -> Class wide array to store each member of the class

    Attributes:
        id: int -> MySQL primary index
        name: str -> Name of the category

    Methods:
        to_sql_insert(self): str ->  Converts a member of a class into a SQL insert statement

    Class Methods:
        __contains__(cls, str): bool -> Returns whether str is in the table
        def index(cls, str): int -> Returns the index of str in the table if it exists, raises value error otherwise
    """
    table = []
    def __init__(self, name):
        """
        Initializes an instance of the category class and appends it to the table class variable

        Parameters:
            name: str -> Name of the category

        Returns:
            None

        Raises:
            ValueError on invalid data
        """
        id = len(CategoryTable.table) + 1
        super().__init__(name, id)
        CategoryTable.table.append(self)
    
    def to_sql_insert(self):
        """
        Converts self into an SQL insert statement

        Returns:
            str -> SQL insert statement
        """
        return f"INSERT INTO Category(ID, Name) VALUES({self.id},'{self.name}');"
    
    @classmethod
    def __contains__(cls, str):
        """
        Returns whether the given string a name of an element in the table
        
        Parameters:
            str: str -> Name of category to find existence of
        
        Returns:
            bool -> Returns True if str is the name of an element in the table, False otherwise
        """
        for e in cls.table:
            if e.name.lower() == str.lower():
                return True
        return False
    
    @classmethod
    def index(cls, str):
        """
        Returns the index of the category with the same name as the given string in the table. Raises a ValueError if str is not a name of an element of the table
        
        Parameters:
            str: str -> Name of category to search for index
        
        Returns:
            int -> Index of str in the table
            
        Raises:
            ValueError if str is not found in the table
        """
        for i in range(len(cls.table)):
            if cls.table[i].name.lower() == str.lower():
                return i
        raise ValueError


class GenreTable(SimpleTable):
    """
    Class that represents the Genre table of the steamgames db, each member of the class represents a row
    of the table

    Class Variables:
        table: array -> Class wide array to store each member of the class

    Attributes:
        id: int -> MySQL primary index
        name: str -> Name of the genre

    Methods:
        to_sql_insert(self): str ->  Converts a member of a class into a SQL insert statement

    Class Methods:
        __contains__(cls, str): bool -> Returns whether str is in the table
        def index(cls, str): int -> Returns the index of str in the table if it exists, raises value error otherwise
    """
    table = []
    def __init__(self, name):
        """
        Initializes an instance of the genre class and appends it to the table class variable

        Parameters:
            name: str -> Name of the genre

        Returns:
            None

        Raises:
            ValueError on invalid data
        """
        id = len(GenreTable.table) + 1
        super().__init__(name, id)
        GenreTable.table.append(self)
    
    def to_sql_insert(self):
        """
        Converts self into an SQL insert statement

        Returns:
            str -> SQL insert statement
        """
        return f"INSERT INTO Genre(ID, Name) VALUES({self.id}, '{self.name}');"
    
    @classmethod
    def __contains__(cls, str):
        """
        Returns whether the given string a name of an element in the table
        
        Parameters:
            str: str -> Name of genre to find existence of
        
        Returns:
            bool -> Returns True if str is the name of an element in the table, False otherwise
        """
        for e in cls.table:
            if e.name.lower() == str.lower():
                return True
        return False
    
    @classmethod
    def index(cls, str):
        """
        Returns the index of the genre with the same name as the given string in the table. Raises a ValueError if str is not a name of an element of the table
        
        Parameters:
            str: str -> Name of genre to search for index
        
        Returns:
            int -> Index of str in the table
            
        Raises:
            ValueError if str is not found in the table
        """
        for i in range(len(cls.table)):
            if cls.table[i].name.lower() == str.lower():
                return i
        raise ValueError
    
    
class IntersectionTable():
    """
    Represents an intersection table of the steamgames db.
    
    Attributes:
        _table: dict -> Dictionary containing the elements of the table keyed by pairs of ids from the 
        left table and the right table. The value saved is normally 1, but for the GameTags table it represents
        the number of times the game was tagged by that genre
        
        left_key: str -> Name of the left_table's id
        right_key: str -> Name of the right_table's id
        name: str -> Name of the table, which is the combination of the left_table and right_table's and in plural
    
    Methods:
        add_entry(self, left_id, right_id, count=1) -> Adds a value, count, to the table keyed by (left_id, right_id)
        to_sql_insert(self, include_val=False) -> Converts a IntersectionTable's contents into SQL Insert statements
    """
    def __init__(self, left_table: str, right_table: str) -> None:
        """
        Inititalizes an IntersectionTable
        
        Parameters:
            left_table: str -> Name of the left table
            right_table: str -> Name of the right table
        
        Returns:
            None
        """
        self._table = {}
        self.left_key = left_table + 'ID'
        self.right_key = right_table + 'ID'

        # Replacing 'y' with 'ies' for plural works most of the time, English isn't that simple however. But It does work here
        if right_table[-1] == 'y':
            self.name = left_table + right_table[:-1] + "ies"
        else:
            self.name = left_table + right_table + 's'

    def add_entry(self, left_id, right_id, count=1):
        """
        Adds a value, count, to the table keyed by (left_id, right_id)
        
        Parameters:
            left_id: int -> id of left table element
            right_id: int -> id of right table element
            count: int -> number of times a game was tagged, only used for the GameTags table. Set to 1 otherwise\
        
        Returns:
            None
        
        Raises:
            ValueError if (left_id, right_id) is already in the table
        """
        # If the entry is already in the table we shouldn't add it, this should never happen in practice
        if (left_id,right_id) in self._table:
            print(f"{left_id}, {right_id} not inserted into the {self.name} table because the keys were already in the table")
            raise ValueError
        self._table[(left_id,right_id)] = count

    def to_sql_insert(self, include_val=False):
        """
        Converts a IntersectionTable's contents into SQL Insert statements

        Parameters:
            include_val: bool -> Determines whether the value save in the table should be included in the insert statement.
            Only set to True for the GameTags table
        
        Returns:
            str -> String containing all SQL insert statements for the IntersectionTable
        """
        tag_count = ''
        tag_num = ''
        name = self.name
        sql_string = ''
        # This is a hacky way to add more data to the single intersection table that needs it, (the GameTags table)
        if include_val:
            tag_count=", TagCount"
            name="GameTags"
        for key in self._table:
            if include_val:
                tag_num = f",{self._table[key]}"
            sql_string += f"INSERT INTO {name}({self.left_key}, {self.right_key}{tag_count}) VALUES({key[0]},{key[1]}{tag_num});\n"
        
        return sql_string