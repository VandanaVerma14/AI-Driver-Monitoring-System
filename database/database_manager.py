import sqlite3
from datetime import datetime



class DatabaseManager:

    def __init__(self):

        self.connection = sqlite3.connect(
            "database/driver_monitor.db"
        )

        self.cursor = self.connection.cursor()
        self.current_trip = 1

        self.create_tables()

    ####################################################

    def create_tables(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                trip_id INTEGER,

                timestamp TEXT,

                event TEXT,

                value TEXT
            )
            """
        )
        self.connection.commit()
    def start_new_trip(self):

        self.cursor.execute(
            """
            SELECT MAX(trip_id)
            FROM events
            """
        )

        result = self.cursor.fetchone()

        if result[0] is None:

            self.current_trip = 1

        else:

            self.current_trip = result[0] + 1

        

    ####################################################

    def log_event(
        self,
        event,
        value="",
    ):

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.cursor.execute(
            """
            INSERT INTO events(
                trip_id,
                timestamp,
                event,
                value
            )

            VALUES(
            ?, ?, ?, ?
            )
            """,
            (
                self.current_trip,
                current_time,
                event,
                value
            ),
)

        self.connection.commit()

    ####################################################

    def fetch_all_events(self):

        self.cursor.execute(
            """
            SELECT *
            FROM events
            ORDER BY id DESC
            """
        )

        return self.cursor.fetchall()

    ####################################################

    def close(self):

        self.connection.close()