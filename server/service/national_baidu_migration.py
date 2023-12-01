from .db_service import DbImpl


class NationalBaiduMigration(DbImpl):
    def __init__(self, db_file):
        super().__init__(db_file)