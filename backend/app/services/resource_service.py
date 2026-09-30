from ..data_loader import resources


def find_available_resources(
    incident_type: str | None = None,
    limit: int = 10
):
    df = resources()

    # Only genuinely available resources
    available = df[
        (df["availability_flag"] == 1) &
        (df["status"].str.lower() == "available")
    ].copy()

    # Prefer communication-ready resources
    available["communication_score"] = (
        available["communications_status"]
        .astype(str)
        .str.lower()
        .eq("online")
        .astype(int)
    )

    # Rank resources
    available = available.sort_values(
        by=[
            "readiness_score",
            "communication_score",
            "response_time"
        ],
        ascending=[False, False, True]
    )

    columns = [
        "resource_id",
        "type",
        "location",
        "capacity",
        "response_time",
        "distance_km",
        "readiness_score",
        "priority",
        "communications_status"
    ]

    return available[columns].head(limit).to_dict(
        orient="records"
    )