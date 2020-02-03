import sys
import os
import pyverdict,json


def run(verdictdbConfig):
  port=verdictdbConfig['port']
  password=verdictdbConfig['password']
  conn=pyverdict.postgres(host=verdictdbConfig['host'],user=verdictdbConfig['username'],password=password,port=port,dbname=verdictdbConfig['database-name'])
  conn.set_loglevel("ERROR")
  scramblePercent = verdictdbConfig['scramblePercent'] / 100.0
  
  # just to make sure the verdictdb metadata exists first
  df=conn.sql('CREATE SCRAMBLE "public"."ssb_test_scramble" from "public"."customer" SIZE 0.05')
  df=conn.sql('DROP SCRAMBLE "public"."ssb_test_scramble" on "public"."customer" SIZE 0.05')
  
  # make the real scrambles
  #df=conn.sql('DROP SCRAMBLE "public"."customer_scrambled_10_percent" on "public"."customer" SIZE 0.1')
  #df=conn.sql('CREATE SCRAMBLE "public"."customer_scrambled_10_percent" from "public"."customer" SIZE 0.1')
  
  #df=conn.sql('DROP SCRAMBLE "public"."supplier_scrambled_10_percent" on "public"."supplier" SIZE 0.1')
  #df=conn.sql('CREATE SCRAMBLE "public"."supplier_scrambled_10_percent" from "public"."supplier" SIZE 0.1')
  
  #df=conn.sql('DROP SCRAMBLE "public"."date__scrambled_10_percent" on "public"."date_" SIZE 0.1')
  #df=conn.sql('CREATE SCRAMBLE "public"."date__scrambled_10_percent" from "public"."date_" SIZE 0.1')
  
  df=conn.sql('DROP SCRAMBLE "public"."lineorder_scrambled_10_percent" on "public"."lineorder" SIZE ' + str(scramblePercent))
  df=conn.sql('CREATE SCRAMBLE "public"."lineorder_scrambled_10_percent" from "public"."lineorder" SIZE ' + str(scramblePercent))
  
  #df=conn.sql('DROP SCRAMBLE "public"."part_scrambled_10_percent" on "public"."part" SIZE 0.1')
  #df=conn.sql('CREATE SCRAMBLE "public"."part_scrambled_10_percent" from "public"."part" SIZE 0.1')
  
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
