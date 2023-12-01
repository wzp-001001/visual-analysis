from .db_service import DbImpl

class BeiShangGuangShenBaiduMigration(DbImpl):
    def __init__(self, db_file):
        super().__init__(db_file)