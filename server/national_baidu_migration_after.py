# national_baidu_migration_after.py
from service.national_baidu_migration import NationalBaiduMigration
import json
from flask import Flask, render_template
from pyecharts.charts import Geo, Timeline
from pyecharts import options as opts
from pyecharts.globals import ChartType
from markupsafe import Markup

def register_routes_national_baidu(app):
    def get_migration_dataru():
        date_list = [20230927, 20230928, 20230929, 20230930, 20231001, 20231002, 20231003, 20231004, 20231005, 20231006,
                     20231007, 20231008]

        # 创建 NationalBaiduMigration 实例
        migration_instance = NationalBaiduMigration(db_file="./db/migration_scale_index.db")
        result_dict = migration_instance.list_national_baidu_migration()

        # 将结果字典转换为 DataFrame
        df1 = migration_instance.to_dataframe(result_dict)

        # 数据筛选
        filtered_data = []
        for i in date_list:
            df_in = df1[(df1["year"] == i) & (df1["type_name"] == "迁入")]
            filtered_data.append(df_in.to_json(orient='records'))

        return filtered_data

    def get_migration_datachu():
        date_list = [20230927, 20230928, 20230929, 20230930, 20231001, 20231002, 20231003, 20231004, 20231005, 20231006,
                     20231007, 20231008]

        # 创建 NationalBaiduMigration 实例
        migration_instance = NationalBaiduMigration(db_file="./db/migration_scale_index.db")
        result_dict = migration_instance.list_national_baidu_migration()

        # 将结果字典转换为 DataFrame
        df1 = migration_instance.to_dataframe(result_dict)

        # 数据筛选
        filtered_data = []
        for i in date_list:
            df_in = df1[(df1["year"] == i) & (df1["type_name"] == "迁出")]
            filtered_data.append(df_in.to_json(orient='records'))

        return filtered_data

    def get_datas_html_qianru():
        json_data_list = get_migration_dataru()  # 包含 JSON 字符串的列表

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

    def get_datas_html_qianchu():
        json_data_list = get_migration_datachu()  # 包含 JSON 字符串的列表

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
                        title="2023中秋国庆-全国热门迁出地(出发地)",
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

    @app.route('/national_baidu_migration1')
    def get_data_htmls1():
        chart_html_ru = get_datas_html_qianru()
        # return render_template('../client/src/templates/index.html', chart_html=chart_html)
        return Markup(chart_html_ru)

    @app.route('/national_baidu_migration2')
    def get_data_htmls2():
        chart_html_chu = get_datas_html_qianchu()
        # return render_template('../client/src/templates/index.html', chart_html=chart_html)
        return Markup(chart_html_chu)
