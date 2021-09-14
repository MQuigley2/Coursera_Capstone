# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()




# Create a dash application
app = dash.Dash(__name__)
launch_sites_list=['All']+list(spacex_df['Launch Site'].unique())
launch_sites_options=[{'label':site,'value':site} for site in launch_sites_list]

def map_class_to_success(class_):
    if class_==1:
        return 'Success'
    return 'Failure'

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'))
def get_success_pie_chart(site):
    if site=='All':
        site_df=spacex_df[spacex_df['class']==1].groupby('Launch Site').count().reset_index()
        names_column='Launch Site'
    else:
        site_df=spacex_df[spacex_df['Launch Site']==site].groupby('class').count().reset_index()
        site_df['Success']=site_df['class'].map(map_class_to_success)
        names_column='Success'
    pie_fig=px.pie(site_df,names=names_column,values='Payload Mass (kg)')
    pie_fig.update_layout()
    return pie_fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'), 
            Input(component_id="payload-slider", component_property="value"))
def get_payload_success_scatter_plot(site,payload_range):
    payload_success=spacex_df.loc[spacex_df['Payload Mass (kg)'].map(lambda mass: payload_range[0]<=mass<=payload_range[1]),:]
    if site !='All':
        payload_success=payload_success.loc[ payload_success['Launch Site']==site,:]
    
    scatter_fig=px.scatter(payload_success,x='Payload Mass (kg)',y='class',color="Booster Version Category")
    scatter_fig.update_layout()
    return scatter_fig

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=launch_sites_options,value='All',placeholder='Select a Launch Site here',searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
