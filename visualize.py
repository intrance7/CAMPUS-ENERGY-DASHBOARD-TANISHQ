import matplotlib.pyplot as plt

def create_dashboard(daily_df, weekly_df, building_summary,
                     output_path="output/dashboard.png"):

    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # 1. Daily line chart
    ax1 = axes[0]
    ax1.plot(daily_df["timestamp"], daily_df["daily_kwh"])
    ax1.set_title("Daily Energy Consumption (Campus)")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("kWh")

    # 2. Bar chart (average consumption per building)
    ax2 = axes[1]
    ax2.bar(building_summary["building"], building_summary["avg_kwh"])
    ax2.set_title("Average Consumption Per Building")
    ax2.set_xlabel("Building")
    ax2.set_ylabel("Avg kWh")
    ax2.tick_params(axis="x", rotation=45)

    # 3. Scatter plot (peak consumption)
    ax3 = axes[2]
    ax3.scatter(building_summary["building"], building_summary["max_kwh"])
    ax3.set_title("Peak Consumption Per Building")
    ax3.set_xlabel("Building")
    ax3.set_ylabel("Peak kWh")
    ax3.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
