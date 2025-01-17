import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc #combined JS, Py, HTML components
import dash_html_components as html 
import plotly.graph_objs as go 


df_path = r"dfs\us_combined_df.csv"

df = pd.read_csv(df_path, index_col=0)

state_list = df["state"].unique().tolist()
category_list = ['retail_and_recreation', 'grocery_and_pharmacy', 'parks', 'transit_stations', 'workplaces', 'residential', 'outdoor']

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id = "my-dropdown",
            value = "Washington",
            options = [
                {"label": i, "value": i} for i in state_list
            ],

            style=dict(
                width='50%',
                # horizontalAlign="middle",
                # verticalAlign="midde",
                margin=25,
                height="30px",)
        )
    ],
    style={'width': '40%', 'display': 'inline-block', 'font-size':16, }),     

    html.Div([

        dcc.Graph(id="the-graph")
    ]),

    html.Div([            
        dcc.Checklist(
        id='the-checklist',
        value = [],
        labelStyle={'display': 'inline-block'},
        options = [
            {"label":i, "value":i} for i in category_list[:-2]
        ],
        style = dict(
                # width='80%',
                margin=10,))
        ],
    style={'padding-left':250, 'width': '80%', 'display': 'inline-block', 'font-size':16,}),
    ])

@app.callback(
    Output("the-graph", "figure"),
    [Input("my-dropdown", "value"),
    Input("the-checklist", "value")
    ]
    )

def update_text(selected_state, category):
    c_df = df[df["state"] == selected_state]
    
    trace3 = go.Line(x = c_df["date"], y = c_df["residential"], name="residential", line=dict(width=4, color="#E14646"), yaxis="y2")
    trace4 = go.Line(x = c_df["date"], y = c_df["outdoor"], name="outdoor", line=dict(width=4, color="#628A3B"), yaxis="y2")
    
    trace1 = go.Bar(x = c_df["date"], y = c_df["new_case"], marker_color='#A5D8DD', name="new case", opacity=0.65, yaxis="y1")
    trace2 = go.Bar(x = c_df["date"], y = c_df["new_death"], marker_color='lightslategrey', name="new death", opacity=0.7, yaxis="y1")

    traces = [trace1, trace2, trace3, trace4]
    # traces = [trace3, trace4]

    colors = ["#F45C51", "#FBBA18", "#02A699", "#965251", "E38690", "#595BD4", "#87311F"]

    for i, c in enumerate(category):
        traces.append(
            go.Line(x = c_df["date"], y = c_df[c], yaxis="y2", name=c,  line=dict(width=1.5, color=colors[i]))
        )

    return {
        "data": traces,
        "layout": go.Layout(
            barmode="overlay",    
            
            title = "my whatever plot",
            height = 600,
            width = 1200,

            # xaxis=dict(title='Date'),
            yaxis2=dict(title='Mobility', range=[-100, 100], overlaying='y', side='left', showgrid=False),
            yaxis=dict(title='Case Counts', side="right"),

            margin=dict(t=50),
            legend=dict(x=1.05),
        )
    }

if __name__ == "__main__":
    app.run_server(debug=True)
