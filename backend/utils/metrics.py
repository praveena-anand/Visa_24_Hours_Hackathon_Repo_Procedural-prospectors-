def extract_auth_signal(summary):
    stats = summary.get("stats", {})
    decline_mean = stats.get("declined_txns", {}).get("mean", 0)
    return {"auth_decline_mean": decline_mean}


def extract_settlement_signal(summary):
    stats = summary.get("stats", {})
    delay_mean = stats.get("delay_hours", {}).get("mean", 0)
    failed_amt = stats.get("failed_amount", {}).get("mean", 0)
    return {
        "settlement_delay_mean": delay_mean,
        "settlement_failed_amount": failed_amt
    }
