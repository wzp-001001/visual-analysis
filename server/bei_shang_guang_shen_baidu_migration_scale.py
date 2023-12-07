import json
from flask import Flask, render_template
from pyecharts.charts import Geo, Timeline
from pyecharts import options as opts
from pyecharts.globals import ChartType
from service.bei_shang_guang_shen_baidu_migration import BeiShangGuangShenBaiduMigration
from pyecharts.charts import Geo, Timeline
from pyecharts import options as opts


def register_bei_shang_guang_shen_baidu_migration(app):
    def _bei_shang_guang_shen_baidu_migration():
        # 定义参数列表
        cities = ['北京', '上海', '广州', '深圳']
        dates = [20230930, 20231001, 20231002, 20231003, 20231004, 20231005, 20231006, 20231007]
        move_types = ['迁入', '迁出']

        # 存储图表 HTML 的列表
        chart_html_list = []

        # 遍历所有组合
        for city in cities:
            for move_type in move_types:
                for date in dates:
                    # 实例化 BeiShangGuangShenBaiduMigration 类
                    migration_instance = BeiShangGuangShenBaiduMigration(db_file="./db/migration_scale_index.db")
                    if move_type == "迁入":
                        # 调用 get_city_numbers 方法
                        city_nums_in, start_end_in = migration_instance.get_in_city_numbers(city, date, move_type)
                        # 创建地图
                        geo = (
                            Geo(init_opts=opts.InitOpts(width="1000px", height="600px", theme="wonderland"))
                            .add_schema(maptype="china",  # 地图
                                        zoom=4.5,
                                        is_roam=True,
                                        center=Geo().get_coordinate(city),  # 视角中心
                                        itemstyle_opts=opts.ItemStyleOpts(color="#28527a",
                                                                          border_color="#9ba4b4"))
                            # 4.添加数据
                            .add('', data_pair=city_nums_in, color='white')
                            .add('', data_pair=start_end_in, type_="lines", label_opts=opts.LabelOpts(is_show=False),
                                 effect_opts=opts.EffectOpts(symbol="arrow",
                                                             color='red',
                                                             symbol_size=8))
                            .set_global_opts(
                                title_opts=opts.TitleOpts(title=f"各个地区迁入到{city}",
                                                          subtitle=f"迁徙时间:{date}"),
                                visualmap_opts=opts.VisualMapOpts(min_=0, max_=15))
                        )
                        # 渲染图表并将 HTML 字符串添加到列表
                        chart_html_list.append(geo.render_embed().strip('\n'))

                    elif move_type == "迁出":
                        city_nums_out, start_end_out = migration_instance.get_out_city_numbers(city, date, move_type)

                        geo = (
                            Geo(init_opts=opts.InitOpts(width="1000px", height="600px", theme="wonderland"))
                            .add_schema(maptype="china",  # 地图
                                        zoom=4.5,
                                        is_roam=True,
                                        center=Geo().get_coordinate(city),  # 视角中心
                                        itemstyle_opts=opts.ItemStyleOpts(color="#28527a",
                                                                          border_color="#9ba4b4"))
                            # 4.添加数据
                            .add('', data_pair=city_nums_out, color='white')
                            .add('', data_pair=start_end_out, type_="lines", label_opts=opts.LabelOpts(is_show=False),
                                 effect_opts=opts.EffectOpts(symbol="arrow",
                                                             color='red',
                                                             symbol_size=8))
                            .set_global_opts(
                                title_opts=opts.TitleOpts(title=f"从{city}迁入到各个地区", subtitle=f"迁徙时间:{date}"),
                                visualmap_opts=opts.VisualMapOpts(min_=0, max_=15))
                        )
                        # 渲染图表并将 HTML 字符串添加到列表
                        # chart_html = geo.render_embed().strip('\n')
                        chart_html = geo.render_embed()
                        chart_html_list.append(chart_html)



        main_template = """
            <html>
            <head>
                <!-- 引入必要的 CSS 和 JavaScript -->
            </head>
            <body>
                <!-- Insert Charts Here -->
            </body>
            </html>
            """
        combined_html = ''.join(chart_html_list)
        # combined_html = main_template.replace('<!-- Insert Charts Here -->', ''.join(chart_html_list))
        return combined_html

    @app.route('/BSGS')
    def get_data_htmls():
        combined_chart_html = _bei_shang_guang_shen_baidu_migration()
        return combined_chart_html
