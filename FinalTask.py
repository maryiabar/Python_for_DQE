import math
import pyodbc

class DatabaseManager:
    def __init__(self):
        # connection to DB
        self.connection = pyodbc.connect(
            'DRIVER={SQLite3 ODBC Driver};'
            'Direct=True;'
            'Database=cities.db;'
            'String Types=Unicode'
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # creating table to store city coordinates
        self.cursor.execute('''create table if not exists Coordinates (
                               id integer primary key autoincrement,
                               city text not null,
                               latitude real, 
                               longitude real,
                               unique(lower(city), latitude, longitude))
                               ''')
        self.connection.commit()

    def close(self):
        # close cursor and connection
        self.cursor.close()
        self.connection.close()


class DistanceCalculator:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def record_exists(self, table, conditions, params):
        # check if city record already exists
        query = f"select 1 from {table} where {conditions}"
        self.db_manager.cursor.execute(query, params)
        return self.db_manager.cursor.fetchone() is not None

    def get_city_coordinates(self, city):
        # select data from the table
        self.db_manager.cursor.execute("select latitude, longitude from Coordinates where lower(city) = lower(?)", (city,))
        result = self.db_manager.cursor.fetchone()
        if result:
            return result[0], result[1]
        else:
            return None

    def add_city_coordinates(self, city, latitude, longitude):
        # insert new data to the table
        if not self.record_exists("Coordinates", "city = ? ", (city,)):
            self.db_manager.cursor.execute('''insert into Coordinates (city, latitude, longitude)
                                  values(?, ?, ?)''', (city, latitude, longitude))
            self.db_manager.connection.commit()
            print("City coordinates successfully added.")

    def request_coordinates(self, city):
        # asking for city coordinates if it not stores in the table
        print(f"Coordinates for {city} are not found in the database.")
        latitude: float = float(input(f"Please enter the latitude for {city}: "))
        longitude: float = float(input(f"Please enter the longitude for {city}: "))
        self.add_city_coordinates(city, latitude, longitude)
        return latitude, longitude

    def calculate_distance(self, city1_coordinates, city2_coordinates):
        # calculate distance using Haversine formula
        earth_radius_km = 6378.0
        lat1, lon1 = map(math.radians, city1_coordinates)
        lat2, lon2 = map(math.radians, city2_coordinates)

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return earth_radius_km * c

    def get_distance_between_cities(self):
        # getting city names for calculating distance
        city1 = input("Enter the first city name: ").strip()
        city2 = input("Enter the second city name: ").strip()

        city1_coordinates = self.get_city_coordinates(city1)
        if city1_coordinates is None:
            city1_coordinates = self.request_coordinates(city1)
        city2_coordinates = self.get_city_coordinates(city2)
        if city2_coordinates is None:
            city2_coordinates = self.request_coordinates(city2)
        distance = self.calculate_distance(city1_coordinates, city2_coordinates)
        print(f"The distance between {city1} and {city2} is {distance:.2f} km.")


if __name__ == "__main__":
    db_manager = DatabaseManager()
    distance_calculator = DistanceCalculator(db_manager)
    print("Main Menu:\n1 - Add New Record\n2 - Calculate Distance Between Cities")
    choice = input("Enter your choice: ")
    if choice == "1":
        # add new city data to the table
        city = input("Please add city name: ").strip()
        latitude = float(input("Please add latitude: "))
        longitude = float(input("Please add longitude: "))
        distance_calculator.add_city_coordinates(city, latitude, longitude)
    elif choice == "2":
        # calculate distance
        distance_calculator.get_distance_between_cities()
    else:
        print("Invalid choice, please try again.")

    db_manager.close()