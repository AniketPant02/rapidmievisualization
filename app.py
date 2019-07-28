# CUSTOM DASH SERVER FOR PLOTTING MIE SPECTRA
# Visualization of Mie Scattering from all Tested Configs
# A generalized scripting tool for rapid plotting of generated Mie spectra.
# Aniket Pant, UAB Plasmonics, 07/23/2019
# DATA PROCESSING
import pandas as pd
import numpy as np
import urllib.parse
import datetime

# WEBSITE CREATION
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# PLOTTING
from plotly.graph_objs import *
import plotly.graph_objs as go
from plotly import tools

# IMPORT DATA
df = pd.read_csv('fullconcat.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# PLOTTING CONSTANTS
materials = ["Au", "Ag", "Al", "Cu", "GaAs", "GaN", "GaP", "Si", "Ge"]
diameters = np.array([90, 110, 140, 170, 200], dtype = 'int')
n_envs = np.array([1.0, 1.4, 2.0, 2.4, 3.0], dtype = 'float64')

# PLOTTING COLORS FOR LINEPLOTS
diameter_rgbs = [
    "rgb(255, 153, 154)",
    "rgb(255, 102, 102)",
    "rgb(255, 51, 51)",
    "rgb(255, 0, 0)",
    "rgb(204, 0, 0)",
    "rgb(153, 0, 0)"
]
n_envs_rgbs = [
    "rgb(102, 178, 255)",
    "rgb(51, 153, 255)",
    "rgb(0, 128, 255)",
    "rgb(0, 102, 244)",
    "rgb(0, 76, 153)",
    "rgb(0, 51, 102)"
]

app.title = 'Mie Extinction Spectra'


app.layout = html.Div(
    html.Div([
        html.Div( # ROW ONE
            [
                html.H3(children="Au: Mie Extinction Spectra",
                        className='nine columns', id = 'page-title', style = {
                            "margin-top": 40,
                            "margin-left": 10
                        }), # WEBSITE TITLE
                html.Div(children = [
                    dcc.Dropdown(
                        id='material-dropdown',
                        options=[
                            {'label': "Au", 'value': "Au"},
                            {'label': "Ag", 'value': "Ag"},
                            {'label': "Al", 'value': "Al"},
                            {'label': "Cu", 'value': "Cu"},
                            {'label': "GaAs", 'value': "GaAs"},
                            {'label': "GaN", 'value': "GaN"},
                            {'label': "GaP", 'value': "GaP"},
                            {'label': "Si", 'value': "Si"},
                            {'label': "Ge", 'value': "Ge"}
                        ],
                        value='Au'
                    )
                ], className = 'three columns',
                style = {
                    "marginRight": 10,
                    'float': "right"
                })
            ], className="row"
        ), # ROW ONE END

        html.Div( # START ROW TWO LINE PLOTS
            [
            html.Div([
                dcc.Graph(
                    id='diameter-lineplot'
                )
                ], className= 'six columns'
                ),

                html.Div([
                dcc.Graph(
                    id='dielectric-lineplot'
                )
                ], className= 'six columns'
                )
            ], className="row"
        ), # END ROW 2 LINE PLOTS

        html.Div( # START ROW 3 SLIDERS FOR SURF PLOTS
            [
            html.Div([
                dcc.Slider(
                    min=1.0,
                    max=3.0,
                    step=0.2,
                    value=1,
                    id='diameter-slider',
                    marks={
                        1: "1",
                        1.2: "1.2",
                        1.4: "1.4",
                        1.6: "1.6",
                        1.8: "1.8",
                        2: "2",
                        2.2: "2.2",
                        2.4: "2.4",
                        2.6: "2.6",
                        2.8: "2.8",
                        3: "3"
                    },
                ),
                ],
                style = {
                        'marginBottom': 10
                    },
                className= 'six columns'
                ),

                html.Div([
                dcc.Slider(
                    min=10,
                    max=200,
                    step=10,
                    value=150,
                    id='dielectric-slider',
                    marks = {
                            10: "10",
                            20: "20",
                            30: "30",
                            40: "40",
                            50: "50",
                            60: "60",
                            70: "70",
                            80: "80",
                            90: "90",
                            100: "100",
                            110: "110",
                            120: "120",
                            130: "130",
                            140: "140",
                            150: "150",
                            160: "160",
                            170: "170",
                            180: "180",
                            190: "190",
                            200: "200"
                    }
                )
                ], className= 'six columns'
                )
            ],
            style = {
                        'marginBottom': 10
                    }, 
            className="row"
        ), # END ROW 3 SURF PLOTS,

        html.Div( # START ROW 4 SURF PLOTS
            [
            html.Div([
                dcc.Graph(
                    id='diameter-surfplot'
                )
                ], className= 'six columns'
                ),

                html.Div([
                dcc.Graph(
                    id='dielectric-surfplot'
                )
                ], className= 'six columns'
                )
            ], className="row"
        ), # END ROW 3 SURF PLOTS,

        html.Div( # START ROW 4 DOWNLOAD LINKS
            [
            html.Div([
                html.A(
                    "Download Diameter-index Data",
                    id='diameter-download',
                    download = 'diameter_data.csv',
                    href = '',
                    target = "_blank"

                )
                ], className= 'six columns',
                style = {
                    'marginTop': 20
                }
                ),

                html.Div([
                html.A(
                    "Download Dielectric-index Data",
                    id='dielectric-download',
                    download = 'dielectric_data.csv',
                    href = '',
                    target = "_blank"

                )
                ], className= 'six columns',
                style = {
                    'marginTop': 20
                }
                )
            ], className="row"
        ) # END ROW 3 SURF PLOTS
    ], className='ten columns offset-by-one')
)

# MATERIAL CALLBACK DEFINED HERE
@app.callback(
    [Output('diameter-lineplot', 'figure'),
     Output('dielectric-lineplot', 'figure'),
     Output('diameter-surfplot', 'figure'),
     Output('dielectric-surfplot', 'figure'),
     Output('page-title', 'children'),
     Output('diameter-download', 'href'),
     Output('dielectric-download', 'href'),
    Output('diameter-download', 'download'),
     Output('dielectric-download', 'download')],
    [Input('material-dropdown', 'value'),
     Input('diameter-slider', 'value'),
     Input('dielectric-slider', 'value')])
def update_site_with_material_choice(material, dielectric, diameter):

    # DATA PROCESSING FOR PLOTTING
    df_mat = df[df['Material'] == material]

    # GETTING DATA IN PLOTTING FORMAT
    # DIAMETER DATA
    df_diameter = df_mat[df_mat['Medium Refractive Index'] == dielectric]
    df_diameter = df_diameter.set_index(df_diameter['Diameter (nm)'])
    df_diameter = df_diameter.drop(['Medium Refractive Index', 'Material', 'Diameter (nm)'], axis = 1)

    # DIELECTRIC DATA
    df_dielectric = df_mat[df_mat['Diameter (nm)'] == diameter]
    df_dielectric = df_dielectric.set_index(df_dielectric['Medium Refractive Index'])
    df_dielectric = df_dielectric.drop(['Diameter (nm)', 'Material', 'Medium Refractive Index'], axis = 1)

    # MAKE CSV STRINGS FOR DF DOWNLOADS
    # DIAMETER DOWNLOAD
    d = datetime.datetime.today()
    diameter_csv_string = df_diameter.to_csv(index=True, encoding='utf-8')
    diameter_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(diameter_csv_string)
    diameter_csv_filename = "{}_{}_{}_Material_{}_Env_Dielectric_{}.csv".format(d.year, d.month, d.day, material, dielectric)
    # DIELECTRIC DOWNLOAD
    dielectric_csv_string = df_dielectric.to_csv(index=True, encoding='utf-8')
    dielectric_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(dielectric_csv_string)
    dielectric_csv_filename = "{}_{}_{}_Material_{}_Diameter_{}.csv".format(d.year, d.month, d.day, material, diameter)

    # DIAMETER LINE PLOT
    return [{
        'data': [
            go.Scatter(
                x=df_diameter.columns,
                y=df_diameter.loc[diameters[i]],
                mode='lines',
                name="{}nm".format(diameters[i]),
                line=dict(color=diameter_rgbs[i], width=4),
            )
        for i in range(len(diameters))],
        'layout': {
            'title': '{}: Vary Diameter. n<sub>env</sub> = {}'.format(material, dielectric),
            'xaxis' : dict(
                title='Wavelength (nm)',
                showline=True, linewidth=1, linecolor='black', mirror=True
            ),
            'yaxis' : dict(
                title='Extinction (a.u.)',
                showline=True, linewidth=1, linecolor='black', mirror=True
            ),
        }
    },
    # DIELECTRIC LINE PLOT
    {
        'data': [
            go.Scatter(
                x=df_dielectric.columns,
                y=df_dielectric.loc[n_envs[i]],
                mode='lines',
                name="n<sub>env</sub> = {}".format(n_envs[i]),
                line=dict(color=n_envs_rgbs[i], width=4)
            )
        for i in range(len(n_envs))],
        'layout': {
            'title': '{}: Vary Dielectric. Diameter = {}nm'.format(material, diameter),
            'xaxis' : dict(
                title='Wavelength (nm)',
                showline=True, linewidth=1, linecolor='black', mirror=True
                ),
            'yaxis' : dict(
                title='Extinction (a.u.)',
                showline=True, linewidth=1, linecolor='black', mirror=True
                )
        }
    },
    # DIAMETER SURF PLOT
    {
        'data': [
                go.Heatmap(
                    z=df_diameter.values,
                    x = df_diameter.columns,
                    y = df_diameter.index,
                    colorscale = "RdBu",
                    reversescale = True,
                    showscale = True,
                    zsmooth = "best"
                    )
                ],
        'layout': {
            'title': '{}: Vary Diameter. n<sub>env</sub> = {}'.format(material, dielectric),
            'xaxis' : dict(
                title='Wavelength (nm)'
                ),
            'yaxis' : dict(
                title='Diameter (nm)'
            )
        }
    },
    # DIELECTRIC SURF PLOT
    {
        'data': [
                go.Heatmap(
                    z=df_dielectric.values,
                    x = df_dielectric.columns,
                    y = df_dielectric.index,
                    colorscale = "RdBu",
                    reversescale = True,
                    showscale = True,
                    zsmooth = "best"
                    )
        ],
        'layout': {
            'title': '{}: Vary Dielectric. Diameter = {}nm'.format(material, diameter),
            'xaxis': dict(
                title = "Wavelength (nm)"
            ),
            'yaxis': dict(
                title = "Environment Dielectric (n)"
            )
        }
    },
                    
    # TITLE FOR WEBSITE WITH MATERIAL TAG
    "{}: Extinction Mie Spectra".format(material),

    # CSV for diameter-download
    diameter_csv_string,

    # CSV for dielectric-download
    dielectric_csv_string,

    # Diameter filename
    diameter_csv_filename,

    # Dielectric filename
    dielectric_csv_filename

    ]

if __name__ == '__main__':
    app.run_server()