--Table to store the ppp loans
CREATE EXTERNAL TABLE IF NOT EXISTS ppp_loans (
  loanamount double,
businessname string,
address string,
city string,
state string,
zip bigint,
naicscode bigint,
businesstype string,
raceethnicity string,
gender string,
veteran string,
nonprofit string,
jobsreported bigint,
dateapproved string,
lender string,
cd string
  )
STORED AS PARQUET
LOCATION 's3://udacitydatalake-processeds3bucket-15oyrvm2o5is9/'
tblproperties ("parquet.compress"="SNAPPY");

--Table to create the covid cases
CREATE EXTERNAL TABLE IF NOT EXISTS covid_cases (
  Province_State string,
  Country_Region string,
  Last_Update string,
  Lat double,
  Long_ double,
  Confirmed double,
  Deaths double,
  Recovered double,
  Active double,
  FIPS double,
  Incident_Rate double,
  Total_Test_Results double,
  People_Hospitalized double,
  Case_Fatality_Ratio double,
  UID double,
  ISO3 string,
  Testing_Rate double,
  Hospitalization_Rate double
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
WITH SERDEPROPERTIES ("separatorChar" = ",", "escapeChar" = "\\")
LOCATION 's3://udacity-datalake-covid-cases/';

--Data quality
select state,cast(sum(loanamount) as bigint) as amount, count(1) as loans
from ppp_loans
group by state
order by 2 desc
limit 10
;

select Province_State,cast(sum(Confirmed) as bigint) as cases
from covid_cases
group by Province_State
order by 2 desc
limit 10
;
