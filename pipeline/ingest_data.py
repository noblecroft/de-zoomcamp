import argparse
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import os

def main(params):
    user = params.pg_user
    password = params.pg_pass
    host = params.pg_host
    port = params.pg_port
    db = params.pg_db
    table_name = params.target_table
    url = params.url

    csv_name = 'output.csv.gz'
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }
    parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

    df_iter = pd.read_csv(
        csv_name,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000
    )

    first_chunk = next(df_iter)
    first_chunk.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
    first_chunk.to_sql(name=table_name, con=engine, if_exists='append')

    for chunk in tqdm(df_iter):
        chunk.to_sql(name=table_name, con=engine, if_exists='append')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    
    parser.add_argument('--pg-user', required=True, help='user name for postgres')
    parser.add_argument('--pg-pass', required=True, help='password for postgres')
    parser.add_argument('--pg-host', required=True, help='host for postgres')
    parser.add_argument('--pg-port', required=True, help='port for postgres')
    parser.add_argument('--pg-db', required=True, help='database name for postgres')
    parser.add_argument('--target-table', required=True, help='name of the table')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()
    main(args)
