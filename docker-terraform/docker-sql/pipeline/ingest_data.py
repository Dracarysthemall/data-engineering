#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

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

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


def ingest_data(
    url: str,
    engine,
    target_table: str,
    chunksize: int = 100000,
                            ) :
    if url.endswith(".csv") or url.endswith(".csv.gz"):
        df_iter = pd.read_csv(
            url,
            dtype=dtype, # type: ignore
            parse_dates=parse_dates,
            iterator=True,
            chunksize=chunksize
        ) # type: ignore

        first_chunk = next(df_iter)

        first_chunk.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists="replace"
        )

        first_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )

        for chunk in tqdm(df_iter):
            chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists="append"
            )
        print(f"Inserted chunk: {len(chunk)}") 
    elif url.endswith(".parquet"):
        df = pd.read_parquet(url)

        df.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists="replace"
        )

        df.to_sql(
            name=target_table,
            con=engine,
            if_exists="append",
            chunksize=chunksize
        )

    print(f'done ingesting to {target_table}')

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--url', default=None, type=str, help='Full link to download data')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
def main(pg_user, pg_pass, pg_host, pg_port, pg_db,url, year, month, chunksize, target_table):

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'

    if url is None : 
        url = f'{url_prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz'

    ingest_data(
        url=url,
        engine=engine,
        target_table=target_table,
        chunksize=chunksize
    )

if __name__ == '__main__':
    main()