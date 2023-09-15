import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
import gs_derived
from pyspark.sql import functions as SqlFuncs


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


def sparkAggregate(
    glueContext, parentFrame, groups, aggs, transformation_ctx
) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = (
        parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs)
        if len(groups) > 0
        else parentFrame.toDF().agg(*aggsFuncs)
    )
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3bucket_node1694090244020 = glueContext.create_dynamic_frame.from_catalog(
    database="raw_data",
    table_name="billybees_raws",
    transformation_ctx="S3bucket_node1694090244020",
)

# Script generated for node Amazon S3
AmazonS3_node1694091091069 = glueContext.create_dynamic_frame.from_catalog(
    database="raw_data",
    table_name="salareference_data",
    transformation_ctx="AmazonS3_node1694091091069",
)

# Script generated for node Change Schema
ChangeSchema_node1694090421109 = ApplyMapping.apply(
    frame=S3bucket_node1694090244020,
    mappings=[
        ("location_id", "int", "location_id", "int"),
        ("location_description", "string", "location_description", "string"),
        ("transaction_datetime", "string", "transaction_datetime", "timestamp"),
        ("week_day", "string", "week_day", "string"),
        ("sale_number", "int", "sale_number", "int"),
        ("transaction_type", "string", "transaction_type", "string"),
        ("product_description", "string", "product_description", "string"),
        ("transaction_amount", "double", "transaction_amount", "double"),
        ("payment_type", "string", "payment_type", "string"),
        ("bonus_amount", "double", "bonus_amount", "double"),
        ("ticket_value", "int", "ticket_value", "int"),
    ],
    transformation_ctx="ChangeSchema_node1694090421109",
)

# Script generated for node SQL Query
SqlQuery0 = """
select * from myDataSource where transaction_type not in ('Balance Adjustments', 'Payment','Card Reissue New','Card Reissue Card Swipe Error') AND transaction_amount != 0 AND sale_number !=0
"""
SQLQuery_node1694090619570 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={"myDataSource": ChangeSchema_node1694090421109},
    transformation_ctx="SQLQuery_node1694090619570",
)

# Script generated for node Aggregate
Aggregate_node1694090845564 = sparkAggregate(
    glueContext,
    parentFrame=SQLQuery_node1694090619570,
    groups=[
        "location_id",
        "location_description",
        "transaction_datetime",
        "week_day",
        "sale_number",
        "transaction_type",
        "product_description",
        "payment_type",
        "ticket_value",
    ],
    aggs=[["transaction_amount", "sum"], ["bonus_amount", "sum"]],
    transformation_ctx="Aggregate_node1694090845564",
)

# Script generated for node Join
Join_node1694091170801 = Join.apply(
    frame1=Aggregate_node1694090845564,
    frame2=AmazonS3_node1694091091069,
    keys1=["location_id"],
    keys2=["location_id"],
    transformation_ctx="Join_node1694091170801",
)

# Script generated for node Derived Column
DerivedColumn_node1694092446073 = Join_node1694091170801.gs_derived(
    colName="Bussiness_Datatime",
    expr="CASE     WHEN DATE_FORMAT(transaction_datetime, 'HH:mm:ss') >= '00:00:00' AND DATE_FORMAT(transaction_datetime, 'HH:mm:ss') <= '03:59:59'      THEN DATE_SUB(DATE(transaction_datetime), 1)     ELSE transaction_datetime END AS Bussiness_Datatime",
)

# Script generated for node Derived Column
DerivedColumn_node1694281103555 = DerivedColumn_node1694092446073.gs_derived(
    colName="Hour",
    expr="if(hour(Bussiness_Datatime) = 23, '23:00-00:00', concat(lpad(hour(Bussiness_Datatime), 2, '0'), ':00-', lpad((hour(Bussiness_Datatime) + 1), 2, '0'), ':00'))",
)

# Script generated for node ApplyMapping
ApplyMapping_node1694092716228 = ApplyMapping.apply(
    frame=DerivedColumn_node1694281103555,
    mappings=[
        ("locationclass", "string", "locationclass", "string"),
        ("cityname", "string", "cityname", "string"),
        ("`sum(bonus_amount)`", "double", "bonus_amount", "double"),
        ("product_description", "string", "product_description", "string"),
        ("ticket_value", "int", "ticket_value", "int"),
        ("region", "string", "region", "string"),
        ("week_day", "string", "week_day", "string"),
        ("transaction_datetime", "timestamp", "transaction_datetime", "timestamp"),
        ("location_description", "string", "location_description", "string"),
        ("payment_type", "string", "payment_type", "string"),
        ("locationname", "string", "locationname", "string"),
        ("location_id", "int", "location_id", "int"),
        ("companyname", "string", "companyname", "string"),
        ("`sum(transaction_amount)`", "double", "transaction_amount", "double"),
        ("transaction_type", "string", "transaction_type", "string"),
        ("brandname", "string", "brandname", "string"),
        ("sale_number", "int", "sale_number", "int"),
        ("bussiness_datatime", "timestamp", "bussiness_datatime", "timestamp"),
        ("hour", "string", "hour", "string"),
    ],
    transformation_ctx="ApplyMapping_node1694092716228",
)

