### Paycheck Protection Program Loans & COVID-19 cases data lake

##### Purpose and goals
The project goal is to create a data lake that enables the final user to explore the PPP Loans and COVID-19 cases. This data lake can be used, for example, to identify if there is a relationship between the geographies that: (i) were most impacted by COVID-19 (based on number of cases); and (ii) had the most PPP loans approved. The data lake will be hosted in the cloud (AWS).

##### Data model
The data lake was designed with automation in mind. It includes automation processes for data cataloging with the end goal of enabling a self-service data lake, as well as automated ETL pipelines, which exposes the data in parquet files to allow faster queries. The following data dictionary explains the data model:

###### PPP Loans table

1. loanamount (double)
2. businessname (string)
3. address (string)
4. city (string)
5. state (string)
6. zip (bigint)
7. naicscode (bigint)
8. businesstype (string)
9. raceethnicity (string)
10. gender (string)
12. veteran (string)
13. nonprofit (string)
14. jobsreported (bigint)
15. dateapproved (string)
16. lender (string)
17. cd (string)

###### COVID-19 cases table
1. province_state (string)
2. country_region (string)
3. last_update (string)
4. lat (double)
5. long_ (double)
6. confirmed (double)
7. deaths (double)
8. recovered (double)
9. active (double)
10. fips (double)
11. incident_rate (double)
12. total_test_results (double)
13. people_hospitalized (double)
14. case_fatality_ratio (double)
15. uid (double)
16. iso3 (string)
17. testing_rate (double)
18. hospitalization_rate (double)

The tables described above will capture the information collected (Please refer to secion Data pipeline for further details).

##### Data pipeline

###### Source data
The data is sourced is from two different datasets:

1. A set of CSV files that include the Paycheck Protection Program loans. 
2. A JSON file that includes the COVID-19 cases by date.

Both datasets are stored in Amazon S3, where they are automatically processed in the pipeline.

###### ETL pipeline

Thw following components integrate the data pipeline:

1. Two S3 buckets - one bucket to store raw data and one to store processed data. (Screenshot below)
2. Two Lambda functions - one to create data catalog andone to send notifications through SNS. (Code in the Lambda folder & in the Glue Folder)
3. A SQS queue to enable retries if the job fails.  (Screenshot below)
4. A SNS topic to send automatic notifications when the data has been successfully processed.  (Screenshot below)
5. Two CloudWatch rules to trigger the lambda funcitons.  (Screenshot below)
6. An Athena table to explore the data (note that other services like EMR or similar could be used to query the data).  (Code in the Athena folder)

Set forth below if a diagram of how the data flows:

![architecture](/architecture.png)

###### Technology leveraged

S3: AWS' proven object storage service. It was utilized to store the data asit can handle big datasets without storage concerns and it provides capabilities such as triggering functions, and versioning.

Lambda - AWS serverless computing service. Used to create microservices that call the Glue data processes without the need of creating virtual machines.

SQS - AWS Distributed queue service. Used to asynchronously manage a potential error in the data pipeline, storing the files that failed in the pipeline to enable future processing.

SNS - AWS Notification service. Used to email the user when new data is ready to be analyzed

Cloudwatch - AWS Metric and event repository. Used to trigger other services.

Athena - AWS serverless interactive query service. Used to execute Data Quality processes and explore the data created without the need of creating databases.


Please refer to the screenshots below for the services used:

S3 Raw Data Bucket and trigger
![sthreerawdata](/sthreerawdata.png)

S3 Processed data bucket
![sthreeprocesseddata](/sthreeprocesseddata.png)

Lambda function to call the crawler
![lambdacrawler](/lambdacrawler.png)

Lamda function to call the ETL job
![lambdaetl](/lambdaetl.png)

SQS queue
![sqs](/sqs.png)

SNS notification
![sns](/sns.png)

Cloudwatch alarm to fire the crawler
![cloudwatchlambda](/cloudwatchlambda.png)

Cloudwatch alarm to send the notification
![cloudwatchsns](/cloudwatchsns.png)

Glue crawler
![gluecrawler](/gluecrawler.png)

Glue schema inferred
![glueschema](/glueschema.png)

Glue ETL job
![glueetl](/glueetl.png)

Athena table
![athena](/athena.png)

*Note that given the fact that the data lake exposes the data through parquet files hosted on S3. Such data can be queried using other services like AWS EMR, spark clusters with access to the bucket, among others.

##### Analysis and Data Quality results

The following queries were executed to validate data integrity:

#of rows in PPP table

![rowstableppp](/rowstableppp.png)

#of rows in COVID-19 table

![rowstablecovid](/rowstablecovid.png)

States with the most COVID-19 cases

![statesmostcases](/statesmostcases.png)

States with the most PPP loans

![statesmostloans](/statesmostloans.png)
