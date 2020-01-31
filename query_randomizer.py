import numbers
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
import random
import util

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
def populateQueryWithOriginalValues(query):
  sql = query["sql_statement"]
  for p in query["parameters"]:
    pu = p.upper()
    #print(p,query["parameters"].keys())
    values = query["parameters"][p]["value"]
    for i,v in enumerate(values):
      k = "".join(["[",pu,"-",str(i),"]"])
      sql = sql.replace(k,str(v))
  query["sql_statement_old"] = query["sql_statement"]
  query["sql_statement"] = sql
  return query

def populateQueryWithSelections(query,selections):
  sql = query["sql_statement"]
  for p in query["parameters"]:
    pu = p.upper()
    #print(p,query["parameters"].keys())
    values = selections[p]
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
  return base + " group by " + attributeName + " order by " + attributeName + " asc;"

def updateUniqueValues(attributeId,query,selected,driver,logger):
  if "depends" in query["parameters"][attributeId]: # take other predicates into account:
    attributeName = query["parameters"][attributeId]["attribute_name"]
    dependsOn = query["parameters"][attributeId]["depends"]
    logger.info("recalculating unique vals for attribute %s, depends on: %s" % (attributeName,", ".join([query["parameters"][d]["attribute_name"] for d in dependsOn])))
    baseQuery = query["base-query"].replace("[ATTRIBUTES]",attributeName+", count(*)").replace(";","")
    for d in dependsOn: # for each attribute we depend on
      dname = query["parameters"][d]["attribute_name"]
      dst = query["parameters"][d]["selection-type"]
      baseQuery = baseQuery + " and " + buildPredicate(selected[d],dst,dname)
    baseQuery = baseQuery + " group by " +attributeName+ " order by " +attributeName+ " asc;"
    print(baseQuery)
    uniqueValues = driver.execute_query(baseQuery)
    print(uniqueValues)
    return uniqueValues
  return None

def createSelection(attributeId,query,uniqueValues,totalRows,selected,driver,logger):
  selType = query["parameters"][attributeId]["selection-type"]
  if selType == "equal":
    return selectForEqual(attributeId,query,uniqueValues,totalRows,selected,driver,logger)
  elif selType == "between":
    return selectForBetween(attributeId,query,uniqueValues,totalRows,selected,driver,logger)
  elif selType == "less-than":
    return selectForLessThan(attributeId,query,uniqueValues,totalRows,selected,driver,logger)
  elif selType == "in":
    return selectForIn(attributeId,query,uniqueValues,totalRows,selected,driver,logger)
  elif selType == "between-equal":
    return selectForBetweenEqual(attributeId,query,uniqueValues,totalRows,selected,driver,logger)
  else: # default
    return None

def selectForEqual(attributeId,query,uniqueValues,totalRows,selected,driver,logger):
  u = updateUniqueValues(attributeId,query,selected,driver,logger)
  if u is not None:
    uniqueValues = u

  #print(uniqueValues)
  index = random.randint(0,len(uniqueValues)-1)
  tup = uniqueValues[index]
  return [tup[0]]

def selectForBetween(attributeId,query,uniqueValues,totalRows,selected,driver,logger):
  u = updateUniqueValues(attributeId,query,selected,driver,logger)
  if u is not None:
    uniqueValues = u

  selectivity = query["parameters"][attributeId]["selectivity"]
  breadth = int(max(1,math.floor(1.0*selectivity["select"]*len(uniqueValues)/selectivity["out-of"])))
  #print("breadth: ",breadth)
  maxStart = len(uniqueValues) - breadth
  start = random.randint(0,maxStart)
  #return [v[0] for v in uniqueValues[start:start+breadth]]
  return [uniqueValues[start][0],uniqueValues[start+breadth-1][0]]

def selectForLessThan(attributeId,query,uniqueValues,totalRows,selected,driver,logger):
  u = updateUniqueValues(attributeId,query,selected,driver,logger)
  if u is not None:
    uniqueValues = u

  selectivity = query["parameters"][attributeId]["selectivity"]
  index = int(1.0*selectivity["select"]*(len(uniqueValues)-1)/selectivity["out-of"])
  return [uniqueValues[index][0]]
  #return None

def selectForBetweenEqual(attributeId,query,uniqueValues,totalRows,selected,driver,logger):
  u = updateUniqueValues(attributeId,query,selected,driver,logger)
  if u is not None:
    uniqueValues = u

  index = random.randint(1,len(uniqueValues)-2)
  return [uniqueValues[index][0],uniqueValues[index][0]]


def selectForIn(attributeId,query,uniqueValues,totalRows,selected,driver,logger):
  u = updateUniqueValues(attributeId,query,selected,driver,logger)
  if u is not None:
    uniqueValues = u
    
  selectivity = query["parameters"][attributeId]["selectivity"]
  total = int(max(1,math.floor(1.0*selectivity["select"]*len(uniqueValues)/selectivity["out-of"])))
  #print("total:",total)
  indexes = list(range(0,len(uniqueValues)))
  random.shuffle(indexes)
  return [uniqueValues[i][0] for i in indexes[:total]]

