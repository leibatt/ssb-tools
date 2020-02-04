import sys
import os
import json
import pandas as pd
import numpy as np, scipy.stats as st

def computeCi95Lower(s):
  return st.t.interval(0.95, len(s) -1, loc=np.mean(s), scale=st.sem(s))[0]

def computeCi95Upper(s):
  return st.t.interval(0.95, len(s) -1, loc=np.mean(s), scale=st.sem(s))[1]


def generate_results_all_scale_factors(filepath):
  res = []
  #for size in ["sf_1","sf_2","sf_4","sf_8"]:
  for size in ["sf_1","sf_2","sf_4"]:
    sizeName = size.replace("sf_","")
    print("evaluating scale factor:",size)
    sizePath = os.path.join(filepath,size)
    # there will be multiple run folders in the scale factor folder
    # TODO: handle run folders
    if os.path.exists(sizePath):
      res1 = consolidate_results_all_runs(sizePath)
      for r in res1:
        r["scale_factor"] = sizeName
      res.extend(res1)
  # concatenate everything
  resDf = pd.concat(res)
  #print(resDf.groupby(["scale_factor","driver"]).count())
  totalQueries = 13
  aggRes = resDf.groupby(["scale_factor", "driver","ssb_id"]).agg(
    meanDuration=('duration', 'mean'),
    durationCiLower=('duration', computeCi95Lower),
    durationCiUpper=('duration', computeCi95Upper),
    durationStd=('duration', 'std')
  ).reset_index().copy()
  aggResDescribe = resDf.groupby(["scale_factor", "driver","ssb_id"]).agg('describe')['duration'].reset_index()
  print(aggResDescribe.to_json(orient="records"))
  return resDf,aggRes

def consolidate_results_all_runs(filepath):
  run_id = 0
  res = []
  run_folder = os.path.join(filepath,"run_" + str(run_id))
  while os.path.exists(run_folder):
    print("\t\tevaluating run folder",run_folder)
    li = consolidate_results_all_drivers(run_folder)
    for df in li:
      df["run_id"] = [run_id] * df.shape[0]
    res.extend(li)
    run_id += 1
    run_folder = os.path.join(filepath,"run_" + str(run_id))
  return res

def consolidate_results_all_drivers(filepath):
  res = []
  for driver in ["duckdb","monetdb","sqlite","postgresql","verdictdb-10"]:
    print("\t\t\tevaluating driver",driver)
    driverPath = os.path.join(filepath,driver)
    if os.path.exists(driverPath):
      li = consolidate_results(driverPath)
      res.extend(li)
  return res

# for a given dataset size, dataset name, and driver
def consolidate_results(filepath):
  li = []
  total = 0
  for report in os.listdir(filepath):
    if report.endswith(".json"):
      data=json.load(open(os.path.join(filepath,report)))
      cols = {"ssb_id":[],"duration":[],"pos":[],"driver":[]}
      driver = data["args"]["driver_name"]
      for query in data["results"]:
        cols["ssb_id"].append(query["ssb_id"])
        cols["duration"].append(query["end_time"]-query["start_time"])
        cols["pos"].append(query["id"])
        cols["driver"].append(driver)
        total += 1
      df = pd.DataFrame.from_dict(cols)
      li.append(df)
  print("\t\t\ttotal records observed",total)
  return li

if __name__ == "__main__":
  if len(sys.argv) > 1:
    filepath = sys.argv[1]
    df,durationMeans=generate_results_all_scale_factors(filepath)
    print(durationMeans.to_json(orient="records"))
    with open(os.path.join(filepath,"ssb_final_results.json"),"w") as f:
      f.write(durationMeans.to_json(orient="records"))
  else:
    print("usage: python3 meanduration [path to reports]")
    sys.exit(0)
