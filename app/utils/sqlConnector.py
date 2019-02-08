import sqlite3
import os
from .configuration import Configuration
from typing import Dict, Tuple

config = Configuration.get_config()
logger = Configuration.get_logger()
database_name = config.songs_path


class TableObj:
    def __init__(self, table_name: str, columns: Dict[str, str], foreign_keys: Dict[str, Tuple[str, str]] = None):
        self.table_name = table_name
        self.columns = columns
        self.foreign_keys = foreign_keys


class SqlClient:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        logger.info('Openning connection to the database')
        self.connection = sqlite3.connect(config.songs_path)
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def clear_database(self):
        try:
            os.remove(database_name)
        except:
            pass

    def execute_script(self, sql):
        logger.info(f'Executing {sql}')
        c = self.connection.cursor()
        try:
            c.executescript(sql)
            return c.fetchall()
        finally:
            c.close()

    def execute_sql(self, sql):
        logger.info(f'Executing {sql}')
        c = self.connection.cursor()
        try:
            c.execute(sql)
            return c.fetchall()
        finally:
            c.close()

    def create_table(self, table_obj: TableObj):
        columns = ", ".join([f"{column} {table_obj.columns[column]}" for column in table_obj.columns])
        keys = table_obj.foreign_keys
        if keys is not None:
            foreign_keys = ',' + ', '.join(
                [f"FOREIGN KEY({key}) REFERENCES {keys[key][0]}({keys[key][1]})" for key in keys])
        else:
            foreign_keys = ''
        sql = f"""CREATE TABLE IF NOT EXISTS {table_obj.table_name} ({columns} {foreign_keys}) """
        self.execute_sql(sql)
