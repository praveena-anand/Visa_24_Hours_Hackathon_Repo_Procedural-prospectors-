def detect_anomalies(summary):
    anomalies = []

    stats = summary.get("stats", {})

    if "declined_txns" in stats:
        mean_decline = stats["declined_txns"].get("mean", 0)
        if mean_decline and mean_decline > 500:
            anomalies.append(
                f"High average authorization declines detected ({mean_decline:.0f})"
            )

    if "delay_hours" in stats:
        mean_delay = stats["delay_hours"].get("mean", 0)
        if mean_delay and mean_delay > 5:
            anomalies.append(
                f"Settlement delays unusually high (avg {mean_delay:.1f} hrs)"
            )

    if not anomalies:
        anomalies.append("No significant anomalies detected")

    return anomalies
