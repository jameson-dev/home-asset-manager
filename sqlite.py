import os.path
import sqlite3
from loguru import logger

DB_FILE = 'assets.db'

CREATE_TYPES_TABLE = '''
                CREATE TABLE IF NOT EXISTS types (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL
                )
            '''

CREATE_MODELS_TABLE = '''
                CREATE TABLE IF NOT EXISTS models (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    type_id INTEGER NOT NULL,
                    FOREIGN KEY (type_id) REFERENCES types (id)
                    )
                '''

CREATE_ASSETS_TABLE = '''
                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY,
                    asset_number INTEGER UNIQUE NOT NULL,
                    type_id INTEGER NOT NULL,
                    model_id INTEGER NOT NULL,
                    location_id INTEGER  NOT NULL,
                    serial_number TEXT NOT NULL,
                    ip_address TEXT,
                    purchase_date DATE,
                    warranty_exp DATE,
                    notes TEXT,
                    FOREIGN KEY (location_id) REFERENCES locations (id),
                    FOREIGN KEY (type_id) REFERENCES types (id),
                    FOREIGN KEY (model_id) REFERENCES models (id)
                    )
                '''

CREATE_LOCATIONS_TABLE = '''
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL
                )
                '''


def connect_db():
    """Create connection to SQLite database"""
    return sqlite3.connect(DB_FILE)


def fetch_data():
    """Retrieve all current data from database """
    logger.info(f"Fetching data..")
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM assets")
        data = c.fetchall()

    logger.info(f"Fetched {len(data)} records.")
    return data


def load_db():
    """Create database & tables if they don't exist.
    Otherwise, connect to the existing database."""
    logger.info("Loading database...")
    if not os.path.isfile(DB_FILE):
        logger.info(f"Database not found. creating it now...")
        try:
            with connect_db() as conn:
                c = conn.cursor()
                c.execute(CREATE_ASSETS_TABLE)
                c.execute(CREATE_LOCATIONS_TABLE)
                c.execute(CREATE_TYPES_TABLE)
                c.execute(CREATE_MODELS_TABLE)
                logger.info(f"Database and tables created.")
        except sqlite3.Error as e:
            logger.error(f"Error loading SQLite database: {e}")
    else:
        logger.info(f"Database found.")


def add_location(name):
    """Add a new location to the database"""
    with connect_db() as conn:
        c = conn.cursor()
        try:
            c.execute('INSERT INTO locations (name) VALUES (?)', (name,))
            conn.commit()
            logger.info(f"Location '{name}' added.")
        except sqlite3.IntegrityError:
            logger.error(f"Location '{name}' already exists.")


def add_type(name):
    """Add a new device type to the database"""
    with connect_db() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO types (name) VALUES (?)", (name,))
            conn.commit()
            logger.info(f"Device type '{name}' added.")
        except sqlite3.IntegrityError as e:
            logger.error(f"Device type '{name}' already exists")


def add_model(name, type_id):
    """Add a new device model to the database"""
    with connect_db() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO models (name) VALUES (?, ?)", (name, type_id))
            conn.commit()
            logger.info(f"Device model '{name}' under Type ID {type_id} has been added to the database.")
        except sqlite3.IntegrityError as e:
            logger.error(f"Device model '{name}' already exists or Type ID {type_id} is invalid")

