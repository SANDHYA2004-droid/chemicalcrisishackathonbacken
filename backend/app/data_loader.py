from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def load_csv(filename: str) -> pd.DataFrame:
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {file_path}"
        )

    return pd.read_csv(file_path)


def incidents():
    return load_csv("incidents_clean.csv")


def resources():
    return load_csv("resources_clean.csv")


def roads():
    return load_csv("roads_clean.csv")


def roads_with_status():
    return load_csv("roads_merged_status.csv")


def road_status():
    return load_csv("status_latest.csv")


def hospitals():
    return load_csv("hospitals_clean.csv")


def shelters():
    return load_csv("shelters_clean.csv")


def chemicals():
    return load_csv("chemicals_clean.csv")