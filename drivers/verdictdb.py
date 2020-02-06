import json
import datetime, time
import itertools
import pyverdict
import decimal
import os
import multiprocessing
from multiprocessing import Queue
import util
import pandas as pd
import numpy as np
import queue
from queue import Empty
import threading
from threading import Thread
import logging

logger = logging.getLogger("ssb")
class SSBDriver:

    def init(self, options):
        self.isRunning = False
        self.requests = queue.Queue()
        self.config = json.load(open(os.path.join(os.path.dirname(__file__),'..','verdictdb.config.json')))

    def verdictdbedit(self, sql_statement):
        sql_statement=sql_statement.replace('from lineorder','from public.lineorder_scrambled_'+str(self.config["scramblePercent"])+'_percent')
        sql_statement=sql_statement.replace(', lineorder,',', public.lineorder_scrambled_'+str(self.config["scramblePercent"])+'_percent,')
        sql_statement=sql_statement.replace(', lineorder ',', public.lineorder_scrambled_'+str(self.config["scramblePercent"])+'_percent ')
        logger.info("SQL: '%s'" % (sql_statement))
        return sql_statement.lower()

    def create_connection(self):
        connection = pyverdict.postgres(host=self.config['host'], user=self.config['username'], password=self.config['password'], port=self.config['port'], dbname=self.config['database-name'])
        connection.set_loglevel("ERROR")
        return connection

    def execute_query(self, query):
        # get a connection from the pool - block if non is available
        sql_statement = query
        #logger.info("(%s) %s" % (request.ssb_id,sql_statement))
        connection = self.conn
        editedSqlStatement = self.verdictdbedit(sql_statement)
        data = connection.sql(editedSqlStatement)

        #results = []
        #for row in data.iterrows():
        #    results.append(row)
        results = json.loads(data.to_json(orient="records"))
        return results

    def execute_request(self, request, result_queue, options):
        sql_statement = request.sql_statement

        # get a connection from the pool - block if non is available
        # connection = self.pool.get()
        connection=self.conn

        request.start_time = util.get_current_ms_time()
        data = None
        try:
            editedSqlStatement = self.verdictdbedit(sql_statement)
            data = connection.sql(editedSqlStatement)
        except Exception as e:
            print(e, flush=True)
            request.result = {}
            request.verdictdb_query = sql_statement
            request.end_time = util.get_current_ms_time()
            result_queue.put(request)
            return
        request.end_time = util.get_current_ms_time()

        #results = []
        #for row in data.iterrows():
        #  results.append(row)
        results = json.loads(data.to_json(orient="records"))
        print(editedSqlStatement)
        print(results)
        request.result = results
        request.verdictdb_query = sql_statement
        result_queue.put(request)

    def process_request(self, request, result_queue, options):
        self.requests.put((request, result_queue, options))

    def process(self):
        # while the workflow is running, pop the latest request from the stack and execute it
        while self.isRunning:
            try:
                requestObject = self.requests.get(timeout=1)
                request = requestObject[0]
                result_queue = requestObject[1]
                options = requestObject[2]

                self.execute_request(request, result_queue, options)
            except Empty:
                # ignore queue-empty exceptions
                pass
            except Exception as e:
                # ignore queue-empty exceptions
                print(e, flush=True)
                pass
        self.conn.close()

    def workflow_start(self):
        self.isRunning = True
        self.conn=self.create_connection()
        thread = Thread(target = self.process)
        thread.start()

    def workflow_end(self):
        self.isRunning = False
        
