from ..data_loader import chemicals


def find_chemical_scenarios(chemical_name: str):
    df = chemicals()

    result = df[
        df["chemical"]
        .astype(str)
        .str.lower()
        == chemical_name.lower()
    ].copy()

    if result.empty:
        return {
            "found": False,
            "message": f"No chemical scenario found for {chemical_name}"
        }

    row = result.iloc[0]

    return {
        "found": True,
        "chemical": row["chemical"],
        "release_type": row["release_type"],
        "release_amount_kg": row["release_amount_kg"],
        "release_duration_min": row["release_duration_min"],
        "wind_speed_kmh": row["wind_speed_kmh"],
        "wind_direction": row["wind_direction"],
        "downwind_direction": row["downwind_direction"],
        "atmospheric_stability": row["atmospheric_stability"],
        "yellow_zone_m": row["yellow_zone_m"],
        "orange_zone_m": row["orange_zone_m"],
        "red_zone_m": row["red_zone_m"],
        "recommended_response": row["recommended_response"]
    }