from ..data_loader import shelters


def find_shelters(people_affected: int, limit: int = 5):
    df = shelters()

    available = df[
        (df["status"].astype(str).str.lower() == "available") &
        (df["available_beds"] > 0)
    ].copy()

    available = available.sort_values(
        by=[
            "available_beds",
            "staff_count"
        ],
        ascending=[False, False]
    )

    result = []

    remaining = people_affected

    for _, row in available.iterrows():

        if remaining <= 0:
            break

        beds = int(row["available_beds"])

        allocation = min(
            beds,
            remaining
        )

        result.append({
            "shelter_id": row["shelter_id"],
            "name": row["name"],
            "available_beds": beds,
            "allocated_people": allocation,
            "status": row["status"],
            "supply_level": row["supply_level"],
            "staff_count": row["staff_count"]
        })

        remaining -= allocation

    return {
        "requested_people": people_affected,
        "allocated_people": people_affected - remaining,
        "unallocated_people": remaining,
        "shelters": result
    }