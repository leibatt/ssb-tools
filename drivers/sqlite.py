import os
import json
import sqlite3
import datetime, time
import itertools
import util
import queue
from queue import Empty
import threading
from threading import Thread
import logging

import sqlite3
import datetime, time
import itertools
import util

logger = logging.getLogger("ssb")
class SSBDriver:
    def init(self, options):
        self.isRunning = False
        self.requests = queue.Queue() #fifo
        self.config = json.load(open(os.path.join(os.path.dirname(__file__),'..','sqlite.config.json')))

    def create_connection(self):
        sqlite_file = self.config['dbFilename']
        conn = sqlite3.connect(sqlite_file)
        return conn

    def sqlitefix(self, sql_statement):
        if not "FLOOR" in sql_statement:
            return sql_statement
        else:
            sql_statement=sql_statement.replace("FLOOR", "ROUND")
            x=sql_statement.find("ROUND")
            y=sql_statement.find(")",x)
            output=sql_statement[:y]+" -0.5 "+sql_statement[y:]
            #print(output,flush=True)
            return output

    def execute_query(self, query):
        # get a connection from the pool - block if non is available
        sql_statement = query
        #logger.info("(%s) %s" % (request.ssb_id,sql_statement))
        connection = self.conn
        cursor = connection.cursor()
        cursor.execute(self.sqlitefix(sql_statement))
        data = cursor.fetchall()

        # put connection back in the queue so the next thread can use it.
        cursor.close()
        self.pool.put(connection)

        results = []
        for row in data:
            results.append(row)
        return results

    def execute_request(self, request, result_queue, options):
        # get a connection from the pool - block if non is available
        sql_statement = request.sql_statement
        #logger.info("(%s) %s" % (request.ssb_id,sql_statement))
        connection = self.conn
        cursor = connection.cursor()
        request.start_time = util.get_current_ms_time()
        cursor.execute(self.sqlitefix(sql_statement))
        data = cursor.fetchall()
        request.end_time = util.get_current_ms_time()

        # put connection back in the queue so the next thread can use it.
        cursor.close()

        results = []
        for row in data:
            results.append(row)
        request.result = results
        result_queue.put(request)

    def process_request(self, request, result_queue, options):
        self.requests.put((request, result_queue, options))

    def process(self):
        self.conn = self.create_connection()
        while self.isRunning:
            try:
                requestObject = self.requests.get(timeout=1)
                request = requestObject[0]
                result_queue = requestObject[1]
                options = requestObject[2]

                # only execute requests that are newer than the last one we processed (drops old/no longer needed queries)
                self.execute_request(request, result_queue, options)
            except Empty:
                # ignore queue-empty exceptions
                pass
            except Exception as e:
                logger.error("exception occurred")
                logger.error(e)
                raise
        # close connection when done
        self.conn.close()
        return

    def workflow_start(self):
        self.isRunning = True
        thread = Thread(target = self.process)
        thread.start()

    def workflow_end(self):
        self.isRunning = False
