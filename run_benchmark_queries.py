import importlib
import json
import csv
import time
import multiprocessing
import numpy as np
import os
from threading import Thread
from queue import Empty
from collections import OrderedDict,deque
from optparse import OptionParser
from request import SqlRequest
import logging

import util

logging.basicConfig(filename='output.log', level=logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger = logging.getLogger("ssb")
logger.addHandler(consoleHandler)


class SSB:
  result_queue = multiprocessing.Queue()
 
  def __init__(self):
    parser = OptionParser()
    parser.add_option("--driver-name", dest="driver_name", action="store", help="Driver name")
    (self.options, args) = parser.parse_args()
    if not self.options.driver_name:
      parser.error("No driver name specified.")

    self.setup()
    self.run()

  def setup(self, driver_arg = None):
    logger.info("loading driver")
    module = importlib.import_module("drivers." +  self.options.driver_name)
    self.driver = getattr(module, "SSBDriver")()

    logger.info("initializing driver")
    try:
      self.driver.init(self.options)
    except AttributeError:
      pass

  def run(self):
    with open(self.get_workflow_path()) as f:
      json_data = json.load(f)
      self.workflow_queries = json_data["queries"]

    self.query_results = OrderedDict({ "args": vars(self.options), "results": deque() })
    self.benchmark_start_time = util.get_current_ms_time()

    try:
      logger.info("calling 'workflow_start' on driver")
      self.driver.workflow_start()
    except AttributeError:
      pass

    total_queries = len(self.workflow_queries)
    global total_processed
    total_processed = 0

    def poll_results(slf, queue):
      global total_processed
      while total_processed < total_queries:
        logger.info("polling for results")
        try:
          process_result = queue.get(timeout=1)
        except Empty:
          logger.info("result queue empty... trying again")
          continue
        if process_result is None:
          continue
        self.deliver_request(process_result)
        total_processed = total_processed + 1
      logger.info("stopped polling results")
    thread = Thread(target = poll_results, args = (self, SSB.result_queue))
    thread.start()

    for query_id,query in enumerate(self.workflow_queries):
      request = SqlRequest(query_id,query)
      self.driver.process_request(request, SSB.result_queue, self.options)
      #time.sleep(0.002) # so the request threads do not overwhelm some of the drivers (particularly verdictdb)
 
    thread.join()
    self.end_run()

  def end_run(self):
    self.benchmark_end_time = util.get_current_ms_time()
    logger.info("done processing queries")
    try:
      logger.info("calling 'workflow_end' on driver")
      self.driver.workflow_end()
    except AttributeError:
      pass

    path = "results.json"
    logger.info("saving results to %s" % path)
    with open(path, "w") as fp:
      res = OrderedDict({
        "args": self.query_results["args"],
        "results": list(self.query_results["results"])
      })
      res["workflow-start-time"] = self.workflow_start_time
      json.dump(res, fp, indent=4)

  def deliver_request(self, request):
    if len(self.query_results["results"]) == 0 :
      self.workflow_start_time = request.start_time
    query_result = {}
    query_result["id"] = request.query_id
    query_result["ssb_id"] = request.ssb_id
    query_result["sql"] = request.sql_statement
    query_result["start_time"] = request.start_time - self.workflow_start_time
    query_result["end_time"] = request.end_time - self.workflow_start_time
    query_result["result"] = request.result
  
    self.query_results["results"].append(query_result)
    request.delivered = True

  def get_workflow_path(self):
    return "workflow.json"

if __name__ == "__main__":
  SSB()

