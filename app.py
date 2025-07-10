from flask import Flask
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import json
import plotly.express as px
from datetime import datetime, timedelta
import os

# Initialize Flask
server = Flask(__name__)

# Initialize Dash
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    update_title=None
)

# Layout
app.layout = dbc.Container([
    html.H1("Network Traffic Anomaly Detection", className="my-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Traffic Overview"),
                dbc.CardBody([
                    dcc.Graph(id='traffic-pie-chart')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Risk Score Timeline"),
                dbc.CardBody([
                    dcc.Graph(id='risk-timeline')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Recent Traffic Logs"),
                dbc.CardBody([
                    html.Div(id='logs-table')
                ])
            ])
        ])
    ]),
    
    dcc.Interval(
        id='interval-component',
        interval=2000,  # in milliseconds
        n_intervals=0
    )
])

def load_logs():
    if not os.path.exists("logs/traffic_log.json"):
        return pd.DataFrame()
    
    logs = []
    try:
        with open("logs/traffic_log.json", "r") as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        log_entry = json.loads(line)
                        logs.append(log_entry)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing line: {line}")
                        print(f"Error details: {str(e)}")
                        continue
    except Exception as e:
        print(f"Error reading log file: {str(e)}")
        return pd.DataFrame()
    
    if not logs:
        return pd.DataFrame()
    
    return pd.DataFrame(logs)

@app.callback(
    [Output('traffic-pie-chart', 'figure'),
     Output('risk-timeline', 'figure'),
     Output('logs-table', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    try:
        # Load logs
        df = load_logs()
        if df.empty:
            # Return empty figures and message
            empty_fig = px.pie(values=[], names=[])
            empty_fig.update_layout(title="No data available")
            return empty_fig, empty_fig, "No logs available"
        
        # Convert timestamp to datetime with proper format
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601')
        
        # Create pie chart
        tag_counts = df['tag'].value_counts()
        pie_fig = px.pie(
            values=tag_counts.values,
            names=tag_counts.index,
            title="Traffic Distribution",
            color_discrete_map={'Normal': 'green', 'Anomaly': 'red'}
        )
        
        # Create timeline
        timeline_fig = px.scatter(
            df.sort_values('timestamp').tail(50),
            x='timestamp',
            y='risk_score',
            color='tag',
            title="Risk Score Timeline",
            color_discrete_map={'Normal': 'green', 'Anomaly': 'red'}
        )
        timeline_fig.update_layout(yaxis_range=[0, 1])
        
        # Create table
        table = dbc.Table([
            html.Thead(html.Tr([
                html.Th("Timestamp"),
                html.Th("Source IP"),
                html.Th("Destination Port"),
                html.Th("Packet Size"),
                html.Th("Risk Score"),
                html.Th("Tag")
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')),
                    html.Td(row['src_ip']),
                    html.Td(row['dst_port']),
                    html.Td(row['packet_size']),
                    html.Td(f"{row['risk_score']:.2f}"),
                    html.Td(html.Span(row['tag'], style={
                        'color': 'red' if row['tag'] == 'Anomaly' else 'green'
                    }))
                ]) for _, row in df.sort_values('timestamp', ascending=False).head(10).iterrows()
            ])
        ], bordered=True, hover=True)
        
        return pie_fig, timeline_fig, table
    except Exception as e:
        print(f"Error in callback: {str(e)}")
        empty_fig = px.pie(values=[], names=[])
        empty_fig.update_layout(title="Error loading data")
        return empty_fig, empty_fig, f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=8051)
