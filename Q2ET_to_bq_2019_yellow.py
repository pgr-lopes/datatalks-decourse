from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    local_location = f"C:/Users/pelope/OneDrive - Microsoft/Desktop/Projects/Datatalks DE camp/Week2/"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path = local_location)
    return Path(f"{local_location}"+f"{gcs_path}").as_posix()

@task(log_prints=True)
def write_bq(path: Path) -> None:
    """Write DataFrame to BiqQuery"""
    
    df = pd.read_parquet(path)
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    print(f"rows: {len(df)}")

    df.to_gbq(
        destination_table="trips_data_all.yellow_trips",
        project_id="high-electron-375823",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500000,
        if_exists="append",
    )

@flow(log_prints=True)
def etl2019_gcs_bq(year: int, month: int, color: str) -> None:
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs(color, year, month)
    write_bq(path)

@flow(log_prints=True)
def et_yellow_2019_parent_flow(
    months: list[int], year: int, color: str):
    for month in months:
        etl2019_gcs_bq(year, month, color)


if __name__ == "__main__":
    color = "yellow"
    months = [2, 3]
    year = 2019
    et_yellow_2019_parent_flow(months, year, color)
