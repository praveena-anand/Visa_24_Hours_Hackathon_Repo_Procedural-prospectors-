import pandas as pd

def understand_report(path):
    df = pd.read_csv(path)

    summary = {
        "columns": list(df.columns),
        "rows": len(df),
        "stats": df.describe(include="all").fillna("").to_dict(),
        "sample_rows": df.head(5).to_dict(orient="records")
    }

    return summary
