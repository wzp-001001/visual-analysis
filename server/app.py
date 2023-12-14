import uuid

from flask import Flask, jsonify, render_template,send_from_directory
from flask_cors import CORS
from markupsafe import Markup
from baidu_migration_scales_route import register_routes
from national_baidu_migration_after import register_routes_national_baidu
from bei_shang_guang_shen_baidu_migration_scale import register_bei_shang_guang_shen_baidu_migration
from flask import send_from_directory
from pyecharts import options as opts
from pyecharts.charts import Bar


app = Flask(__name__, static_folder="templates")


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
register_routes(app)
register_routes_national_baidu(app)
register_bei_shang_guang_shen_baidu_migration(app)
# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

def bar_base() -> Bar:
    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
            .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

@app.route("/bar")
def bar_view():
    c = bar_base()
    return Markup(c.render_embed())

@app.route('/')
def home():
    return render_template('golden_week.html')

@app.route('/golden_week')
def golden_week():
    return render_template('golden_week.html')

@app.route('/metropolis')
def metropolis():
    return render_template('metropolis.html')

@app.route('/emigration')
def emigration():
    return render_template('emigration.html')

@app.route('/immigration')
def immigration():
    return render_template('immigration.html')

@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory('static', filename)

# 添加路由，用于处理字体文件请求
# @app.route('/font/<filename>')
# def font(filename):
#     return send_from_directory('your_font_directory', filename)




if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
