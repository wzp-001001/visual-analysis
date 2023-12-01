from flask import jsonify
from service.baidu_migration_scale import BaiduMigrationScale


def register_routes(app):

    @app.route('/baidu/baidu_migration_scale', methods=['GET'])
    def all_baidu_migration_scales():
        response_object = {'status': 'success'}
        baiduMigrationScale = BaiduMigrationScale(db_file="./db/migration_scale_index.db")
        print(baiduMigrationScale)
        result_dict = baiduMigrationScale.listAllBaiduMigrationScales(baiduMigrationScale.connection)
        response_object['data'] = result_dict
        return jsonify(response_object)