import os

import MySQLdb as mysql


class DBHub:
    '''The interface between user and DB where store the data'''
    def __init__(self, db_name):
        self.db_name = db_name
        self.data_info = {}
        # if the db_name database not exist, create one
        db = mysql.connect(host='localhost', user='root', passwd='1234')
        cursor = db.cursor()
        cmd_str = 'show databases;'
        cursor.execute(cmd_str)
        db_list = cursor.fetchall()
        db_list = self.tuple_process(db_list)
        if db_name not in db_list:
            cmd_str = 'CREATE DATABASE {} default charset utf8 collate utf8_general_ci;'.format(db_name)
            cursor.execute(cmd_str)
        cursor.close()
        db.close()

    def store_data(self, file_path, file_name):
        '''Store the data from raw data file to database'''
        file_name_cleaned = file_name.replace("-", "_").split(".")[0]
        self.DB_table_name = file_name_cleaned
        self.data_info[file_name_cleaned] = {}
        with open(os.path.join(file_path, file_name), 'r') as f:
            # Obtain the variable name from first row of the raw data file
            head_list = f.readline().replace("-", "_").split()
            self.data_info[file_name_cleaned].update(head=head_list)
            # head_str is a single string used for create columns in DB table and insert data to DB
            head_str = ','.join(head_list)
            self.data_info[file_name_cleaned].update(head_str=head_str)
            # DB_table_name is the name of table in DB, using the cleaned file name without the postfix
            DB_table_name = file_name_cleaned
            self.data_info[file_name_cleaned].update(DB_table_name=DB_table_name)

            # read the second row(first data row) and get the time string, then check time format
            init_time_str = f.readline().split()[0]
            time_format = self.check_time_format(init_time_str)
            self.data_info[file_name_cleaned].update(time_format=time_format)
            self.data_info[file_name_cleaned].update(init_time_str=init_time_str)

            # Create DB and table using file name and variable names
            # TODO create DB
            db, cursor = self.connect_db(self.db_name)
            # create db table with variable names as column names
            cmd_list_part = ["{} float".format(i_var) for i_var in head_list]
            if time_format == 'time_string':
                cmd_list_part[0] = cmd_list_part[0].replace('float', 'varchar(20)')
                cmd_list_part.append('Time_added float')
                head_str += ', Time_added'
            cmd_str_part = ','.join(cmd_list_part)
            cmd_str = "CREATE TABLE IF NOT EXISTS {} ({});".format(DB_table_name, cmd_str_part)
            # execute the command
            cursor.execute(cmd_str)

        # Insert data to DB
        with open(os.path.join(file_path, file_name), 'r') as f:
            # skip the head line
            _ = f.readline()
            while True:
                data_line = f.readline()
                if data_line:
                    data_line = data_line.split()
                    # if time format is like XX:XX:XX:XXX, then add one column for the second time
                    if time_format == 'time_string':
                        data_line.append(self.time_delta(init_time_str, data_line[0]))
                        # make the time str to str when it is in sql cmd
                        data_line[0] = '"'+data_line[0]+'"'
                    data_line = ','.join(data_line)
                    cmd_str = "INSERT INTO {} ({}) VALUES ({})".format(DB_table_name, head_str, data_line)
                    cursor.execute(cmd_str)
                else:
                    break
            db.commit()
            # close the connection
            cursor.close()
            db.close()

    def check_time_format(self, time_str):
        '''Check the time format in raw data file, Beijing time format or just second'''
        if ':' in time_str:
            return 'time_string'
        else:
            return 'second'

    def time_delta(self, begin_time, end_time):
        '''calculate the delta seconds between two time string'''
        b_t = begin_time.split(':')
        e_t = end_time.split(':')
        for i,_ in enumerate(b_t):
            b_t[i] = int(b_t[i])
            e_t[i] = int(e_t[i])
        delta = (e_t[0] - b_t[0])*60*60 + (e_t[1] - b_t[1])*60 + (e_t[2] - b_t[2])*1 + (e_t[3] - b_t[3])*0.001
        return str(delta)

    def connect_db(self, db_name):
        '''Connect to the database.
        inner function'''
        db = mysql.connect(host='localhost', user='root', passwd='1234', db=db_name)
        cursor = db.cursor()
        print("Connect to database: {}".format(self.db_name))
        return db, cursor

    def create_table(self):
        '''Create the table in database according to the data file
        inner function'''
        pass

    def check_time_type(self):
        '''check the time format in the data file,
        in "second" format or "HH:MM:SS:mmm" format.
        Inner function'''
        pass


    def get_var_names(self):
        '''Get all variable names stored in database from all tables'''
        db, cursor = self.connect_db(self.db_name)
        cmd_str = 'SHOW TABLES;'
        cursor.execute(cmd_str)
        tables = cursor.fetchall()
        tables = self.tuple_process(tables)
        var_names = []
        for table in tables:
            cmd_str = 'DESCRIBE {};'.format(table)
            cursor.execute(cmd_str)
            var_info = cursor.fetchall()
            var_info = [x[0] for x in var_info]
            # TODO: too arguly, need optimize
            try:
                var_info.remove('TIME')
                var_info.remove('Time_added')
            except:
                pass
            var_names.extend(var_info)
        return var_names

    def get_var(self, var_name):
        '''Get tha data from database according to the variable name'''
        db, cursor = self.connect_db(self.db_name)
        # Get the table list from DB
        cmd_str = 'SHOW TABLES;'
        cursor.execute(cmd_str)
        tables = cursor.fetchall()
        tables = self.tuple_process(tables)
        data = []
        for table in tables:
            cmd_str = 'SELECT {} from {}'.format(var_name, table)
            try:
                cursor.execute(cmd_str)
            except:
                continue
            data = cursor.fetchall()
            break
        if data:
            data = self.tuple_process(data)
            return data
        return None

    def tuple_process(self, data_tuple):
        # transfer double layer tuple to one layer
        # ((1,),(2,),)  ->   (1, 2,)
        return tuple(map(lambda x: x[0], data_tuple))
