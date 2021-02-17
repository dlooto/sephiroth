import os
import json
import time
import datetime

import requests
import MySQLdb
import schedule

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DEVICE_META_PATH = os.path.join(PROJECT_DIR, 'device_meta.json')


class Retransmission:
    '''
    device_meta = [
        {
            "id": 15,
            "table_name": "hpic_rec",
            "data_type":"data",
            "transform_meta": [
                ("Doserate", "doserate"),
            ]
        }
    ]
    '''

    def __init__(self, debug=False):
        self.debug = debug
        if self.debug:
            self.db_params = {
                'host': '127.0.0.1',
                'user': 'root',
                'passwd': 'root',
                'db': 'scada',
                'charset': 'utf8',
            }
        else:
            self.db_params = {
                'host': '127.0.0.1',
                'user': 'root',
                'passwd': 'root',
                'db': 'scada',
                'charset': 'utf8',
            }
        with open(DEVICE_META_PATH, 'r') as json_file:
            self.device_meta = json.load(json_file)

    def get_db(self):
        db = MySQLdb.connect(**self.db_params)
        return db

    def transform_datas(self, rows, transform_meta):
        datas = {}
        for idx, row in enumerate(rows):
            for source, target in transform_meta:
                if source not in row:
                    continue

                value = row[source]
                if isinstance(value, datetime.datetime):
                    value = round(value.timestamp())
                datas['data[%s][%s]' % (idx, target)] = str(value)

        return datas

    def transform_file_datas(self, device_id, rows):
        datas = []
        for row in rows:
            filename = os.path.basename(row['Path'])
            data = {
                'device': device_id,
                'sid': row['Sid'],
                'data_time': row['Time'].strftime('%Y-%m-%d %H:%M:%S'),
                'start_time': row['StartTime'].strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': row['EndTime'].strftime('%Y-%m-%d %H:%M:%S'),
                'file_name': filename,
                'origin_file_path': row['Path'],
            }
            datas.append(data)
        return datas

    def get_db_datas(self, device_info, timestamp_points):
        start_time, end_time = (
            datetime.datetime.fromtimestamp(timestamp_points[0]).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.datetime.fromtimestamp(timestamp_points[-1]).strftime('%Y-%m-%d %H:%M:%S'),
        )
        table = device_info['table_name']
        db = self.get_db()
        with db:
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'select * from %s where time between "%s" and "%s"' % (table, start_time, end_time)
            )
            rows = cursor.fetchall()
        return rows

    def send(self, device_id, missing_datas):
        url = 'http://platform.scarletsun.wang/api/v1/receive/device/data/%s/' % device_id
        try:
            resp = requests.post(url, data=missing_datas)
            print(resp.json())
        except Exception as e:
            print(e)

    def upload_files(self, datas):
        for data in datas:
            print(data)
            filepath = data.pop('origin_file_path')
            api = 'http://platform.scarletsun.wang/api/v1/device/hpge/upload/'
            with open(filepath, 'rb') as file:
                try:
                    resp = requests.post(api, params=data, files={'file': file})
                    print(resp.status_code)
                except Exception as e:
                    print(e)

    def retransmission(self, device_info):
        url = 'http://platform.scarletsun.wang/api/v1/device/data/retransmission/%s/fetch_history/' % device_info['id']
        try:
            resp = requests.get(url)
            ret = resp.json()
            print(ret)
        except Exception as e:
            print(e)
            return None

        timestamp_points = ret.get('data', {}).get('timePoints', [])
        if not timestamp_points:
            return None

        rows = self.get_db_datas(device_info, timestamp_points)
        if not rows:
            return None

        data_type = device_info['data_type']
        if data_type == 'data':
            datas = self.transform_datas(rows, device_info['transform_meta'])
            self.send(device_info['id'], datas)
        if data_type == 'file':
            datas = self.transform_file_datas(device_info['id'], rows)
            self.upload_files(datas)

    def check(self):
        for device_info in self.device_meta:
            print(device_info)
            try:
                self.retransmission(device_info)
            except Exception as e:
                print(e)

    def upload_hpge_file(self):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(seconds=60*60*4)
        timepoints = [
            start_time.timestamp(),
            end_time.timestamp(),
        ]

        for device_info in self.device_meta:
            if device_info['data_type'] != 'file':
                continue

            print(device_info)
            try:
                rows = self.get_db_datas(device_info, timepoints)
                datas = self.transform_file_datas(device_info['id'], rows)
                self.upload_files(datas)
            except Exception as e:
                print(e)

    def send_hpge_status_data(self):
        end_time = datetime.datetime.now()
        start_time = datetime.datetime(end_time.year, end_time.month, end_time.day)

        timepoints = [
            start_time.timestamp(),
            end_time.timestamp(),
        ]

        for device_info in self.device_meta:
            if device_info['table_name'] != 'hpge_nuclide_rec':
                continue

            print(device_info)
            try:
                rows = self.get_db_datas(device_info, timepoints)
                datas = self.transform_datas(rows, device_info['transform_meta'])
                self.send(device_info['id'], datas)
            except Exception as e:
                print(e)


def retransmission_task():
    task = Retransmission()
    task.check()


def upload_hpge_file_task():
    task = Retransmission()
    task.upload_hpge_file()


def send_hpge_status_data_task():
    task = Retransmission()
    task.send_hpge_status_data()


schedule.every(1).minutes.do(retransmission_task)
schedule.every(2).hours.do(upload_hpge_file_task)
schedule.every(3).hours.do(send_hpge_status_data_task)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
