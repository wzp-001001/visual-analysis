from .db_service import DbImpl
import pandas as pd


class BeiShangGuangShenBaiduMigration(DbImpl):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.df = self.load_data()

    def load_data(self):
        result_dict = self.list_national_baidu_migration()
        df = self.to_dataframe(result_dict)
        return df

    def list_national_baidu_migration(self):
        result_dict = {}  # 使用字典替代列表
        with self.create_connection():
            sql = '''
            SELECT city_name, province_name, value, date, type_name, area
            FROM bei_shang_guang_shen_baidu_migration_scale
            WHERE date IN ('20230927', '20230928', '20230929', '20230930', '20231001', '20231002', '20231003', '20231004', '20231005', '20231006', '20231007', '20231008')
            '''
            cur = self.conn.cursor()
            cur.execute(sql)
            result_set = cur.fetchall()
            for result in result_set:
                city_name = result[0]
                result_dict.setdefault(city_name, []).append({
                    'city_name': result[0],
                    'province_name': result[1],
                    'value': result[2],
                    'date': result[3],
                    'type_name': result[4],
                    'area': result[5]
                })
        return result_dict

    def to_dataframe(self, result_dict):
        # 将字典的值转换为平铺的列表
        adjusted_data = [item for sublist in result_dict.values() for item in sublist]

        # 将平铺的列表转换为 DataFrame
        df = pd.DataFrame(adjusted_data, columns=['city_name', 'province_name', 'value', 'date', 'type_name', 'area'])
        return df

    def get_in_city_numbers(self, city, date, move_type):
        filtered_data = self.df[
            (self.df["area"] == city) & (self.df["date"] == date) & (self.df["type_name"] == move_type)]
        city_nums_out = list(zip(filtered_data['city_name'], filtered_data['value']))
        start_end_out = [(j, city) for j in filtered_data['city_name']]
        return city_nums_out, start_end_out

    def get_out_city_numbers(self, city, date, move_type):
        filtered_data = self.df[
            (self.df["area"] == city) & (self.df["date"] == date) & (self.df["type_name"] == move_type)]
        city_nums_in = list(zip(filtered_data['city_name'], filtered_data['value']))
        start_end_in = [(city, j) for j in filtered_data['city_name']]
        return city_nums_in, start_end_in