def buildPredicate(selectedVals,selType,attributeName):
  if isinstance(selectedVals[0], numbers.Number):
    if selType == "equal":
      return attributeName + " = " + str(selectedVals[0])
    elif selType == "between":
      return attributeName + " between " + str(selectedVals[0]) + " and " + str(selectedVals[1])
    elif selType == "less-than":
      return attributeName + " < " + str(selectedVals[0])
    elif selType == "in":
      return "(" + " or ".join([attributeName +" = "+str(sv) for sv in selectedVals])+ ")"
    elif selType == "between-equal":
      return attributeName + " between " + str(selectedVals[0]-1) + " and " + str(selectedVals[0]+1)
    else: # default
      return None
  else:
    if selType == "equal":
      return attributeName + " = '" + str(selectedVals[0]) + "'"
    elif selType == "between":
      return attributeName + " between '" + str(selectedVals[0]) + "' and '" + str(selectedVals[1]) + "'"
    elif selType == "less-than":
      return attributeName + " < '" + str(selectedVals[0]) + "'"
    elif selType == "in":
      return "(" + " or ".join([attributeName +" = '"+str(sv) + "'" for sv in selectedVals])+ ")"
    elif selType == "between-equal":
      return attributeName + " between '" + str(selectedVals[0]-1) + "' and '" + str(selectedVals[0]+1) + "'"
    else: # default
      return None
 
def checkQuerySelectivity(driver,selectedVals,attributeId,selType,query,totalRows):
  selectivity = query["parameters"][attributeId]["selectivity"]
  attributeName = query["parameters"][attributeId]["attribute_name"]
  baseQuery = query["base-query"].replace("[ATTRIBUTES]","count(*)").replace(";","")
  if "where" in baseQuery:
    baseQuery = baseQuery + " and " + buildPredicate(selectedVals,selType,attributeName) + ";"
  else:
    baseQuery = baseQuery + " where " + buildPredicate(selectedVals,selType,attributeName) + ";"
  print("baseQuerySelectivityCheck",baseQuery)
  res = driver.execute_query(baseQuery)
  ct = res[0][0]
  newsel=1.0*ct/totalRows
  oldsel=1.0*selectivity["select"]/selectivity["out-of"]
  diff = abs(newsel-oldsel)
  diff_adj = diff/(oldsel)
  print("attributeName:",attributeName,"count:",ct,"total:",totalRows,"selectivity:",1.0*ct/totalRows,"old selectivity:",1.0*selectivity["select"]/selectivity["out-of"],"difference:",diff,"normalized difference:",diff_adj)

def generateFinalQueries(workflow,driver,logger):
  for query_id,query in enumerate(workflow["queries"]):
    generateFinalQuery(query_id,query,driver,logger)
  return workflow

def generateFinalQuery(query_id,query,driver,logger):
    # get total rows
    trq = getTotalRowsQuery(query)
    res = driver.execute_query(trq)
    totalRows = res[0][0]
    #logger.info("query: '%s', result: %d" % (trq,res[0][0]))

    # find correct selectivity
    selected = {}
    predicates = []
    for attributeId in query["parameters"]:
      selectivity = query["parameters"][attributeId]["selectivity"]
      cq = getCardinalityQuery(attributeId,query)
      uniqueValues = driver.execute_query(cq)
      totalUnique = len(uniqueValues)
      #logger.info("query: '%s', result: %d" % (cq,res[0][0]))
      totalSelections = int(math.ceil(1.0 * selectivity["select"] / selectivity["out-of"] * totalUnique))

      #pick random values
      #logger.info("query: '%s', unique vals for attr '%s': %d, total selections: %d" % (cq,attributeId,totalUnique,totalSelections))
      #print(uniqueValues)
      sel = createSelection(attributeId,query,uniqueValues,totalRows,selected,driver,logger)
      selected[attributeId]=sel
      selType = query["parameters"][attributeId]["selection-type"]
      attributeName = query["parameters"][attributeId]["attribute_name"]
      #print(query)
      #print(uniqueValues)
      #print(sel)
      #scheck=checkQuerySelectivity(self.driver,sel,attributeId,selType,query,totalRows) 
      #print(scheck)
      predicates.append(buildPredicate(sel,selType,attributeName))

    # selected object has all selections for each attribute. Now we can build the final query
    finalQuery=populateQueryWithSelections(query,selected)
    #print(finalQuery["sql_statement"])

class QueryRandomizer:
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
    self.workflow = None
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

    generateFinalQueries(self.workflow,self.driver,logger)

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
      json.dump(self.workflow, fp, indent=4)

  def get_workflow_path(self):
    return self.ssb_config["workflow-file"]

if __name__ == "__main__":
  logging.basicConfig(filename='ssb_query_randomizer.log', level=logging.INFO)
  logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
  consoleHandler = logging.StreamHandler()
  consoleHandler.setFormatter(logFormatter)
  logger = logging.getLogger("ssb-randomizer")
  logger.addHandler(consoleHandler)
  QueryRandomizer()

