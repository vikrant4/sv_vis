import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


# Loading data
transaction_data = pd.read_excel(
    'Transactions Gippsland modified NC.xlsx', sheet_name=1)
transfer_data = pd.read_excel(
    'Transactions Gippsland modified NC.xlsx', sheet_name=2)
disposal_data = pd.read_excel(
    'Transactions Gippsland modified NC.xlsx', sheet_name=3)
transaction_out_index = transaction_data['INNOUTUT'] == 'OUT'
transaction_out_data = transaction_data.loc[transaction_out_index, :]


def get_location(name, type):
    """
    Return (lat, lon) tuple of a facility
    name: Name of the facility
    type: 'transfer' or 'disposal'
    """
    if type == 'transfer':
        location_index = transfer_data['Facilty Name'] == name
        return (
            transfer_data.loc[location_index, 'Latitude'].values[0],
            transfer_data.loc[location_index, 'Longitude'].values[0]
        )
    elif type == 'disposal':
        location_index = disposal_data['Disposal Facility'] == name
        return (
            disposal_data.loc[location_index, 'DF Latitude'].values[0],
            disposal_data.loc[location_index, 'DF Longitude'].values[0]
        )


# Basic dash app setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
mapbox_access_token = 'pk.eyJ1IjoidmlrcmFudDQiLCJhIjoiY2p0YzRocm44MHNxdzN6b2E1dm9wMjF2cCJ9.VrFaPJ36LG0Vzjlw1zSPTg'
latInitial = -38.30366863
lonInitial = 145.55121652
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1('Flow of waste material'),
    dcc.Graph(
        id='map-graph',
        figure=go.Figure(
            data=[
                # Plotting Transfer stastions
                go.Scattermapbox(
                    mode='markers',
                    hoverinfo='text',
                    text=transfer_data['Facilty Name'],
                    lat=transfer_data['Latitude'],
                    lon=transfer_data['Longitude'],
                    marker=dict(size=9)
                ),
                # Plotting Disposal facilities
                go.Scattermapbox(
                    mode='markers',
                    hoverinfo='text',
                    text=disposal_data['Disposal Facility'],
                    lat=disposal_data['DF Latitude'],
                    lon=disposal_data['DF Longitude'],
                    marker=dict(size=9)
                )
            ] +
            # Plotting transactions lines
            [
                go.Scattermapbox(
                    mode='lines',
                    lat=[
                        get_location(row['Facility NAME'], 'transfer')[0],
                        get_location(row['Disposal Facility'], 'disposal')[0]
                    ],
                    lon=[
                        get_location(row['Facility NAME'], 'transfer')[1],
                        get_location(row['Disposal Facility'], 'disposal')[1]
                    ],
                    line=dict(color='red', width=1),
                    opacity=0.5,
                    hoverinfo='text',
                    text='' + row['Facility NAME'] + ' to ' + row['Disposal Facility']
                ) for _, row in transaction_out_data.iterrows()
            ],
            layout=go.Layout(
                autosize=True,
                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                showlegend=False,
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    center=dict(
                        lat=latInitial,
                        lon=lonInitial
                    ),
                    bearing=0,
                    zoom=8.0
                )
            )
        ),
        style={
            'height': 690
        }
    )
])


@app.callback(
    dash.dependencies.Output('map-graph', 'figure')
)
def update_map():
    return go.Figure(
        data=go.Data([
            go.Scattermapbox(
                lat=str(latInitial),
                lon=str(lonInitial),
                mode='markers',
                hoverinfo='lat+lon'
            )
        ]),
        layout=go.Layout(
            autosize=True,
            height=750,
            margin=go.Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accessoken=mapbox_access_token,
                centre=dict(
                    lat=latInitial,
                    lon=lonInitial
                ),
                bearing=0,
                zoom=7.0
            )
        )
    )


if __name__ == '__main__':
    app.run_server(debug=True)
