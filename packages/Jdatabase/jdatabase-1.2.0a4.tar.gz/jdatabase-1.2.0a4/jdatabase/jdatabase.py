import MySQLdb
import psycopg2
from itertools import repeat
import random, string  # random string gen
import datetime


class JdatabaseConnection:
    """
    this class is mainly for the Jdatabase class and can be ignored if you are using the wrapper (Jdatabase class)
    however, it can be used as an easy connection former if you do not want to use the wrapper (Jdatabase class)
    """

    # conf, kwargs store
    __conf = None
    # connection object
    conn = None
    # cursor object
    cur = None
    # the type of database, not really used at this time
    type = None
    # type reference, mainly for error printing use
    __type_reference = {0: None, 1: "MySQL", 2: "PostgreSQL", }
    # set the types to their methods
    __type_methods = {1: "mysql_connect", 2: "postgresql_connect"}
    # set the default ports
    __type_default_ports = {1: 3306, 2: 5432}
    # the connection error, defaults to True changes to error on connection error
    errors = []

    def __init__(self, **kwargs):
        """
        sets the __conf args and establishes a connection with the database with the connect method

        :param kwargs: host, user, passwd, db, charset, port, ssl, autocommit
        """
        # TODO check for row

        self.__conf = kwargs

        # charset to use for reading the data, defaults utf8 and will not need to be changed in most situations
        self.__conf["charset"] = kwargs.get("charset", "utf8")
        # the port to use when connecting to the database, defaults to None, and will be changed to
        # the default port for each connection type unless a port is specified
        self.__conf["port"] = kwargs.get("port", None)
        # whether or not ssl is used, defaults True for encrypted connections
        self.__conf["ssl"] = kwargs.get("ssl", True)
        # autocommit changes to the database, defaults to True to autocommit
        self.__conf["autocommit"] = kwargs.get("autocommit", True)

        # connect to the database
        self.connect()

    def connect(self):
        # reset the error value for reconnect attempts
        self.errors = []
        # check type for reconnect attempts
        if self.type is None or self.type == 0:
            # try connecting to each type until type is found and connected to
            for _type in self.__type_methods:
                if self.type is None or self.type == 0:
                    try:
                        if self.__conf["port"] is None:
                            # if no port is input into the objects instantiation use the default per the connection type
                            self.__conf["port"] = self.__type_default_ports[_type]
                        if getattr(self, self.__type_methods[_type])():
                            self.type = _type
                    except Exception as e:
                        self.errors.append(f"{self.__type_reference[_type]}: {e}")
            if self.type is None or self.type == 0:
                # if connection fails each time return errors
                print("Connection errors in JdatabaseConnection connect method:")
                for error in self.errors:
                    print(f"====== \n{error} \n======")
                return self.errors
        else:
            # connect based on known type
            getattr(self, self.__type_methods[self.type])()
        # set the cursor object
        self.cur = self.conn.cursor()
        # set the autocommit status
        self.conn.autocommit(self.__conf["autocommit"])

    def mysql_connect(self):
        """
        runs connection to a MySQL database through MySQLdb
        MySQLdb documentation: http://mysql-python.sourceforge.net/MySQLdb.html
        :return: True on connect
        """
        self.conn = MySQLdb.connect(host=self.__conf["host"],
                                    user=self.__conf["user"],
                                    passwd=self.__conf["passwd"],
                                    db=self.__conf["db"],
                                    charset=self.__conf["charset"],
                                    port=self.__conf["port"],
                                    ssl=self.__conf["ssl"])
        return True

    def postgresql_connect(self):
        """
        runs connection to a PostgreSQL database through psycopg2
        psycopg2 documentation: https://pypi.org/project/psycopg2/
        :return: True on connect
        """
        self.conn = psycopg2.connect(host=self.__conf["host"],
                                     database=self.__conf["db"],
                                     user=self.__conf["user"],
                                     password=self.__conf["passwd"],
                                     port=self.__conf["port"])
        return True


