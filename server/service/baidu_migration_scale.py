from .db_service import DbImpl


class BaiduMigrationScale(DbImpl):

    def __init__(self, db_file):
        super().__init__(db_file)

    # List all info.
    def listAllBaiduMigrationScales(self, conn):
        result_dict = {}
        with conn:
            sql = '''
                    SELECT * FROM baidu_migration_scale_index
                    where date between 20230901 and 20231015
                    or date between 20220901 and 20221015
                    or date between 20210901 and 20211015
                  '''
            cur = conn.cursor()
            cur.execute(sql)
            result_set = cur.fetchall()
            for result in result_set:
                date_int = result[0]
                year = str(date_int)[0:4]
                if year in result_dict:
                    # 如果这个键不在字典中，创建一个新的列表并添加这个元组（去掉第三个元素）
                    result_dict[year].append((result[0], result[1]))
                else:
                    result_dict[year] = [(result[0], result[1])]
        return result_dict

# baiduMigrationScale = BaiduMigrationScale(db_file="../db/migration_scale_index.db")
# result_dict = baiduMigrationScale.listAllBaiduMigrationScales(baiduMigrationScale.connection)
# print(result_dict)
