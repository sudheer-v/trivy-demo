"""
This Program is test program
handle with care
"""
from __future__ import annotations

import datetime

from dateutil.relativedelta \
    import relativedelta  # pylint: disable=import-error
from google.cloud \
    import bigquery  # pylint: disable=import-error

bq_client = bigquery.Client(project='devops-counsel-demo')

dataset = bigquery.Dataset('devops-counsel-demo.demo_dataset')
dataset.location = 'EU'
dataset.default_table_expiration_ms = 172800000

bq_client.create_dataset(dataset)

schema = [
    bigquery.SchemaField('fruit_name', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('count', 'INTEGER', mode='REQUIRED'),
]
table = bigquery.Table(
    'devops-counsel-demo.demo_dataset.demo_table', schema=schema,
)

bq_client.create_table(table)

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    write_disposition='WRITE_TRUNCATE',
)
with open('fruits.csv', 'rb') as source_file:
    job = bq_client.load_table_from_file(
        source_file,
        'demo_dataset.demo_table', job_config=job_config,
    )

job.result()

table = bq_client.get_table('demo_dataset.demo_table')
print('Loaded number of rows: ' + str(table.num_rows))


today = datetime.date.today()
today_date = datetime.date(day=today.day, month=today.month, year=today.year)
expiry_date = today_date + relativedelta(days=30)
snap_query = f"""
    CREATE SNAPSHOT TABLE IF NOT EXISTS demo_dataset.demo_snapshot
    CLONE demo_dataset.demo_table
    OPTIONS(expiration_timestamp = TIMESTAMP
    "{str(expiry_date)} 00:00:00.00-00:00")
    """

bq_client.query(snap_query)
