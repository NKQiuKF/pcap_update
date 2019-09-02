#coding:utf-8
#from superset.data import *
"""conn.log中每一条代表一次完整的连接，包含多个包"""
import sys
#sys.path.append("../../")
import os
import pandas as pd
from superset.data import *
from geoip import geolite2
import hashlib
from get_province import get_province_code

FilePath = os.path.join('/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-2]),'web/file')
BroPath =  os.path.join(os.path.dirname(os.path.abspath(__file__)),'bro')
os.chdir(BroPath)

def sha256(filename):
    sha256Obj = hashlib.sha256()
    with open(filename,'rb') as f:
       sha256Obj.update(f.read())
    return sha256Obj.hexdigest()

def get_pcap_info(f):
    pcap_analysis=[]
    pcap = os.path.join(FilePath,f)
    slug = sha256(pcap)
    os.popen('mv '+pcap+' '+BroPath)
    os.popen('bro -C -r '+f)
    df_conn = pd.read_csv("conn.log",skiprows=8,skipfooter=1,
                sep=r"\t",engine='python')
    df_conn.drop(df_conn.columns[-1],axis=1,inplace=True)
    df_conn.columns = ['time', 'id', 'orig_h',
                       'orig_p', 'resp_h', 'resp_p',
                       'proto', 'service', 'duration',
                       'orig_bytes', 'resp_bytes',
                       'conn_state', 'local_orig',
                       'local_resp', 'missed_bytes',
                       'history','orig_pkts',
                       'orig_ip_bytes',
                       'resp_pkts',
                        'tunnel_parents']
    df_conn.sort_values(['time'],ascending=True,inplace=True)
    df_conn['temporary'] = df_conn['resp_h'].apply(geolite2.lookup)
    #CCA2
    df_conn['country'] = df_conn['temporary'].apply(
            lambda x:'local' if not x else x.country
            )
    df_conn['continent'] = df_conn['temporary'].apply(
            lambda x:'local' if not x else x.continent
            )
    df_conn['Lat'] = df_conn['temporary'].apply(
            lambda x:'None' if not x else x.location[0]
            )
    df_conn['Lng'] = df_conn['temporary'].apply(
            lambda x:'None'if not x else x.location[1]
            )
    del df_conn['temporary'] 
    f = os.path.splitext(f)[0]
    f = f.replace('-','_')
    for col in df_conn.columns[1:]:
        df_conn[col] = df_conn[col].apply(lambda x: x if x!='-' else 0)
    df_conn['service'] = df_conn['service'].apply(lambda x:x if x!=0 else 'Unknown')
    df_conn.time = pd.to_datetime(df_conn['time'],unit='s')
    df_conn['date'] = df_conn['time']
    df_conn['allbytes']=df_conn['orig_bytes']+df_conn['resp_bytes']
    df_conn.to_sql(
                f,
                db.engine,
                if_exists='replace',
                chunksize=500,
                dtype={
                    'time':DateTime(),
                    'date':Date(),
                    'id':String(),
                    'orig_p':String(),
                    'orig_h':String(),
                    'resp_h':String(),
                    'resp_p':String(),
                    'proto':String(),
                    'service':String(),     
                    'duration':Float(),
                    'orig_bytes':Float(),
                    'resp_bytes':Float(),
                    'conn_state':String(),
                    'local_orig':String(),
                    'local_resp':String(),
                    'missed_bytes':Float(),
                    'history':String(),
                    'orig_pkts':BigInteger(),
                    'orig_ip_bytes':BigInteger(),
                    'resp_pkts':BigInteger(),
                    'tunnel_parents':BigInteger(),
                    'country':String(),
                    'allbytes':Float(),
                    },
                index=False
                )
    tbl = db.session.query(TBL).filter_by(table_name=f).first()
    if not tbl:
        tbl = TBL(table_name=f)
    tbl.database = get_or_create_main_db()
    tbl.description = "Pcap Connection Info"
    tbl.filter_select_enabled = True
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()

    defaults = {
            "bottom_margin":"auto",
            "viz_type":'table',
            "since":"100 years ago",
            "until":'',
            "show_controls":True,
            }

    slc=Slice(
            slice_name=f+u'_table',
            viz_type='table',
            datasource_type='table',
            datasource_id=tbl.id,
            params=get_slice_json(
                defaults,
                page_length=50,
                row_limit=None,
                table_filter=True,
                metrics=[],
                all_columns=[u'time', u'id', u'orig_h', u'orig_p', u'resp_h', u'resp_p', u'proto',
                u'service', u'duration', u'orig_bytes', u'resp_bytes', u'conn_state',
                u'local_orig', u'local_resp', u'missed_bytes', u'history', u'orig_pkts',
                u'orig_ip_bytes', u'resp_pkts', u'tunnel_parents','country'],
                include_search=True,

            )
        )
    pcap_analysis.append(slc.slice_name)
    merge_slice(slc)

    slc=Slice(
            slice_name=f+u'_目的端口',
            viz_type='pie',
            datasource_type='table',
            datasource_id=tbl.id,
            params=get_slice_json(
                defaults,
                viz_type='pie',
                groupby=['resp_p'],
                metrics=['count'],
                donut=True,
                show_legend=False,
                labels_outside=False,
            )
        )
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)

    slc=Slice(
            slice_name=f+u'_发送流量',
            viz_type='sankey',
            datasource_type='table',
            datasource_id=tbl.id,
            params=textwrap.dedent("""\
            {
            "having": "", 
            "slice_id": 432, 
            "viz_type": "sankey", 
            "row_limit": 50000, 
            "metric": "sum__orig_bytes", 
            "since": "100 years ago", 
            "until": "", 
            "where": "", 
            "datasource": "33__table", 
            "filters": [], 
            "color_scheme": "bnbColors", 
            "granularity_sqla": "time", 
            "time_grain_sqla": "Time Column", 
            "groupby": ["service", "country"]
            }
            """)
            )
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)
    

    slc=Slice(
            slice_name=f+u'_对应日期',
            viz_type='sankey',
            datasource_type='table',
            datasource_id=tbl.id,
            params=textwrap.dedent("""\
            {
            "having": "", 
            "slice_id": 432, 
            "viz_type": "sankey", 
            "row_limit": 50000, 
            "metric": "sum__orig_bytes", 
            "since": "100 years ago", 
            "until": "", 
            "where": "", 
            "datasource": "33__table", 
            "filters": [], 
            "color_scheme": "bnbColors", 
            "granularity_sqla": "time", 
            "time_grain_sqla": "Time Column", 
            "groupby": ["service", "date"]
            }
            """),
            )
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)

    slc=Slice(
            slice_name=f+u'_源端口_发送与接收',
            viz_type='dist_bar',
            datasource_type='table',
            datasource_id=tbl.id,
            params=textwrap.dedent("""\
                    {"bottom_margin": "auto", "y_axis_label": "", "row_limit": 10, "show_legend": true, "filters": [], "show_controls": true, "granularity_sqla": "time", "viz_type": "dist_bar", "since": "100 years ago", "x_axis_label": "", "order_bars": false, "color_scheme": "d3Category10", "until": "", "columns": ["proto"], "show_bar_value": false, "y_axis_format": ".3s", "metrics": ["sum__orig_bytes", "sum__resp_bytes"], "slice_id": 458, "where": "", "reduce_x_ticks": false, "groupby": ["orig_h"], "datasource": "34__table", "contribution": false, "time_grain_sqla": null, "having": "", "bar_stacked": true}
                    """
            ))
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)

    slc=Slice(
            slice_name=f+u'_目的端口_发送与接收',
            viz_type='dist_bar',
            datasource_type='table',
            datasource_id=tbl.id,
            params=textwrap.dedent("""\
                    {"bottom_margin": "auto", "y_axis_label": "", "row_limit": 10, "show_legend": true, "filters": [], "show_controls": true, "granularity_sqla": "time", "viz_type": "dist_bar", "since": "100 years ago", "x_axis_label": "", "order_bars": false, "color_scheme": "d3Category10", "until": "", "columns": ["proto"], "show_bar_value": false, "y_axis_format": ".3s", "metrics": ["sum__orig_bytes", "sum__resp_bytes"], "slice_id": 458, "where": "", "reduce_x_ticks": false, "groupby": ["resp_h"], "datasource": "34__table", "contribution": false, "time_grain_sqla": null, "having": "", "bar_stacked": true}
                    """
            ))
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)

    slc=Slice(
            slice_name=f+u'_服务_发送与接收',
            viz_type='dist_bar',
            datasource_type='table',
            datasource_id=tbl.id,
            params=textwrap.dedent("""\
                    {"bottom_margin": "auto", "y_axis_label": "", "row_limit": 10, "show_legend": true, "filters": [], "show_controls": true, "granularity_sqla": "time", "viz_type": "dist_bar", "since": "100 years ago", "x_axis_label": "", "order_bars": false, "color_scheme": "d3Category10", "until": "", "columns": [], "show_bar_value": false, "y_axis_format": ".3s", "metrics": ["sum__orig_bytes", "sum__resp_bytes"], "slice_id": 463, "where": "", "reduce_x_ticks": false, "groupby": ["service"], "datasource": "34__table", "contribution": false, "time_grain_sqla": null, "having": "", "bar_stacked": true}
                    """
            ))
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)

    slc=Slice(
            slice_name=f+u'_国家_发送与接收',
            viz_type='dist_bar',
            datasource_type='table',
            datasource_id=tbl.id,
            params=textwrap.dedent("""\
                    {"bottom_margin": "auto", "y_axis_label": "", "row_limit": 10, "show_legend": true, "filters": [], "show_controls": true, "granularity_sqla": "time", "viz_type": "dist_bar", "since": "100 years ago", "x_axis_label": "", "order_bars": false, "color_scheme": "d3Category10", "until": "", "columns": [], "show_bar_value": false, "y_axis_format": ".3s", "metrics": ["sum__orig_bytes", "sum__resp_bytes"], "slice_id": 463, "where": "", "reduce_x_ticks": false, "groupby": ["country"], "datasource": "34__table", "contribution": false, "time_grain_sqla": null, "having": "", "bar_stacked": true}
                    """
            ))
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)

    slc=Slice(
            slice_name=f+u'_Duration时间',
            viz_type='treemap',
            datasource_type='table',
            datasource_id=tbl.id,
            params=textwrap.dedent("""\
                    {"having": "", "slice_id": 463, "viz_type": "treemap", "where": "", "since": "100 years ago", "until": "", "metrics": ["sum__duration"], "datasource": "34__table", "filters": [], "color_scheme": "bnbColors", "granularity_sqla": "time", "treemap_ratio": 1.618033988749895, "time_grain_sqla": "Time Column", "groupby": ["service"], "number_format": ".3s"}
                    """
            ))
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)

    slc=Slice(
            slice_name=f+u'_气泡图',
            viz_type='bubble',
            datasource_type='table',
            datasource_id=tbl.id,
            params=textwrap.dedent("""\
            {"bottom_margin": "auto", "y_axis_label": "\u63a5\u6536\u5305", "series": "proto", "entity": "service", "show_legend": true, "filters": [], "granularity_sqla": "time", "size": "sum__allbytes", "viz_type": "bubble", "since": "100 years ago", "x_axis_label": "\u53d1\u9001\u5305", "color_scheme": "bnbColors", "y_axis_format": ".3s", "y_axis_showminmax": true, "x_axis_format": ".3s", "left_margin": "auto", "where": "", "until": "", "y_log_scale": false, "datasource": "34__table", "x_axis_showminmax": true, "y": "sum__resp_pkts", "x": "sum__orig_pkts", "x_log_scale": false, "time_grain_sqla": "Time Column", "having": "", "max_bubble_size": "100"}
            """
                )
            )
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)

    slc=Slice(
            slice_name=f+u'_流量力导向图',
            viz_type='directed_force',
            datasource_type='table',
            datasource_id=tbl.id,
            params=textwrap.dedent("""\
           {"link_length": "150", "slice_id": 2, "viz_type": "directed_force", "row_limit": 50, "metric": "sum__allbytes", "since": "", "until": "now", "where": "", "charge": "-500", "groupby": ["orig_h", "resp_h"], "datasource": "34__table", "filters": [], "granularity_sqla": "time", "time_grain_sqla": "Time Column", "having": ""}
            """
                )
            )
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)

    slc=Slice(
            slice_name=f+u'_过滤器',
            viz_type='filter_box',
            datasource_type='table',
            datasource_id=tbl.id,
            params=textwrap.dedent("""\
            {"having": "", "slice_id": 406, "show_sqla_time_granularity": false, "viz_type": "filter_box", "where": "", "metric": "sum__duration", "since": "100 years ago", "until": "", "show_druid_time_origin": false, "groupby": ["orig_h", "orig_p", "resp_h", "resp_p", "proto", "service", "country"], "datasource": "35__table", "filters": [], "show_druid_time_granularity": false, "granularity_sqla": "time", "show_sqla_time_column": false, "time_grain_sqla": "Time Column", "date_filter": true, "instant_filtering": true}
            """
                )
            )
    merge_slice(slc)
    pcap_analysis.append(slc.slice_name)

    def draw_map():
        df_map = df_conn[df_conn['country']!='local']
        df_map.to_sql(
                    f+'_map',
                    db.engine,
                    if_exists='replace',
                    chunksize=500,
                    dtype={
                        'time':DateTime(),
                        'date':Date(),
                        'id':String(),
                        'allbytes':Float(),
                        'orig_p':String(),
                        'orig_h':String(),
                        'resp_h':String(),
                        'resp_p':String(),
                        'proto':String(),
                        'service':String(),     
                        'duration':Float(),
                        'orig_bytes':Float(),
                        'resp_bytes':Float(),
                        'conn_state':String(),
                        'local_orig':String(),
                        'local_resp':String(),
                        'missed_bytes':Float(),
                        'history':String(),
                        'orig_pkts':BigInteger(),
                        'orig_ip_bytes':BigInteger(),
                        'resp_pkts':BigInteger(),
                        'tunnel_parents':BigInteger(),
                        'country':String(),
                        'Lat':Float(),
                        'Lng':Float()
                        },
                    index=False
                    )

        tbl = db.session.query(TBL).filter_by(table_name=f+'_map').first()
        if not tbl:
            tbl = TBL(table_name=f+'_map')
        tbl.database = get_or_create_main_db()
        tbl.description = "Pcap Connection Map Info"
        tbl.filter_select_enabled = True
        db.session.merge(tbl)
        db.session.commit()
        tbl.fetch_metadata()
        slc=Slice(
                slice_name=f+u'_WorldMap',
                viz_type='world_map',
                datasource_type='table',
                datasource_id=tbl.id,
                params=textwrap.dedent("""\
                {"since": "100 years ago", "having": "", "viz_type": "world_map", "slice_id": 531, "where": "", "metric": "sum__duration", "show_bubbles": true, "entity": "country", "country_fieldtype": "cca2", "datasource": "35__table", "filters": [], "secondary_metric": "sum__allbytes", "granularity_sqla": "time", "time_grain_sqla": "Time Column", "until": "", "max_bubble_size": "25"} 
                """
                    )
                )
        merge_slice(slc)
        pcap_analysis.append(slc.slice_name)


    draw_map()

    print("Creating a Pcap Analysis dashboard")
    dash_name = f+"_Analysis"
    dash = db.session.query(Dash).filter_by(slug=slug).first()

    if not dash:
        dash = Dash()

    js = textwrap.dedent("""\
            [
                {
                        "col": 1, 
                                "row": 97, 
                                        "size_x": 47, 
                                                "size_y": 19, 
                                                        "slice_id": "433"
                                                            
                }, 
        {
                "col": 37, 
                        "row": 0, 
                                "size_x": 12, 
                                        "size_y": 17, 
                                                "slice_id": "434"
                                                    
        }, 
        {
                "col": 34, 
                        "row": 116, 
                                "size_x": 15, 
                                        "size_y": 28, 
                                                "slice_id": "435"
                                                    
        }, 
        {
                "col": 33, 
                        "row": 144, 
                                "size_x": 16, 
                                        "size_y": 16, 
                                                "slice_id": "436"
                                                    
        }, 
        {
                "col": 17, 
                        "row": 129, 
                                "size_x": 16, 
                                        "size_y": 14, 
                                                "slice_id": "437"
                                                    
        }, 
        {
                "col": 1, 
                        "row": 129, 
                                "size_x": 16, 
                                        "size_y": 14, 
                                                "slice_id": "438"
                                                    
        }, 
        {
                "col": 15, 
                        "row": 116, 
                                "size_x": 17, 
                                        "size_y": 13, 
                                                "slice_id": "439"
                                                    
        }, 
            {
                    "col": 1, 
                            "row": 116, 
                                    "size_x": 14, 
                                            "size_y": 12, 
                                                    "slice_id": "440"
                                                        
            }, 
                {
                        "col": 33, 
                                "row": 160, 
                                        "size_x": 16, 
                                                "size_y": 16, 
                                                        "slice_id": "441"
                                                            
                }, 
                    {
                            "col": 1, 
                                    "row": 143, 
                                            "size_x": 32, 
                                                    "size_y": 16, 
                                                            "slice_id": "442"
                                                                
                    }, 
                        {
                                "col": 1, 
                                        "row": 159, 
                                                "size_x": 32, 
                                                        "size_y": 16, 
                                                                "slice_id": "443"
                                                                    
                        }, 
                            {
                                    "col": 1, 
                                            "row": 0, 
                                                    "size_x": 9, 
                                                            "size_y": 15, 
                                                                    "slice_id": "444"
                                                                        
                            }, 
                                {
                                        "col": 10, 
                                                "row": 0, 
                                                        "size_x": 27, 
                                                                "size_y": 18, 
                                                                        "slice_id": "445"
                                                                            
                                }

    ]
    """)
    l = json.loads(js)
    slices = (
            db.session.query(Slice).filter(Slice.slice_name.in_(
                pcap_analysis)).all()
            )
#    slices = sorted(slices,key=lambda x:x.id)
    for i,pos in enumerate(l):
        pos['slice_id'] = str(slices[i].id)
        dash.dashboard_title = dash_name
        dash.position_json = json.dumps(l, indent=4)
        dash.slug = slug

        dash.slices = slices
        db.session.merge(dash)
        db.session.commit()

def main():
    while True:
        file_list = os.listdir(FilePath)
        for f in file_list:
            if os.path.splitext(f)[-1]!='.pcap':
                continue
            else:
                get_pcap_info(f)
                os.popen("rm -f "+BroPath+'/*.log')
    
if __name__=='__main__':
    main()
