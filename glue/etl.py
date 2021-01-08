import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "udacitydb", table_name = "udacitydatalake_raws3bucket_1bzpc5li2rs64", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "udacitydb", table_name = "udacitydatalake_raws3bucket_1bzpc5li2rs64", transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("loanamount", "double", "loanamount", "double"), ("businessname", "string", "businessname", "string"), ("address", "string", "address", "string"), ("city", "string", "city", "string"), ("state", "string", "state", "string"), ("zip", "long", "zip", "long"), ("naicscode", "long", "naicscode", "long"), ("businesstype", "string", "businesstype", "string"), ("raceethnicity", "string", "raceethnicity", "string"), ("gender", "string", "gender", "string"), ("veteran", "string", "veteran", "string"), ("nonprofit", "string", "nonprofit", "string"), ("jobsreported", "long", "jobsreported", "long"), ("dateapproved", "string", "dateapproved", "string"), ("lender", "string", "lender", "string"), ("cd", "string", "cd", "string")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("loanamount", "double", "loanamount", "double"), ("businessname", "string", "businessname", "string"), ("address", "string", "address", "string"), ("city", "string", "city", "string"), ("state", "string", "state", "string"), ("zip", "long", "zip", "long"), ("naicscode", "long", "naicscode", "long"), ("businesstype", "string", "businesstype", "string"), ("raceethnicity", "string", "raceethnicity", "string"), ("gender", "string", "gender", "string"), ("veteran", "string", "veteran", "string"), ("nonprofit", "string", "nonprofit", "string"), ("jobsreported", "long", "jobsreported", "long"), ("dateapproved", "string", "dateapproved", "string"), ("lender", "string", "lender", "string"), ("cd", "string", "cd", "string")], transformation_ctx = "applymapping1")
## @type: ResolveChoice
## @args: [choice = "make_struct", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")
## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]
dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")
## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://udacitydatalake-processeds3bucket-15oyrvm2o5is9"}, format = "parquet", transformation_ctx = "datasink4"]
## @return: datasink4
## @inputs: [frame = dropnullfields3]
datasink4 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields3, connection_type = "s3", connection_options = {"path": "s3://udacitydatalake-processeds3bucket-15oyrvm2o5is9"}, format = "parquet", transformation_ctx = "datasink4")
job.commit()
