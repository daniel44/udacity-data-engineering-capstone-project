### Paycheck Protection Program Loans & COVID-19 cases data lake

##### Purpose and goals
The project goal is to create a data lake that enables the final user to explore the PPP Loans and COVID-19 cases. This data lake can be used, for example, to identify if there is a relationship between the geographies that: (i) were most impacted by COVID-19 (based on number of cases); and (ii) had the most PPP loans approved. The data lake will be hosted in the cloud (AWS).

##### Data model & dictionary
The data lake was designed with automation in mind. It includes automation processes for data cataloging with the end goal of enabling a self-service data lake, as well as automated ETL pipelines, which exposes the data in parquet files to allow faster queries. The following data dictionary explains the data model:

###### PPP Loans table

![datadictone](/datadictone.png)

###### COVID-19 cases table

![datadicttwo](/datadicttwo.png)

The tables described above will capture the information collected (Please refer to secion Data pipeline for further details).

##### Data model justification
A data lake was implemented for this use case, as it allows to store relational data like the PPP Loans in it's raw format (CSV files), and non-relational data like COVID-19 data. It also enables to understand what data is in the lake through crawling, cataloging, and indexing of data in a very cost-effective way. There is no cost associated for the implementation of this data lake in AWS, which results in big-scale analysis at a 0 dollar cost.

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

###### Technology justification

S3: AWS' proven object storage service. It was utilized to store the data as it can handle big datasets without storage concerns and it provides capabilities such as triggering functions, and versioning. It serves as the storage layer for the lake.

Lambda - AWS serverless computing service. Used to create microservices that call the Glue data processes without the need of creating virtual machines. Serverless computing is easier to manage and provides auto-scaling capabilities, hence it was decided to use Lambda.

SQS - AWS Distributed queue service. Used to asynchronously manage a potential error in the data pipeline, storing the files that failed in the pipeline to enable future processing. Using a queue ensures that there is not a single event loss.

SNS - AWS Notification service. Used to email the user when new data is ready to be analyzed. This enables the user to identify if the automatic processing of file was succesful while being away from the computer

Cloudwatch - AWS Metric and event repository. Used to trigger other services.

Athena - AWS serverless interactive query service. Used to execute Data Quality processes and explore the data created without the need of creating databases.


###### Steps taken
Scope the Project and Gather Data
The data was gathered from public sources (SBA webpage and John Hopkins COVID-19 data). The scope is set forth below and incldued in the beginning of the Read Me: The project goal is to create a data lake that enables the final user to explore the PPP Loans and COVID-19 cases. The data was stored into a S3 bucket and an alarm was created to trigger a Lambda function every time a file is uploaded

S3 Raw Data Bucket and trigger
![sthreerawdata](/sthreerawdata.png)

Cloudwatch alarm to fire the crawler
![cloudwatchlambda](/cloudwatchlambda.png)

Explore and Assess the Data
The exploring and assessment of the data was automated using an AWS Glue Crawler that identifies column names and types, and adds such data into the meta store. A lamda function was created to call the AWS Crawler:

Lambda function to call the crawler
![lambdacrawler](/lambdacrawler.png)

Glue crawler
![gluecrawler](/gluecrawler.png)

Define the Data Model
The AWS Glue crawler identifies the data model from the files uploaded and inferes the data types:

Glue schema inferred
![glueschema](/glueschema.png)

Run ETL to Model the Data
A transformation script is used in AWS Glue to process the raw data, transform and store in parquet format. In addition an alarm is created to trigger a SNS email notification:

Lamda function to call the ETL job
![lambdaetl](/lambdaetl.png)

Cloudwatch alarm to send the notification
![cloudwatchsns](/cloudwatchsns.png)

Glue ETL job
![glueetl](/glueetl.png)

SNS notification
![sns](/sns.png)

Athena table
![athena](/athena.png)

In case of errors a SQS queue stores the file name for reprocessing:

SQS queue
![sqs](/sqs.png)

Please refer to the screenshots below for the services used:

*Note that given the fact that the data lake exposes the data through parquet files hosted on S3. Such data can be queried using other services like AWS EMR, spark clusters with access to the bucket, among others.

##### Workload scenarios

Q: When the data was increased by 100x, do you store the data in the same way?
A:The AWS technologies used can handle large amounts of data. An increase of 100x the data can be stores with no limitations in S3.
Q: How do you run this pipeline on a daily basis by 7 am every day?
A: The pipeline is automated so that ETL job is executed when a different file is uploaded and does not wait for a specific time. If a scheduler was needed, it can be triggered without an alarm. If the pipeline fails, the queue will store the errors tio be processed one more time
Q: How do you make your database could be accessed by 100+ people? Can you come up with a more cost-effective approach? Does your project need to support 100+ connections at the same time?
A: Since the data is stored in AWS S3 and queried using Athena, it can handle 100+ users. If an RDB is needed. Tha data can be easily migrated to Redshift or RDS.

##### Data Quality checks

The following queries were executed to validate data integrity:

#of rows in PPP table

![rowstableppp](/rowstableppp.png)

#of rows in COVID-19 table

![rowstablecovid](/rowstablecovid.png)

##### Sample analyses

States with the most COVID-19 cases

![statesmostcases](/statesmostcases.png)

States with the most PPP loans

![statesmostloans](/statesmostloans.png)
