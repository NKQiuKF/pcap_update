from flask import render_template
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView, BaseView, expose, has_access
from app import appbuilder, db

import pandas as pd
import json

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""

"""
    Application wide 404 error handler
"""

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

class IpManagerView(BaseView):
    default_view = "panel"

    @expose('/panel')
    @has_access
    def panel(self):
        return self.render_template("ManagingPanel.html")

    @expose('/data')
    @has_access
    def data(self):
        df = pd.read_csv("csv/heatmap.csv")
        df = df[["src_ip"]]
        df.drop_duplicates(["src_ip"])
        return json.dumps({"maskbits": 6, "ipranges": [{"beginip": "10.79.196.0", "endip": "10.79.196.255"}],
            "groupnames": {"10.79.196.0": "Beijing1", "10.79.196.64": "Beijing2", "10.79.196.128": "Tianjin1", "10.79.196.192": "Tianjin2", "-1": "Other"},
            "grouptree": {'text':'Show all', 'nodes':[
                {'text':'Beijing Station', 'nodes':[
                    {'text':'Beijing1'},
                    {'text':'Beijing2'}
                    ]},
                {'text':'Tianjin', 'nodes':[
                    {'text':'Tianjin1'},
                    {'text':'Tianjin2'}
                    ]},
                {'text':'Other'}
                ]},
            "list": df.to_dict(orient='records')})

appbuilder.add_view(IpManagerView, "IP Manager")

db.create_all()


