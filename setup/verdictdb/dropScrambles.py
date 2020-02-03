import sys
import os
import pyverdict,json

def run(verdictdbConfig):
  port=verdictdbConfig['port']
  password=verdictdbConfig['password']
  conn=pyverdict.postgres(host=verdictdbConfig['host'],user=verdictdbConfig['username'],password=password,port=port,dbname=verdictdbConfig['database-name'])
  conn.set_loglevel("ERROR")

  df=conn.sql('DROP SCRAMBLE "public"."lineorder_scrambled_10_percent" on "public"."lineorder" SIZE 0.1')
  
if __name__ == "__main__":
  if len(sys.argv) > 2:
    verdictdbConfigPath = sys.argv[1]
    ssbConfigPath = sys.argv[2]
    try:
      verdictdbConfig = json.load(open(verdictdbConfigPath))
      ssbConfig = json.load(open(ssbConfigPath))
      run(verdictdbConfig)
    except Exception as e:
      print(e)
      print("usage: python",sys.argv[0],"[verdictdb config] [ssb config]")
      sys.exit(0)
