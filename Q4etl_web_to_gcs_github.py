from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    # if randint(0, 1) > 0:
    #     raise Exception
    df = pd.read_csv(dataset_url)
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"C:/Users/pelope/OneDrive - Microsoft/Desktop/Projects/Datatalks DE camp/Week2/data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    print(f"rows: {len(df)}")
    return path


@task()
def write_gcs(path: Path, color: str, dataset_file: str) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_path = Path(f"data/{color}/{dataset_file}.parquet")
    gcs_block.upload_from_path(from_path=path, to_path=gcs_path.as_posix())
    return


@flow()
def etl_web_to_gcs_green(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    path = write_local(df, color, dataset_file)
    print(f"rows: {len(df)}")
    write_gcs(path, color, dataset_file)


@flow()
def github_flow_green(
    months: list[int], year: int, color: str):
    for month in months:
        etl_web_to_gcs_green(year, month, color)


if __name__ == "__main__":
    color = "green"
    months = [11]
    year = 2020
    github_flow_green(months, year, color)
