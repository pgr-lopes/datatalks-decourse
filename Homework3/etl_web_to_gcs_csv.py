from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from pathlib import Path
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(log_prints=True, retries=3)
def fetch_web(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    #if randint(0, 1) > 0:
    #    raise Exception

    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
    df["dropOff_datetime"] = pd.to_datetime(df["dropOff_datetime"])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as csv file"""
    path = Path(f"C:/Users/pelope/OneDrive - Microsoft/Desktop/Projects/Datatalks DE camp/Week3/data/{dataset_file}.csv")
    df.to_csv(path, compression="gzip")
    return path

@task()
def write_gcs(path: Path, dataset_file: str) -> None:
    """Upload local csv file to GCS"""
    gcs_path = Path(f"data/fhv/{dataset_file}.csv")
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=f"{path}", to_path=gcs_path.as_posix())
    return


@flow()
def etl_web_to_gcs_csv(year: int, month: int) -> None:
    """The main ETL function"""
    dataset_file = f"fhv_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_{year}-{month:02}.csv.gz"

    df = fetch_web(dataset_url)
    #df_clean = clean(df)
    path = write_local(df, dataset_file)
    write_gcs(path, dataset_file)

@flow()
def week3_etl_to_gcs_csv_parent(months: list[int], year: int):
    for month in months:
        etl_web_to_gcs_csv(year, month)


if __name__ == "__main__":
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    year = 2019
    week3_etl_to_gcs_csv_parent(months, year)