import pandas as pd

def prepare_time_index(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp").sort_index()
    return df


def calculate_daily_totals(df):
    daily = df["kwh"].resample("D").sum().reset_index()
    daily.rename(columns={"kwh": "daily_kwh"}, inplace=True)
    return daily


def calculate_weekly_aggregates(df):
    weekly = df["kwh"].resample("W").agg(["sum", "mean", "max"]).reset_index()
    weekly.rename(columns={
        "sum": "weekly_total_kwh",
        "mean": "weekly_avg_kwh",
        "max": "weekly_peak_kwh"
    }, inplace=True)
    return weekly


def building_wise_summary(df):
    summary = (
        df.groupby("building")["kwh"]
        .agg(["sum", "mean", "min", "max"])
        .reset_index()
    )
    summary.rename(columns={
        "sum": "total_kwh",
        "mean": "avg_kwh",
        "min": "min_kwh",
        "max": "max_kwh"
    }, inplace=True)
    return summary
