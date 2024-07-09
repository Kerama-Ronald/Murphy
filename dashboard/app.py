import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash_iconify import DashIconify

#create the dataframes
df = pd.read_csv('data/auction_items.csv')
df_sold = pd.read_csv('data/auction_sold_items.csv')
# Initialize the Dash app
app = dash.Dash(__name__)

#sidebar layout
sidebar = html.Div(
    [
        html.Img(src='assets/logo.png', className='logo-img'),
        html.Nav([
            html.Ul([
                html.Li(html.A(children=[DashIconify(icon="mdi:home", className='icon'),'Home'], href='', style={'display':'block'})),
                html.Li(html.A(children=[DashIconify(icon="mdi:tag-plus", className='icon'),'New Item'], href='')),
                html.Li(html.A(children=[DashIconify(icon="mdi:account", className='icon'),'Account'], href='')),
                html.Li(html.A(children=[DashIconify(icon="mdi:cog", className='icon'),'Settings'], href='')),
            ], className='nav'),
        ])
    ],className='navbar'
)
#GRAPHS
#bar chart
# Calculate the count of items per type
df_count = df['Type'].value_counts().reset_index()
df_count.columns = ['Type', 'Count']
figure_bar = px.bar(df_count, x='Type', y='Count')
figure_bar.update_layout(
        plot_bgcolor='rgb(250, 249, 250)',
        paper_bgcolor='rgb(249, 250, 252)',
        font_color='black',
        width=349,
        height=300,
        margin=dict(l=5, r=5, t=80, b=5),
        title=dict(text='Number of Items per Type', font=dict(family='Arial', color='black')),
        title_x = 0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left",  x=0)
)
figure_bar.update_xaxes(showgrid=True, gridcolor='rgb(240, 239, 236)')
figure_bar.update_yaxes(showgrid=True, gridcolor='rgb(245, 249, 246)')

#pie chart
# Convert Starting Bid to numerical values
df['Starting Bid'] = df['Starting Bid'].replace('[\$,]', '', regex=True).astype(float)
# Aggregate the sum of starting bids by type
df_agg = df.groupby('Type', as_index=False)['Starting Bid'].sum()
figure_pie = px.pie(df_agg, values='Starting Bid', names='Type')
figure_pie.update_layout(margin=dict(l=40, r=0, t=70, b=0), 
                      paper_bgcolor='rgb(250, 249, 250)', width=330, height=300, 
                      title=dict(text='Distribution of Starting Bids by Type', font=dict(family='Arial', color='black')),
                      legend=dict(
                        font=dict(
                            color="black"  
                        )))

#histogram
figure_hist = px.histogram(df, x="Starting Bid", title="Distribution of Starting Bids")
figure_hist.update_layout(
        plot_bgcolor='rgb(250, 249, 250)',
        paper_bgcolor='rgb(249, 250, 252)',
        font_color='black',
        width=349,
        height=300,
        margin=dict(l=5, r=5, t=80, b=5),
        title=dict(text='Distribution of Starting Bids', font=dict(family='Arial', color='black')),
        title_x = 0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left",  x=0)
)
figure_hist.update_xaxes(showgrid=True, gridcolor='rgb(240, 239, 236)')
figure_hist.update_yaxes(showgrid=True, gridcolor='rgb(245, 249, 246)')

#scatter chart
figure_scatter = px.scatter(df, x="Model/Size", y="Starting Bid", color="Type", title="Starting Bids for Different Models/Sizes")
figure_scatter.update_layout(
        plot_bgcolor='rgb(250, 249, 250)',
        paper_bgcolor='rgb(250, 249, 250)',
        font_color='black',
        width=500,
        height=300,
        margin=dict(l=5, r=5, t=90, b=3),
        title=dict(text='Starting Bids for Different Models/Sizes', font=dict(family='Arial', color='black')),
        title_x = 0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left",  x=0)
)
figure_scatter.update_xaxes(showgrid=True, gridcolor='white')

figure_box=px.box(df, x="Type", y="Starting Bid", title="Starting Bids by Type")
#grouped bar chart
# Calculate mean starting bid and final bid for each item type
mean_values = df_sold.groupby('Item Type')[['Starting Bid', 'Final Bid']].mean().reset_index()
# Melt the dataframe for easier plotting
mean_values_melted = mean_values.melt(id_vars='Item Type', value_vars=['Starting Bid', 'Final Bid'],
                                      var_name='Bid Type', value_name='Bid Amount')
# Create the bar chart
figure_grouped = px.bar(mean_values_melted, x='Item Type', y='Bid Amount', color='Bid Type',
             barmode='group', title='Mean Starting Bid and Mean Final Bid by Item Type')
figure_grouped.update_layout(
        plot_bgcolor='rgb(250, 249, 250)',
        paper_bgcolor='rgb(249, 250, 252)',
        font_color='black',
        width=550,
        height=300,
        margin=dict(l=5, r=5, t=80, b=5),
        title=dict(text='Mean Starting and Final Bid by Item Type', font=dict(family='Arial', color='black')),
        title_x = 0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left",  x=0)
)
figure_grouped.update_xaxes(showgrid=True, gridcolor='rgb(240, 239, 236)')
figure_grouped.update_yaxes(showgrid=True, gridcolor='rgb(245, 249, 246)')

app.layout = html.Div([
    html.Div(
        sidebar
    ),
    html.H1(className='header', children=['MURPHY MERCHANTS AUCTIONEERS']),
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Div(
                        id='bar-chart', className='chart', children=[dcc.Graph(figure=figure_bar, config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)]
                    )
                ]
            ),
            dbc.Col(
                [
                    html.Div(
                        id='pie-chart', className='chart', children=[dcc.Graph(figure=figure_pie, config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)]
                    )
                ]
            ),
            dbc.Col(
                [
                    html.Div(
                        id='histogram', className='chart', children=[dcc.Graph(figure=figure_hist, config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)]
                    )
                ]
            )
        ], className='row row-first'
    ),
    html.Hr(className='row'),
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Div(
                        id='scatter-chart', className='chart', children=[dcc.Graph(figure=figure_scatter, config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)]
                    )
                ]
            ),
            dbc.Col(
                [
                    html.Div(
                        id='grouped-chart', className='chart', children=[dcc.Graph(figure=figure_grouped, config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)]
                    )
                ]
            )
        ], className='row'
    )
], className='content')

if __name__ == '__main__':
    app.run_server(debug=True)
