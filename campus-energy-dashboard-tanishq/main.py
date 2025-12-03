import os
import pandas as pd
from pathlib import Path

from analysis import (
    prepare_time_index,
    calculate_daily_totals,
    calculate_weekly_aggregates,
    building_wise_summary
)

from visualize import create_dashboard
from models import BuildingManager


def load_data(data_dir="data"):
    data_path = Path(data_dir)
    all_files = list(data_path.glob("*.csv"))

    df_list = []
    error_log = []

    for csv_file in all_files:
        try:
            df = pd.read_csv(csv_file)

            # Add building name if not present
            if "building" not in df.columns:
                df["building"] = csv_file.stem

            # Ensure timestamp column exists and convert
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
            else:
                raise Exception("Timestamp column missing in file.")

            df_list.append(df)

        except Exception as e:
            error_log.append(f"Error in {csv_file}: {e}")

    if df_list:
        df_combined = pd.concat(df_list, ignore_index=True)
    else:
        df_combined = pd.DataFrame()

    return df_combined, error_log


def generate_text_summary(df, building_summary, path="output/summary.txt"):
    # Always reset index so timestamp becomes a column
    df = df.reset_index()

    total_campus = df["kwh"].sum()

    highest_row = building_summary.loc[building_summary["total_kwh"].idxmax()]
    top_building = highest_row["building"]
    top_building_kwh = highest_row["total_kwh"]

    peak_idx = df["kwh"].idxmax()
    peak_time = df.loc[peak_idx, "timestamp"]
    peak_value = df.loc[peak_idx, "kwh"]

    with open(path, "w") as f:
        f.write("Campus Energy Consumption Summary\n")
        f.write("================================\n\n")
        f.write(f"Total campus consumption: {total_campus:.2f} kWh\n")
        f.write(f"Highest-consuming building: {top_building} ({top_building_kwh:.2f} kWh)\n")
        f.write(f"Peak load time: {peak_time} with {peak_value:.2f} kWh\n")


def main():
    os.makedirs("output", exist_ok=True)

    print("Loading data...")
    df_combined, errors = load_data()

    if errors:
        print("Errors while reading files:")
        for err in errors:
            print(" -", err)

    if df_combined.empty:
        print("No data loaded. Exiting...")
        return

    print("Processing data...")

    # Keep DatetimeIndex for resampling
    df_combined = prepare_time_index(df_combined)

    # Daily / weekly with timestamp as index
    daily = calculate_daily_totals(df_combined)
    weekly = calculate_weekly_aggregates(df_combined)
    summary = building_wise_summary(df_combined)

    print("Creating visual dashboard...")
    create_dashboard(daily, weekly, summary)

    print("Saving output files...")
    df_combined.reset_index().to_csv("output/cleaned_energy_data.csv", index=False)
    summary.to_csv("output/building_summary.csv", index=False)

    generate_text_summary(df_combined, summary)

    print("\nAll tasks completed successfully!")

    # OOP REPORT — needs timestamp as column
    df_for_oop = df_combined.reset_index()

    manager = BuildingManager()
    manager.load_from_dataframe(df_for_oop)

    print("\n=== OOP Building Report ===")
    print(manager.overall_report())


if __name__ == "__main__":
    main()
