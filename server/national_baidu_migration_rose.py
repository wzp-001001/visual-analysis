import pandas as pd
import json
import seaborn as sns
from service.national_baidu_migration import NationalBaiduMigration
import matplotlib
matplotlib.use('Agg')  # 避免 Matplotlib 警告
from matplotlib.ticker import MaxNLocator
from flask import Flask, render_template, Markup
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie, Timeline
import base64
def  register_routes_national_baidu_rose(app):
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
    def aggregate_migration_data_out(json_data_list):
        aggregated_data = {}

        for json_data in json_data_list:
            try:
                day_data = json.loads(json_data)
            except json.JSONDecodeError:
                # 处理JSON解析错误，可以记录日志或者采取其他适当的措施
                continue

            for city_data in day_data:
                city_name = city_data.get("city_name")
                value = city_data.get("value")

                if city_name is not None and value is not None:
                    if city_name not in aggregated_data:
                        aggregated_data[city_name] = 0

                    aggregated_data[city_name] += value

        return aggregated_data
    def aggregate_migration_data_in(json_data_list):
        aggregated_data = {}

        for json_data in json_data_list:
            try:
                day_data = json.loads(json_data)
            except json.JSONDecodeError:
                # 处理JSON解析错误，可以记录日志或者采取其他适当的措施
                continue

            for city_data in day_data:
                city_name = city_data.get("city_name")
                value = city_data.get("value")

                if city_name is not None and value is not None:
                    if city_name not in aggregated_data:
                        aggregated_data[city_name] = 0

                    aggregated_data[city_name] += value

        return aggregated_data
    def plot_migration_rose_qianchu():
        json_data_list = get_migration_datachu()
        aggregated_data = aggregate_migration_data_out(json_data_list)

        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(list(aggregated_data.items()), columns=['城市', '数值'])

        # Sort the DataFrame based on the '数值' column in descending order
        df_sorted = df.sort_values(by='数值', ascending=False)

        # Select only the first fifty cities
        df_sorted_top50 = df_sorted.head(50)

        # Define your own color scheme
        mode = [
            "#A6CEE3",
            "#1F78B4",
            "#B2DF8A",
            "#33A8FF",
            "#E31A1C",
            "#FF7F00",
            "#27AE60",
            "#D62728",
            "#9467BD",
            "#8C564B",
            "#E79C00",
            "#8DD3C7",
            "#B8860B",
            "#7AC5CD",
            "#99D5BD",
            "#CCEBC5",
            "#D9D9D9",
            "#C0C0C0",
            "#808080",
            "#555555",
            "#000000",
            "#FF0000",
            "#00FF00",
            "#0000FF",
            "#FFFF00",
            "#FF00FF",
            "#00FFFF",
            "#800000",
            "#008000",
            "#000080",
            "#808000",
            "#008080",
            "#800080",
            "#F00000",
            "#00F000",
            "#0000F0",
            "#F08000",
            "#00F080",
            "#F000F0",
        ]
        pie = Pie(init_opts=opts.InitOpts(width='1000px', height='800px', bg_color='white'))
        pie.add(
            '', [list(z) for z in zip(df_sorted_top50['城市'], df_sorted_top50['数值'])],
            radius=['10%', '70%'], center=['50%', '50%'], rosetype="radius"
        ).set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)".format, is_show=True, position="inside",
                                      font_size=10),
        ).set_global_opts(
            title_opts=opts.TitleOpts(
                                      title_textstyle_opts=opts.TextStyleOpts(color='black', font_size=16)),
            legend_opts=opts.LegendOpts(is_show=True, pos_top='bottom', orient='horizontal')
        ).set_colors(mode)

        # Render the pie chart to embedded HTML
        chart_html = pie.render_embed()

        return Markup(chart_html)

    def plot_migration_rose_qianru():
        json_data_list = get_migration_dataru()
        aggregated_data = aggregate_migration_data_in(json_data_list)

        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(list(aggregated_data.items()), columns=['城市', '数值'])

        # Sort the DataFrame based on the '数值' column in descending order
        df_sorted = df.sort_values(by='数值', ascending=False)

        # Select only the first fifty cities
        df_sorted_top50 = df_sorted.head(50)

        # Define your own color scheme
        mode = [
            "#A6CEE3",
            "#1F78B4",
            "#B2DF8A",
            "#33A8FF",
            "#E31A1C",
            "#FF7F00",
            "#27AE60",
            "#D62728",
            "#9467BD",
            "#8C564B",
            "#E79C00",
            "#8DD3C7",
            "#B8860B",
            "#7AC5CD",
            "#99D5BD",
            "#CCEBC5",
            "#D9D9D9",
            "#C0C0C0",
            "#808080",
            "#555555",
            "#000000",
            "#FF0000",
            "#00FF00",
            "#0000FF",
            "#FFFF00",
            "#FF00FF",
            "#00FFFF",
            "#800000",
            "#008000",
            "#000080",
            "#808000",
            "#008080",
            "#800080",
            "#F00000",
            "#00F000",
            "#0000F0",
            "#F08000",
            "#00F080",
            "#F000F0",
        ]

        pie = Pie(init_opts=opts.InitOpts(width='1000px', height='800px', bg_color='white'))
        pie.add(
            '', [list(z) for z in zip(df_sorted_top50['城市'], df_sorted_top50['数值'])],
            radius=['10%', '70%'], center=['50%', '50%'], rosetype="radius"
        ).set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)".format, is_show=True, position="inside",
                                      font_size=10),
        ).set_global_opts(
            title_opts=opts.TitleOpts(
                                      title_textstyle_opts=opts.TextStyleOpts(color='black', font_size=16)),
            legend_opts=opts.LegendOpts(is_show=True, pos_top='bottom', orient='horizontal')
        ).set_colors(mode)

        # Render the pie chart to embedded HTML
        chart_html = pie.render_embed()

        return Markup(chart_html)

    @app.route('/rose_migration1')
    def get_data_rose_in():
        chart_html = plot_migration_rose_qianru()
        return render_template('t1.html', chart_html=chart_html)

    @app.route('/rose_migration2')
    def get_data_rose_2():
        chart_html = plot_migration_rose_qianchu()
        return render_template('t2.html', chart_html=chart_html)