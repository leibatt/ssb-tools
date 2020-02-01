import json
import datetime, time
import itertools
import duckdb
import decimal
import os
import multiprocessing
from multiprocessing import Queue
import util
import queue
from queue import Empty
import threading
from threading import Thread
import logging

logger = logging.getLogger("ssb")
class SSBDriver:
    def init(self, options):
        self.isRunning = False
        self.requests = queue.Queue() #fifo
        self.config = json.load(open(os.path.join(os.path.dirname(__file__),'..','duckdb.config.json')))
        
    def create_connection(self):
        connection = duckdb.connect(self.config['dbFilename'])
        return connection

    def execute_query(self, query):
        # get a connection from the pool - block if non is available
        sql_statement = query
        #logger.info("(%s) %s" % (request.ssb_id,sql_statement))
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(sql_statement)
        data = cursor.fetchall()

        # put connection back in the queue so the next thread can use it.
        cursor.close()

        results = []
        for row in data:
            results.append(row)
        return results

    def process_request(self, request, result_queue, options):
        self.requests.put((request, result_queue, options))

    def process(self):
        self.conn = self.create_connection()
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
                 logger.error("exception occurred")
                 logger.error(e)
                 raise
        self.conn.close()
        return

    def workflow_start(self):
        self.isRunning = True

        thread = Thread(target = self.process)
        thread.start()

    def workflow_end(self):
        self.isRunning = False
