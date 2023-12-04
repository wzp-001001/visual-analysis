# from pyecharts import options as opts
# from pyecharts.charts import Geo, Timeline
# from pyecharts.globals import ThemeType, ChartType
# from service.national_baidu_migration import NationalBaiduMigration
#
#
# def generate_migration_chart():
#     # 创建 NationalBaiduMigration 实例
#     migration_instance = NationalBaiduMigration(db_file="server/db/migration_scale_index.db")
#     result_dict = migration_instance.list_national_baidu_migration(conn=migration_instance.connection)
#
#     # 将结果字典转换为 DataFrame
#     df1 = migration_instance.to_dataframe(result_dict)
#
#     # 创建时间轴
#     timeline = Timeline(init_opts=opts.InitOpts(width="1200px", height="700px", theme=ThemeType.DARK))
#
#     for i in [20230927, 20230928, 20230929, 20230930, 20231001, 20231002, 20231003, 20231004, 20231005, 20231006,
#               20231007, 20231008]:
#         df_in = df1[(df1["year"] == str(i)) & (df1["type_name"] == "迁入")]
#
#         # 创建 Geo 散点图
#         c_chart = (
#             Geo()
#             .add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(color="#28527a", border_color="#9ba4b4"))
#             .add(
#                 "",
#                 [(city, value) for city, value in zip(df_in['city_name'], df_in['value'])],
#                 type_=ChartType.EFFECT_SCATTER,
#                 effect_opts=opts.EffectOpts(symbol_size=2)
#             )
#             .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#             .set_global_opts(
#                 title_opts=opts.TitleOpts(title="2023中秋国庆-全国热门迁入地(目的地)",
#                                           pos_left='center',
#                                           subtitle=f'迁徙日期:{i}'),
#                 visualmap_opts=opts.VisualMapOpts(
#                     range_text=['迁徙比例', ''],
#                     split_number=5,
#                     pos_left='20%',
#                     pos_top='70%',
#                     is_piecewise=True,
#                     pieces=[
#                         {"min": 0.1, "max": 0.5, "color": "#32e0c4"},
#                         {"min": 0.5, "max": 1, "color": "#b8de6f"},
#                         {"min": 1, "max": 1.5, "color": "#fd8c04"},
#                         {"min": 1.5, "max": 2, "color": "#ec5858"},
#                         {"min": 2, "color": "#5a191b"},
#                     ]
#                 )
#             )
#         )
#
#         timeline.add(c_chart, str(i) + '日')
#
#     timeline.add_schema(
#         play_interval=1500,
#         is_timeline_show=True,
#         is_auto_play=False,
#         pos_left="0",
#         pos_right="0"
#     )
#
#     return timeline
# national_baidu_migration_after.py
from service.national_baidu_migration import NationalBaiduMigration
import json
from flask import Flask, render_template
from pyecharts.charts import Geo, Timeline
from pyecharts import options as opts
from pyecharts.globals import ChartType
from flask import Flask, render_template
from pyecharts.charts import Geo, Timeline
from pyecharts import options as opts
from pyecharts.globals import ChartType

def register_routes_national_baidu(app):
    def get_migration_data():
        date_list = [20230927, 20230928, 20230929, 20230930, 20231001, 20231002, 20231003, 20231004, 20231005, 20231006,
                     20231007, 20231008]

        # 创建 NationalBaiduMigration 实例
        migration_instance = NationalBaiduMigration(db_file="server/db/migration_scale_index.db")
        result_dict = migration_instance.list_national_baidu_migration(conn=migration_instance.connection)

        # 将结果字典转换为 DataFrame
        df1 = migration_instance.to_dataframe(result_dict)

        # 数据筛选
        filtered_data = []
        for i in date_list:
            df_in = df1[(df1["year"] == i) & (df1["type_name"] == "迁入")]
            filtered_data.append(df_in.to_json(orient='records'))

        return filtered_data





    def get_datas_html():
        json_data_list = get_migration_data()  # 包含 JSON 字符串的列表

        timeline = Timeline()
        for i, json_data in enumerate(json_data_list):
            day_data = json.loads(json_data)

            # 假设 day_data 包含 year 字段
            year = day_data[0]['year'] if day_data else "Unknown Year"
            geo_chart = (
                Geo()
                .add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(color="#568bf5", border_color="#d5d6d8"))
                .add("", [(city['city_name'], city['value']) for city in day_data], type_=ChartType.EFFECT_SCATTER)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                    visualmap_opts=opts.VisualMapOpts(
                        min_=min(city['value'] for city in day_data),
                        max_=max(city['value'] for city in day_data),
                        range_color=["yellow", "red"],
                        is_calculable=True
                    ),
                    title_opts=opts.TitleOpts(
                        title="2023中秋国庆-全国热门迁入地(目的地)",
                        pos_left='center')
                )
            )
            timeline.add(geo_chart, f'{year}日')

        timeline.add_schema(
            orient="h",  # 设置为水平方向
            is_auto_play=True,
            is_inverse=False,  # 设置为 False
            play_interval=2000,
            width="80%",  # 调整宽度
            pos_bottom="3%",  # 设置在图例的下面，减小距离
            label_opts=opts.LabelOpts(is_show=True, color="#aaa", interval=0, font_size=10)  # 调整间隔、字体大小和居中对齐
        )

        chart_html = timeline.render_embed()
        return chart_html


    @app.route('/national_baidu_migration')
    def get_data_htmls():
        chart_html = get_datas_html()
        return render_template('index.html', chart_html=chart_html)

