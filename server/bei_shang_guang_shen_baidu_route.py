from flask import jsonify

def register_routes2(app):
    @app.route('/ping2', methods=['GET'])
    def ping_pong2():
        return jsonify('pong2!')