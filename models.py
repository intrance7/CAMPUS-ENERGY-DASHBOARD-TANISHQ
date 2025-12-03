class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"{self.name}: Total Consumption = {total:.2f} kWh"


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def get_or_create_building(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def load_from_dataframe(self, df):
        for _, row in df.iterrows():
            building_obj = self.get_or_create_building(row["building"])
            reading = MeterReading(row["timestamp"], row["kwh"])
            building_obj.add_reading(reading)

    def overall_report(self):
        lines = []
        for building in self.buildings.values():
            lines.append(building.generate_report())
        return "\n".join(lines)
