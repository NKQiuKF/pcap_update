#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
import pandas as pd
import networkx as nx
from networkx.readwrite import json_graph
import json
app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('/templates/MySocket.html')
@app.route('/getdata/')
def get_data():
    datafile=pd.read_csv("csv/heatmap.csv")
    print(datafile['src_ip'][0])
    rl_columns=['src_ip','dst_ip']
    rl=datafile[rl_columns].dropna()
    print(rl['src_ip'][0])
    g = nx.Graph()
    src_ips=rl['src_ip']
    for src_ip in src_ips:
        if src_ip not in g:
            g.add_node(src_ip, dict(
                name=src_ip))
    i=0
    while(i<len(rl)):
        print(rl['src_ip'][i])
        if rl['src_ip'][i] in g:
            if rl['dst_ip'][i] in g:
                new_edge=(rl['src_ip'][i],rl['dst_ip'][i])
                if new_edge not in g.edges():
                    g.add_edge(rl['src_ip'][i],rl['dst_ip'][i])
        i+=1
    d=json_graph.node_link_data(g)
    return json.dumps(d)
#     json.dump(d,open('force/force.json','w'))
#     return json.dumps('/force/force.json')
@socketio.on('client_event')
def client_msg(msg):
    emit('server_response', {'data': 'hello'+msg['data']})
    
@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': 'hello'+msg['data']})

@app.route('/graph')
def opengraph():
    return render_template('/templates/MyGraph.html')



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=8080)
    
    
    
    
    
    
    
    