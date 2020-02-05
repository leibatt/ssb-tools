import sys
import os
import pyverdict,json

def run(verdictdbConfig):
  port=verdictdbConfig['port']
  password=verdictdbConfig['password']
  conn=pyverdict.postgres(host=verdictdbConfig['host'],user=verdictdbConfig['username'],password=password,port=port,dbname=verdictdbConfig['database-name'])
  conn.set_loglevel("ERROR")
  scramblePercent = verdictdbConfig['scramblePercent']
  scrambleFrac = scramblePercent / 100.0

  df=conn.sql('DROP SCRAMBLE "public"."lineorder_scrambled_'+str(scramblePercent)+'_percent" on "public"."lineorder" SIZE '+str(scrambleFrac))
  
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
