import math
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

import random
logging.basicConfig(filename='output.log', level=logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger = logging.getLogger("ssb")
logger.addHandler(consoleHandler)



# creates proper queries and returns them in random order
def populateAndRandomize(workflow):
  queries = list(workflow["queries"])
  populateAllQueries(queries)
  return randomizeQueries(queries)

# create a random ordering and return it
def randomizeQueries(queries):
  ordering = list(queries)
  random.shuffle(ordering)
  return ordering

# generate a proper sql statement for all queries in the workflow
def populateAllQueries(queries):
  for query in queries:
    populateQuery(query)
  return queries

# generate a proper sql statement
def populateQuery(query):
  sql = query["sql_statement"]
  for p in query["parameters"]:
    pu = p.upper()
    print(p,query["parameters"].keys())
    values = query["parameters"][p]["value"]
    for i,v in enumerate(values):
      k = "".join(["[",pu,"-",str(i),"]"])
      sql = sql.replace(k,str(v))
  query["sql_statement_old"] = query["sql_statement"]
  query["sql_statement"] = sql
  return query

def getTotalRowsQuery(query):
  return query["base-query"].replace("[ATTRIBUTES]","count(*)")

def getCardinalityQuery(attributeId, query):
  attributeName = query["parameters"][attributeId]["attribute_name"]
  base = query["base-query"].replace("[ATTRIBUTES]",",".join([attributeName,"count(*)"])).replace(";","")
  return base + " group by " + attributeName + ";"

class QueryRandomizer:
  new_workflow = {}
  def __init__(self):
    parser = OptionParser()
    parser.add_option("--driver-name", dest="driver_name", action="store", help="Driver name")
    (self.options, args) = parser.parse_args()
    if not self.options.driver_name:
      parser.error("No driver name specified.")
    self.ssb_config = json.load(open("ssb.config.json"))

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
      self.workflow = json_data

    self.benchmark_start_time = util.get_current_ms_time()

    try:
      logger.info("calling 'workflow_start' on driver")
      self.driver.workflow_start()
    except AttributeError:
      pass

    self.new_workflow = dict(self.workflow)
    #total_queries = len(self.workflow["queries"])

    for query_id,query in enumerate(self.workflow["queries"]):
      # get total rows
      trq = getTotalRowsQuery(query)
      res = self.driver.execute_query(trq)
      totalRows = res[0][0]
      #logger.info("query: '%s', result: %d" % (trq,res[0][0]))

      # find correct selectivity
      for attrId in query["parameters"]:
        selectivity = query["parameters"][attrId]["selectivity"]
        cq = getCardinalityQuery(attrId,query)
        res = self.driver.execute_query(cq)
        uniqueVals = len(res)
        #logger.info("query: '%s', result: %d" % (cq,res[0][0]))
        totalSelections = int(math.ceil(1.0 * selectivity["select"] / selectivity["out-of"] * uniqueVals))
        logger.info("query: '%s', unique vals for attr '%s': %d, total selections: %d" % (cq,attrId,uniqueVals,totalSelections))
 
    self.end_run()

  def end_run(self):
    logger.info("done processing queries")
    try:
      logger.info("calling 'workflow_end' on driver")
      self.driver.workflow_end()
    except AttributeError:
      pass

    path = self.get_workflow_path()+".generated"
    logger.info("saving results to %s" % path)
    with open(path, "w") as fp:
      json.dump(self.new_workflow, fp, indent=4)

  def get_workflow_path(self):
    return self.ssb_config["workflow-file"]

if __name__ == "__main__":
  QueryRandomizer()