# Script generated for node Amazon Redshift
AmazonRedshift_node1694108173144 = glueContext.write_dynamic_frame.from_options(
    frame=ApplyMapping_node1694092716228,
    connection_type="redshift",
    connection_options={
        "postactions": "BEGIN; MERGE INTO public.sample_data_new USING public.sample_data_new_temp_2d4197 ON sample_data_new.location_id = sample_data_new_temp_2d4197.location_id AND sample_data_new.sale_number = sample_data_new_temp_2d4197.sale_number AND sample_data_new.transaction_datetime = sample_data_new_temp_2d4197.transaction_datetime AND sample_data_new.transaction_type = sample_data_new_temp_2d4197.transaction_type AND sample_data_new.product_description = sample_data_new_temp_2d4197.product_description WHEN MATCHED THEN UPDATE SET locationclass = sample_data_new_temp_2d4197.locationclass, cityname = sample_data_new_temp_2d4197.cityname, bonus_amount = sample_data_new_temp_2d4197.bonus_amount, product_description = sample_data_new_temp_2d4197.product_description, ticket_value = sample_data_new_temp_2d4197.ticket_value, region = sample_data_new_temp_2d4197.region, week_day = sample_data_new_temp_2d4197.week_day, transaction_datetime = sample_data_new_temp_2d4197.transaction_datetime, location_description = sample_data_new_temp_2d4197.location_description, payment_type = sample_data_new_temp_2d4197.payment_type, locationname = sample_data_new_temp_2d4197.locationname, location_id = sample_data_new_temp_2d4197.location_id, companyname = sample_data_new_temp_2d4197.companyname, transaction_amount = sample_data_new_temp_2d4197.transaction_amount, transaction_type = sample_data_new_temp_2d4197.transaction_type, brandname = sample_data_new_temp_2d4197.brandname, sale_number = sample_data_new_temp_2d4197.sale_number, bussiness_datatime = sample_data_new_temp_2d4197.bussiness_datatime, hour = sample_data_new_temp_2d4197.hour WHEN NOT MATCHED THEN INSERT VALUES (sample_data_new_temp_2d4197.locationclass, sample_data_new_temp_2d4197.cityname, sample_data_new_temp_2d4197.bonus_amount, sample_data_new_temp_2d4197.product_description, sample_data_new_temp_2d4197.ticket_value, sample_data_new_temp_2d4197.region, sample_data_new_temp_2d4197.week_day, sample_data_new_temp_2d4197.transaction_datetime, sample_data_new_temp_2d4197.location_description, sample_data_new_temp_2d4197.payment_type, sample_data_new_temp_2d4197.locationname, sample_data_new_temp_2d4197.location_id, sample_data_new_temp_2d4197.companyname, sample_data_new_temp_2d4197.transaction_amount, sample_data_new_temp_2d4197.transaction_type, sample_data_new_temp_2d4197.brandname, sample_data_new_temp_2d4197.sale_number, sample_data_new_temp_2d4197.bussiness_datatime, sample_data_new_temp_2d4197.hour); DROP TABLE public.sample_data_new_temp_2d4197; END;",
        "redshiftTmpDir": "s3://aws-glue-assets-735926817203-eu-west-1/temporary/",
        "useConnectionProperties": "true",
        "dbtable": "public.sample_data_new_temp_2d4197",
        "connectionName": "Reshift",
        "preactions": "CREATE TABLE IF NOT EXISTS public.sample_data_new (locationclass VARCHAR, cityname VARCHAR, bonus_amount DOUBLE PRECISION, product_description VARCHAR, ticket_value INTEGER, region VARCHAR, week_day VARCHAR, transaction_datetime TIMESTAMP, location_description VARCHAR, payment_type VARCHAR, locationname VARCHAR, location_id INTEGER, companyname VARCHAR, transaction_amount DOUBLE PRECISION, transaction_type VARCHAR, brandname VARCHAR, sale_number INTEGER, bussiness_datatime TIMESTAMP, hour VARCHAR); DROP TABLE IF EXISTS public.sample_data_new_temp_2d4197; CREATE TABLE public.sample_data_new_temp_2d4197 (locationclass VARCHAR, cityname VARCHAR, bonus_amount DOUBLE PRECISION, product_description VARCHAR, ticket_value INTEGER, region VARCHAR, week_day VARCHAR, transaction_datetime TIMESTAMP, location_description VARCHAR, payment_type VARCHAR, locationname VARCHAR, location_id INTEGER, companyname VARCHAR, transaction_amount DOUBLE PRECISION, transaction_type VARCHAR, brandname VARCHAR, sale_number INTEGER, bussiness_datatime TIMESTAMP, hour VARCHAR);",
    },
    transformation_ctx="AmazonRedshift_node1694108173144",
)

job.commit()
