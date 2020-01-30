import random

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