class Jdatabase:
    """
    this class acts as a SQL wrapper
    after instantiation of this class, the object acts as the primary tool for interacting with the connected database
    """

    # conf, kwargs store
    __conf = None
    # jdc, the JdatabaseConnection object that stores connection data and the connection
    jdc = None
    # the names of all the tables in the database
    table_names = None
    # the names of all the system tables in the database
    system_table_names = None

    def __init__(self, **kwargs):
        """
        sets the __conf args and establishes a connection with the JdatabaseConnection object

        :param kwargs: host, user, passwd, db, charset, port, ssl, autocommit, track, log, log_level
        """
        self.__conf = kwargs
        # whether get queries for data are returned as a list or dict. requires tracking TODO
        self.__conf["return_type"] = kwargs.get("return_type", "list")
        # whether or not to track the database's tables created through the jdatabase object, defaults False to not TODO
        self.__conf["track"] = kwargs.get("track", False)
        # table names that are currently being tracked
        self.__tracked_tables = []
        # log the database changes using the logger module, defaults to False to not TODO
        self.__conf["log"] = kwargs.get("log", False)
        # the log level to log if log is set to True, defaults to info level TODO
        self.__conf["log_level"] = kwargs.get("log_level", "info")

        # set up jdc object
        self.jdc = JdatabaseConnection(host=self.__conf["host"],
                                       user=self.__conf["user"],
                                       passwd=self.__conf["passwd"],
                                       db=self.__conf["db"],
                                       charset=kwargs.get("charset"),
                                       port=kwargs.get("port"),
                                       ssl=kwargs.get("ssl"),
                                       autocommit=kwargs.get("autocommit"))

        # create info table if not already created
        # self.__check_for_and_create_info_table() TODO

    """ TABLE NAMES METHODS """
    def __get_table_names_processor(self, schema=None, schema_equals=True, type=None, type_equals=True):
        """
        takes in schema and type arguments and forms the sql query for getting table names
        returns a list of table names returned from a call to 'self.__get_table_names_data' with the formed query

        :param schema: the argument to put in for 'TABLE_SCHEMA' in the sql query
        :param schema_equals: defaults to 'True', input 'False' for '<>' instead of '='
        :param type: the argument to put in for 'TABLE_TYPE' in the sql query
        :param type_equals: defaults to 'True', input 'False' for '<>' instead of '='
        :return: call to 'self.__get_table_names_data' with the formed query
        """

        def __get_table_names_data(selt, sql):
            """
            executes an sql query that returns the names of tables from information_schema.tables based on the query
            then processes and returns the names as a list

            :param sql: sql query
            :return: list of table names
            """
            selt.query(sql)
            data = selt.jdc.cur.fetchall()
            try:
                # try to split the data after removing the extra end
                data = list((str(data).replace("(('", "").replace("',))", "")).split("',), ('"))
            except Exception as error:
                print("jdatabse module __get_table_names_data error")
                print(error)
                data = data
            return data

        sql = "SELECT table_name FROM information_schema.tables"
        sql += " WHERE" if schema is not None or type is not None else ""
        sql += " TABLE_SCHEMA %s '%s'" % ("=" if schema_equals else "<>", schema) if schema is not None else ""
        sql += " and" if schema is not None and type is not None else ""
        sql += " TABLE_TYPE %s '%s'" % ("=" if type_equals else "<>", type) if type is not None else ""
        return __get_table_names_data(self, sql)

    def get_table_names(self):
        """
        gets the names of all of the tables in the connected database

        :return: list of table names
        """
        # table names are updated based on a query every time this method is called unlike the system table names
        self.table_names = self.__get_table_names_processor(schema=self.__conf['db'], type="SYSTEM VIEW", type_equals=False)
        return self.table_names

    def get_system_table_names(self):
        """
        gets the names of all of the system tables in the connected database server

        :return: list of table names
        """
        if self.system_table_names is not None:
            # if system tables have already been loaded return them
            return self.system_table_names
        self.system_table_names = self.__get_table_names_processor(schema="information_schema", type="SYSTEM VIEW")
        return self.system_table_names

    def get_all_table_names(self):
        """
        gets the names of all of the tables in the connected database and all system tables in the connected database
        server

        :return: list of table names
        """
        return self.get_table_names() + self.get_system_table_names()
    """ END TABLE NAMES METHODS """

    """ DATABASE METHODS """
    def create_database(self, database):
        """
        creates a database in the database server

        :param database: the name of the database to create
        :return: query rowcount
        """
        sql = "CREATE DATABASE %s" % database
        return self.query(sql).rowcount

    def drop_database(self, database):
        """
        drops a database from the database server

        :param database: the name of the database to drop
        :return: query rowcount
        """
        sql = "DROP DATABASE %s" % database
        return self.query(sql).rowcount
    """ END DATABASE METHODS """

    """ TABLE METHODS """
    def check_for_table(self, table):
        """
        checks if a table exists in the connected database

        :param table: the name of the table to look for
        :return: True if the table exists in the connected database
        :return: False if the table does not exist in the connected database
        """
        if table in self.get_all_table_names():
            return True
        return False

    def create_table(self, table, columns):
        """
        creates a table in the database with the params given

        :param table: the name of the table
        :param columns: the columns to create in the table
        :return: query rowcount
        """
        # track
        if self.__conf["track"] and str(table) != "jdatabase_info":
            self.__add_info(table, columns)
        sql = "CREATE TABLE %s (%s)" % (table, self.__serialize_columns(columns))
        return self.query(sql).rowcount

    def create_table_if_not_exists(self, table, columns):
        """
        creates a table in the database with the parms given using IF NOT EXISTS as an sql argument

        :param table: the name of the table
        :param columns: the columns to create in the table
        :return: query rowcount
        """
        sql = "CREATE TABLE IF NOT EXISTS %s (%s)" % (table, self.__serialize_columns(columns))
        rowcount = self.query(sql).rowcount
        # track, if rowcount is 0
        if self.__conf["track"] and str(rowcount) == "0" and str(table) != "jdatabase_info":
            self.__add_info(table, columns)
        return rowcount

    def create_table_if_false_check(self, table, columns):
        """
        creates a table in the database with the parms given if it is not found with the check_for_table method

        :param table: the name of the table
        :param columns: the columns to create in the table
        :return: query rowcount, None if table exists
        """
        if not self.check_for_table(table):
            # track
            if self.__conf["track"] and str(table) != "jdatabase_info":
                self.__add_info(table, columns)
            sql = "CREATE TABLE %s (%s)" % (table, self.__serialize_columns(columns))
            return self.query(sql).rowcount
        else:
            return None

    def drop_table(self, table):
        """
        drops a table from the database

        :param table: the name of the table
        :return: query rowcount
        """
        sql = "DROP TABLE %s" % (table)
        return self.query(sql).rowcount
    """ END TABLE METHODS """

    """ DATA METHODS """
    def get_type_returner(self, table, data_list):
        if self.__conf["track"] and table in self.__tracked_tables and self.__conf["return_type"].lower() == "dict":
            # TODO get column list from tracking table and return it with the data_list data
            return data_list
        return data_list

    def get_one(self, table, fields="*", where=None, order=None):
        """
        gets one row of data from the database

        :param table: the name of the table to get the data from
        :param fields: the column names to get, '*' for all
        :param where: where condition
        :param order: order condition
        :return: row of data
        """
        if not self.is_connected():  # if not connected / error connecting return error
            return self.jdc.errors
        try:
            row = (self.__select(table, fields, where, order)).fetchone()
            return row if row else None
        except TypeError:  # row not found
            return None
        except Exception:
            raise

    def get_all(self, table, fields='*', where=None, order=None):
        """
        gets all rows of data from the database

        :param table: the name of the table to get the data from
        :param fields: the column names to get, '*' for all
        :param where: where condition
        :param order: order condition
        :return: rows of data
        """
        if not self.is_connected():  # if not connected / error connecting return error
            return self.jdc.errors
        try:
            data = (self.__select(table, fields, where, order)).fetchall()
            return data if data else None
        except TypeError:  # data not found
            return None
        except Exception:
            raise

    def insert(self, table, data):
        query = self.__serialize_insert(data)
        sql = "INSERT INTO %s (%s) VALUES(%s)" % (table, query[0], query[1])
        return self.query(sql, data.values()).rowcount

    def insert_batch(self, table, data):
        query = self.__serialize_batch_insert(data)
        sql = "INSERT INTO %s (%s) VALUES %s" % (table, query[0], query[1])
        vals = [v for sublist in data for k, v in sublist.items()]
        return self.query(sql, vals).rowcount

    def update(self, table, data, where=None):
        query = self.__serialize_update(data)
        sql = "UPDATE %s SET %s" % (table, query)
        if where and len(where) > 0:
            sql += " WHERE %s" % where[0]
        return self.query(sql, list(data.values()) + where[1] if where and len(where) > 1 else data.values()).rowcount

    def insert_or_update(self, table, data, keys=["jd"]):
        insert_data = data.copy()
        data = {k: data[k] for k in data if k not in keys}
        insert = self.__serialize_insert(insert_data)
        update = self.__serialize_update(data)
        sql = "INSERT INTO %s (%s) VALUES(%s) ON DUPLICATE KEY UPDATE %s" % (table, insert[0], insert[1], update)
        return self.query(sql, list(insert_data.values()) + list(data.values())).rowcount

    def delete(self, table, where=None):
        sql = "DELETE FROM %s" % table
        if where and len(where) > 0:
            sql += " WHERE %s" % where[0]
        return self.query(sql, where[1] if where and len(where) > 1 else None).rowcount

    def last_id(self):
        return self.jdc.cur.lastrowid

    def last_query(self):
        # try to get cur statement
        try:
            return self.jdc.cur.statement
        # attribute error, get cur last executed
        except AttributeError:
            return self.jdc.cur._last_executed
    """ END DATA METHODS """

    """ CLASS METHODS """
    def is_open(self):
        try:
            return self.jdc.conn.open
        except:
            return False

    def is_connected(self):
        if not self.is_open():
            self.jdc.connect()
        return self.jdc.errors

    def query(self, sql, parms=None):
        try:
            self.jdc.cur.execute(sql, parms)
        except (Exception, MySQLdb.DatabaseError) as error:
            try:
                if error[0] == 2006 or error[0] == 2013:
                    self.jdc.connect()
                    self.jdc.cur.execute(sql, parms)
                else:
                    raise
            except TypeError:
                self.jdc.connect()
                self.jdc.cur.execute(sql, parms)
        return self.jdc.cur

    def commit(self):
        return self.jdc.conn.commit()

    def close(self):
        try:
            self.jdc.cur.close()
            self.jdc.conn.close()
            return True
        except (Exception, MySQLdb.DatabaseError) as error:
            return error

    def reconnect(self):
        self.close()
        self.database_type = self.jdc.connect()
        return True
    """ END CLASS METHODS """

    """ RESTRICTED METHODS """
    def __str__(self):
        return str(self.__conf["db"])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __select(self, table=None, fields=(), where=None, order=None):
        sql = "SELECT %s FROM %s" % (",".join(fields), table)
        if where and len(where) > 0:
            sql += " WHERE %s" % where[0]
        if order:
            sql += " ORDER BY %s" % order[0]
            if len(order) > 1:
                sql += " %s" % order[1]
        return self.query(sql, where[1] if where and len(where) > 1 else None)

    def __serialize_insert(self, data):
        keys = ",".join(data.keys())
        vals = ",".join(["%s" for k in data])
        return [keys, vals]

    def __serialize_batch_insert(self, data):
        keys = ",".join(data[0].keys())
        v = "(%s)" % ",".join(tuple("%s".rstrip(',') for v in range(len(data[0]))))
        l = ','.join(list(repeat(v, len(data))))
        return [keys, l]

    def __serialize_update(self, data):
        return "=%s,".join(data.keys()) + "=%s"

    def __serialize_columns(self, data):
        if len(data) > 1:
            return ", ".join(f"{column} {data[column][0]} {data[column][1]}" for column in data)
        else:
            return ", ".join(f"{column} {data[column]}" for column in data)

    # method to add dict2 to dict1, does not add duplicates
    def __add_dicts(self, dict1, dict2):
        for item in dict2:
            if item not in dict1:
                dict1[item] = dict2[item]
        return dict1

    # method to add dict2 to dict1, and update duplicates
    def __add_and_update_dicts(self, dict1, dict2):
        for item in dict2:
            dict1[item] = dict2[item]
        return dict1

    # method to generate a random string with length length
    def __random_string_gen(self, length):
        return "".join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
            range(length))
    """ END RESTRICTED METHODS """

    """ INFO TABLE """
    def __check_and_create_info_table(self):
        structure = {
            "table_name": ["VARCHAR(256)", "PRIMARY KEY"],
            "columns": ["TEXT(0)", "NOT NULL"],
            "creation_datetime": ["DATETIME(0)", "NOT NULL"],
        }
        self.create_table_if_false_check("jdatabase_info", structure)

    def __add_info(self, table_name, columns):
        self.insert_or_update("jdatabase_info", {"table_name": str(table_name),
                                                 "columns": str(columns),
                                                 "creation_datetime": datetime.datetime.utcnow()})
    """ END INFO TABLE """
