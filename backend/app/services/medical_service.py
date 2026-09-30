from ..data_loader import hospitals


def find_hospitals(people_affected: int, limit: int = 5):
    df = hospitals()

    available = df[
        df["status"].astype(str).str.lower().isin(
            ["available", "limited"]
        )
    ].copy()

    available = available[
        available["emergency_capacity"] >= people_affected
    ]

    available = available.sort_values(
        by=[
            "average_response_time",
            "emergency_capacity"
        ],
        ascending=[True, False]
    )

    columns = [
        "hospital_id",
        "name",
        "beds",
        "icu",
        "emergency_capacity",
        "status",
        "zone",
        "average_response_time",
        "icu_ratio"
    ]

    return available[columns].head(limit).to_dict(
        orient="records"
    )