
from sqlalchemy import create_engine, text

DATABASE_URL = ""

class DB:
    def __init__(self, dbName = "", dbUser = "", dbPassword = "", dbHost = "", dbPort = "", dbURL = ""):
        self.db_name = dbName
        self.db_user = dbUser
        self.db_password = dbPassword
        self.db_host = dbHost
        self.db_port = dbPort
        engine = create_engine(DATABASE_URL)
        self.conn = engine.connect()

    def commit(self):
        self.conn.commit()

    def deleteTable(self, table):
        tableDelete = text(f"DROP TABLE IF EXISTS {table}")
        self.conn.execute(tableDelete)
        DB.commit(self)
    
    def createPrereqsTable(self, table = "prereqs"):
        createCoursesTable = text(f"""
                                  CREATE TABLE IF NOT EXISTS {table} (
                                  id SERIAL PRIMARY KEY,
                                  subject TEXT NOT NULL,
                                  code TEXT NOT NULL,
                                  prereq JSONB NOT NULL
                                  );
                                  """)
        self.conn.execute(createCoursesTable)
        DB.commit(self)

    def createInternalTable(self, table = "internal"):
        createInternalTable = text(f"""
                                   CREATE TABLE IF NOT EXISTS {table} (
                                   id SERIAL PRIMARY KEY,
                                   name TEXT NOT NULL,
                                   data TEXT[] NOT NULL
                                   );
                                   """)
        self.conn.execute(createInternalTable)
        DB.commit(self)
    
    def insertInternalData(self, name, data, table = "internal"):
        ## Check data is TEXT[] !!!!!
        insertInternal = text(f"""
                              INSERT INTO {table} (name, data)
                              VALUES (:name, :data)
                              """)
        
        self.conn.execute(insertInternal, {
            "name": name,
            "data": data
        })
        DB.commit(self)
    
    def deleteInternalData(self, name, table = "internal"):
        deleteInternalRow = text(f"DELETE FROM {table} WHERE name = :name")
        self.conn.execute(deleteInternalRow, {"name": name})
        DB.commit(self)

    def checkInternalDataExist(self, name, table = "internal"):
        checkInternalDataExist = text(f"SELECT * FROM {table} WHERE name = :name")

        return self.conn.execute(checkInternalDataExist, {"name": name}).fetchone()
