from ..data_loader import roads_with_status


def get_safe_roads(limit: int = 20):
    df = roads_with_status()

    safe = df[
        (df["blocked_binary"] == 0) &
        (df["status"].astype(str).str.lower() != "blocked") &
        (df["emergency_access"] == 1)
    ].copy()

    safe = safe.sort_values(
        by=[
            "road_risk_score",
            "traffic_score",
            "distance_km"
        ],
        ascending=[True, True, True]
    )

    columns = [
        "road_id",
        "from_node",
        "to_node",
        "distance_km",
        "road_type",
        "traffic_score",
        "emergency_access",
        "road_risk_score",
        "status",
        "traffic_level"
    ]

    return safe[columns].head(limit).to_dict(
        orient="records"
    )