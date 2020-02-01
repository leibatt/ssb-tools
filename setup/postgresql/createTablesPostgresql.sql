DROP TABLE IF EXISTS lineorder;
DROP TABLE IF EXISTS date_;
DROP TABLE IF EXISTS supplier;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS part;

CREATE TABLE date_ (
  d_datekey          INTEGER,     -- identifier, unique id -- e.g. 19980327 (what we use)
  d_date             VARCHAR(18),  -- varchar(18), --fixed text, size 18, longest: december 22, 1998
  d_dayofweek        VARCHAR(9),  -- varchar(9), --fixed text, size 9, sunday, monday, ..., saturday)
  d_month            VARCHAR(9),  -- varchar(9), --fixed text, size 9: january, ..., december
  d_year             INTEGER,     -- unique value 1992-1998
  d_yearmonthnum     INTEGER,     -- numeric (yyyymm) -- e.g. 199803
  d_yearmonth        VARCHAR(7),  -- varchar(7), --fixed text, size 7: mar1998 for example
  d_daynuminweek     INTEGER,     -- numeric 1-7
  d_daynuminmonth    INTEGER,     -- numeric 1-31
  d_daynuminyear     INTEGER,     -- numeric 1-366
  d_monthnuminyear   INTEGER,     -- numeric 1-12
  d_weeknuminyear    INTEGER,     -- numeric 1-53
  d_sellingseason    VARCHAR(12),  -- varchar(12), --text, size 12 (christmas, summer,...)
  d_lastdayinweekfl  INTEGER,     -- 1 bit
  d_lastdayinmonthfl INTEGER,     -- 1 bit
  d_holidayfl        INTEGER,     -- 1 bit
  d_weekdayfl        INTEGER,     -- 1 bit
  extra INTEGER,
  PRIMARY KEY (d_datekey) 
);

CREATE TABLE supplier (
  s_suppkey INTEGER,     -- identifier
  s_name    VARCHAR(25),  -- varchar(25), --fixed text, size 25: 'supplier'||suppkey
  s_address VARCHAR(25),  -- varchar(25), --variable text, size 25 (city below)
  s_city    VARCHAR(10),  -- varchar(10), --fixed text, size 10 (10/nation: nation_prefix||(0-9))
  s_nation  VARCHAR(15),  -- varchar(15), --fixed text(15) (25 values, longest united kingdom)
  s_region  VARCHAR(12),  -- varchar(12), --fixed text, size 12 (5 values: longest middle east)
  s_phone   VARCHAR(15),  -- varchar(15) --fixed text, size 15 (many values, format: 43-617-354-1222)
  extra INTEGER,
  PRIMARY KEY (s_suppkey)
);

CREATE TABLE customer (
  c_custkey    INTEGER,--numeric identifier
  c_name       VARCHAR(25),     -- varchar(25), --variable text, size 25 'customer'||custkey
  c_address    VARCHAR(25),     -- varchar(25), --variable text, size 25 (city below)
  c_city       VARCHAR(10),     -- varchar(10), --fixed text, size 10 (10/nation: nation_prefix||(0-9)
  c_nation     VARCHAR(15),     -- varchar(15), --fixed text(15) (25 values, longest united kingdom)
  c_region     VARCHAR(12),     -- varchar(12), --fixed text, size 12 (5 values: longest middle east)
  c_phone      VARCHAR(15),     -- varchar(15), --fixed text, size 15 (many values, format: 43-617-354-1222)
  c_mktsegment VARCHAR(10),     -- varchar(10) --fixed text, size 10 (longest is automobile)
  extra INTEGER,
  PRIMARY KEY (c_custkey)
);

CREATE TABLE part (
  p_partkey   INTEGER,        -- identifier
  p_name      VARCHAR(22),     -- varchar(22), --variable text, size 22 (not unique per part but never was)
  p_mfgr      VARCHAR(6),     -- varchar(6), --fixed text, size 6 (mfgr#1-5, card = 5)
  p_category  VARCHAR(7),     -- varchar(7), --fixed text, size 7 ('mfgr#'||1-5||1-5: card = 25)
  p_brand1    VARCHAR(9),     -- varchar(9), --fixed text, size 9 (category||1-40: card = 1000)
  p_color     VARCHAR(11),     -- varchar(11), --variable text, size 11 (card = 94)
  p_type      VARCHAR(25),     -- varchar(25), --variable text, size 25 (card = 150)
  p_size      INTEGER,        -- numeric 1-50 (card = 50)
  p_container VARCHAR(15),     -- varchar(15) --fixed text(10) (card = 40)
  extra INTEGER,
  PRIMARY KEY (p_partkey)
);

CREATE TABLE lineorder (
  lo_orderkey      INTEGER,     -- numeric (int up to sf 300) first 8 of each 32 keys used
  lo_linenumber    INTEGER,     -- numeric 1-7
  lo_custkey       INTEGER,     -- numeric identifier foreign key reference to c_custkey
  lo_partkey       INTEGER,     -- identifier foreign key reference to p_partkey
  lo_suppkey       INTEGER,     -- numeric identifier foreign key reference to s_suppkey
  lo_orderdate     INTEGER,     -- identifier foreign key reference to d_datekey
  lo_orderpriority VARCHAR(15),  -- varchar(15), --fixed text, size 15 (5 priorities: 1-urgent, etc.)
  lo_shippriority  VARCHAR(1),  -- varchar(1), --fixed text, size 1
  lo_quantity      INTEGER,     -- numeric 1-50 (for part)
  lo_extendedprice INTEGER,     -- numeric, max about 55,450 (for part)
  lo_ordtotalprice INTEGER,     -- numeric, max about 388,000 (for order)
  lo_discount      INTEGER,     -- numeric 0-10 (for part) -- (represents percent)
  lo_revenue       INTEGER,     -- numeric (for part: (extendedprice*(100-discount))/100)
  lo_supplycost    INTEGER,     -- numeric (for part, cost from supplier, max = ?)
  lo_tax           INTEGER,     -- numeric 0-8 (for part)
  lo_commitdate    INTEGER,     -- foreign key reference to d_datekey
  lo_shipmode      VARCHAR(10),  -- varchar(10) --fixed text, size 10 (modes: reg air, air, etc.)
  extra INTEGER,
  PRIMARY KEY (lo_orderkey, lo_linenumber), --Compound Primary Key: ORDERKEY, LINENUMBER
  FOREIGN KEY (lo_orderdate)  REFERENCES date_    (d_datekey), --identifier foreign key reference to D_DATEKEY
  FOREIGN KEY (lo_commitdate) REFERENCES date_    (d_datekey), --Foreign Key reference to D_DATEKEY
  FOREIGN KEY (lo_suppkey)    REFERENCES supplier (s_suppkey), --numeric identifier foreign key reference to S_SUPPKEY
  FOREIGN KEY (lo_custkey)    REFERENCES customer (c_custkey)  --numeric identifier foreign key reference 
);
