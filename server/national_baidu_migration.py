from flask import jsonify

def register_routes3(app):
    @app.route('/ping3', methods=['GET'])
    def ping_pong3():
        return jsonify('pong3!')