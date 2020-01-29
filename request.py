import json

class SqlRequest:
  def __init__(self, query_id, query):
    self.query_id = query_id
    self.ssb_id = query["ssb_id"]
    self.sql_statement = query["sql_statement"]
    self.start_time = -1
    self.end_time = -1
    self.result = None

  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)        
