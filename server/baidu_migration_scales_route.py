from flask import jsonify
from service.baidu_migration_scale import BaiduMigrationScale
import pyecharts.options as opts
from pyecharts.charts import Line
from markupsafe import Markup

def register_routes(app):

    def line_base(x_data,y_data_1,y_data_2,y_data_3) -> Line:
        return (
            Line()
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="2021年",
                y_axis=y_data_1,
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name="2022年",
                y_axis=y_data_2,
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name="2023年",
                y_axis=y_data_3,
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="黄金周前后迁徙趋势(万人)"),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            )
        )

    @app.route('/baidu/baidu_migration_scale', methods=['GET'])
    def all_baidu_migration_scales():
        baiduMigrationScale = BaiduMigrationScale(db_file="./db/migration_scale_index.db")
        result_dict = baiduMigrationScale.listAllBaiduMigrationScales(baiduMigrationScale.connection)
        c = line_base(result_dict['month_day'],result_dict['2021'],result_dict['2022'],result_dict['2023'])
        return Markup(c.render_embed())