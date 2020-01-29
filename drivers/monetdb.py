import pymonetdb
import datetime, time
import itertools
import csv
import json
import os
import queue
import multiprocessing
import threading
from threading import Thread
import logging
from subprocess import call
import util

logger = logging.getLogger("ssb")
class SSBDriver:
  def init(self, options):
    self.isRunning = False
    self.requests = queue.LifoQueue()
    self.config = json.load(open(os.path.join(os.path.dirname(__file__),'..','monetdb.config.json')))

  def create_connection(self):
    conn = pymonetdb.connect(username="crossfilter", password=self.config['password'], hostname=self.config["host"], port=self.config['port'], database=self.config['database-name'])
    return conn

  def execute_request(self, request, result_queue, options):
    # get a connection from the pool - block if non is available
    logger.info(request.toJson())
    sql_statement = request.sql_statement
    connection = self.pool.get()
    cursor = connection.cursor()
    request.start_time = util.get_current_ms_time()
    cursor.execute(sql_statement)
    data = cursor.fetchall()
    request.end_time = util.get_current_ms_time()

    # put connection back in the queue so the next thread can use it.
    cursor.close()
    self.pool.put(connection)

    results = []
    for row in data:
      results.append(dict(row))
    request.result = results
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
      except:
        # ignore queue-empty exceptions
        #pass
        raise
    return

  def workflow_start(self):
    # pool a number of db connections
    self.isRunning = True
    self.pool = queue.Queue()
    for i in range(10):
      conn = self.create_connection()
      self.pool.put(conn)

    thread = Thread(target = self.process)
    thread.start()

  def workflow_end(self):
    self.isRunning = False
    # close all db connections at the end of a workflow
    for i in range(self.pool.qsize()):
      conn = self.pool.get(timeout=1)
      conn.close()

