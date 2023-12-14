import json
from flask import Flask, render_template, request
from markupsafe import Markup
from service.bei_shang_guang_shen_baidu_migration import BeiShangGuangShenBaiduMigration
from pyecharts.charts import Geo, Timeline
from pyecharts import options as opts


def register_bei_shang_guang_shen_baidu_migration(app):
    def _bei_shang_guang_shen_baidu_migration(request):
        # 获取请求中的 JSON 数据
        data = request.get_json()
        city = data.get('cities')
        date = int(data.get('datas'))
        move_type = data.get('move_types')
        # cities = ['北京', '上海', '广州', '深圳']
        # dates = [20230930, 20231001, 20231002, 20231003, 20231004, 20231005, 20231006, 20231007]
        # move_types = ['迁入', '迁出']

        # 存储图表 HTML 的列表
        print(date, city, move_type)
        # 遍历所有组合
        # 实例化 BeiShangGuangShenBaiduMigration 类
        migration_instance = BeiShangGuangShenBaiduMigration(db_file="./db/migration_scale_index.db")

        if move_type == "迁入":
            color = "#e1519e"
            color2 = "#bde2ff"
            city_nums_in, start_end_in = migration_instance.get_in_city_numbers(city, date, move_type)
            # 创建地图
            print(city_nums_in, start_end_in)

            geo = (
                Geo(init_opts=opts.InitOpts(width="1000px", height="600px"))
                .add_schema(maptype="china",  # 地图
                            zoom=4.5,
                            is_roam=True,
                            center=Geo().get_coordinate(city),  # 视角中心
                            itemstyle_opts=opts.ItemStyleOpts(color=color2,
                                                              border_color="white"))
                # 4.添加数据
                .add('', data_pair=city_nums_in, color='white')
                .add('', data_pair=start_end_in, type_="lines", label_opts=opts.LabelOpts(is_show=False, color=""),
                     effect_opts=opts.EffectOpts(symbol="arrow",
                                                 color=color,
                                                 symbol_size=8))
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=f"各个地区迁入到{city}",
                                              subtitle=f"迁徙时间:{date}"),
                    visualmap_opts=opts.VisualMapOpts(min_=0, max_=3, range_color=["white", "black"]))
            )
            # 渲染图表并将 HTML 字符串添加到列表
            return Markup(geo.render_embed())

        elif move_type == "迁出":
            color = "#1fb257"
            color2 = "#db9e9e"
            city_nums_out, start_end_out = migration_instance.get_out_city_numbers(city, date, move_type)
            print(city_nums_out, start_end_out)
            geo = (
                Geo(init_opts=opts.InitOpts(width="1000px", height="600px"))
                .add_schema(maptype="china",  # 地图
                            zoom=4.5,
                            is_roam=True,
                            center=Geo().get_coordinate(city),  # 视角中心
                            itemstyle_opts=opts.ItemStyleOpts(color=color2,
                                                              border_color="black"))
                # 4.添加数据
                .add('', data_pair=city_nums_out, color='white')
                .add('', data_pair=start_end_out, type_="lines", label_opts=opts.LabelOpts(is_show=False),
                     effect_opts=opts.EffectOpts(symbol="arrow",
                                                 color=color,
                                                 symbol_size=8))
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=f"从{city}迁入到各个地区", subtitle=f"迁徙时间:{date}"),
                    visualmap_opts=opts.VisualMapOpts(min_=0, max_=3, range_color=["white", "black"]))
            )
            # 渲染图表并将 HTML 字符串添加到列表

            return Markup(geo.render_embed())

    @app.route('/BSGS', methods=['POST'])
    def get_data_htmls():
        combined_chart_html = _bei_shang_guang_shen_baidu_migration(request)
        # combined_chart_html = combined_chart_html.replace('https://assets.pyecharts.org/assets/v5/echarts.min.js',"static/layui.js")\
        #     .replace('https://assets.pyecharts.org/assets/v5/maps/china.js',"static/china.js")\
        #     .replace('https://assets.pyecharts.org/assets/v5/themes/wonderland.js',"static/china.js")
        #
        return combined_chart_html
