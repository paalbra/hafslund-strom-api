#!/usr/bin/env python3
import datetime
import pprint
import time

import hafslund
import influxdb

api = hafslund.HafslundAPI("config.ini")

facilities = api.get_facilities()
meter_point_ids = [facility["meterPointId"] for facility in facilities]

data = []
now = datetime.datetime.now()
to_date = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
from_date = (now - datetime.timedelta(days=8)).strftime("%Y-%m-%d")

for meter_point_id in meter_point_ids:
    consumption_data = []
    response = api.get_consumption(meter_point_id, from_date, to_date, "hourly").json()
    for daily_consumption_data in response:
        daily_consumption_data = daily_consumption_data["consumption"]
        for data_point in daily_consumption_data:
            data_object = {
                "measurement": meter_point_id,
                "time": data_point["timestamp"],
                "fields": {
                    "kWh": data_point["value"]
                }
            }
            data.append(data_object)

pprint.pprint(data)
client = influxdb.InfluxDBClient(host="localhost", port=8086)
client.switch_database("hafslund")
client.write_points(data)
