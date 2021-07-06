import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

df = pd.read_csv('./airbnb-dataset.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets, title='AirBnb Analysis')

df['Features Count'] = df['Features'].apply(lambda x: len(str(x).split(',')))
df['Amenities Count'] = df['Amenities'].apply(lambda x: len(str(x).split(',')))

df = df.drop(columns=['Unnamed: 0'], axis=1)
df['Review Scores Value'] = df['Review Scores Value'].astype(int)

continuous_cols = df.select_dtypes(include='number').columns
categorical_cols = df.select_dtypes(include='object').columns

# Select only the required columns to visualize
continuous_cols = continuous_cols.drop(['Latitude', 'Longitude'])

# Select only the required columns to visualize
categorical_cols = categorical_cols.drop(
    ['Name', 'City', 'Zipcode', 'Market', 'Country Code', 'Features', 'Amenities', 'Country'])

app.layout = html.Div([

    # Map plot
    dcc.Graph(id='map-id'),
    dcc.Markdown("Select Smart Location to view on the map"),
    dcc.Dropdown(
        id='drop-id',
        options=[{'label': i, 'value': i} for i in df['Smart Location'].unique()],
        value='London, United Kingdom'
    ),

    dcc.Markdown("""
        Map Plot Observations :
            Paris, France :
                Most of the properties that are available are apartments that we can select on the map that is all around Paris.
                As for houses available there are various houses available throughout Paris, Lofts and condomonium are available and mostly located in the north of Paris.
            London, United Kingdom :
                In London the aparements and houses are the type of properties that have the highest availability and it is all around the city.
                Loft are more available within the north-east of London and as for townhouse, condominium, guest house there are only few available which are available around London.
                From the 2 locations, London have more available houses and apartments that are within the city compared to Paris because London is among the largest metropolitan city.
                For lofts, condominium there are more available Airbnbs in PAris than in London.
    """),

    # Pie Chart Plots
    dcc.Graph(id='pie-chart-id'),
    dcc.Markdown("Select Column to display as Pie Chart"),
    dcc.Dropdown(
        id='pie-dropdown-id',
        options=[{'label': i, 'value': i} for i in categorical_cols],
        value='Property Type'
    ),

    dcc.Markdown("""
    Pie Chart Observations :
        Among Paris and London, most Airbnb are available in Lambeth (by 7.21%) and the lowest percentage of available Airbnb is in Bourse (by 0.847%).
        By location wise, London has more available places to rent by 59.6% and Paris has 40.4%.
        Comparing the property types, most available places are apartments which is 89.2% and the least available to rent is the condominium which is only 0.12% in both cities.
        73.8% are the entire home or an apartment and there are only 0.984% shared room.
        Most beds are real beds (92.9%) and there are other types available such as couch , pull-out, sofa, futton and airbed.
        For all Airbnb's cancellation policy most are moderate (39.7%) and 32.2% are flexible while 28% are strict and 0.008% are super strict.
    """),

    # Scatter Plot with Price
    html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Markdown("Select x axis column to compare with Price"),
        dcc.Dropdown(
            id='x-axis-col',
            options=[{'label': i, 'value': i} for i in continuous_cols],
            value='Accommodates'
        ),

        dcc.Markdown("Slider to filter by ratings"),
        dcc.Slider(
            id='Review-slider',
            min=df['Review Scores Value'].min(),
            max=df['Review Scores Value'].max(),
            value=df['Review Scores Value'].max(),
            marks={str(scr): str(scr) for scr in df['Review Scores Value'].unique()},
        ),
    ], style={'width': '100%', 'display': 'inline-block'}),

    dcc.Markdown("""
    Scatter Plot Observations :
    When choosing the rate 10 for the Airbnb, it shows that there is one apartment that accomodates 2 people that has the highest price among all.
    Most apartments accommodates from 1-6 people with an average to lower price.
    
    For the availability of bathrooms, it shows that apartments mostly have 1-2.5 bathrooms where mostly the prices are below 400.
    There are a house in London which has no bedroom but has a price of 700 while there is an apartment in Paris with 1 bedroom with the price of 1000.
    Beds are available ranging from 1-10 and it can be seen that even the house with 10 beds have are within the average range at the price of 200.
    With 1 bed available the price can also be pretty high which is in 1000 located in Paris.
    
    Most apartments and houses have the average prices are 11-400 and there are several apartments and houses that are above 400 and the highest price is the apartment in PAris with the price of 1000.
    Most houses are at the same price as the apartments and the type of the property does not determine the price of the rent.
    Mostly the prices of extra people are under 100.
    
    There are a lot of houses and apartments that are available for 365 that is under 400 in both PAris and London.
    Most properties rented have review less than 50 review and the most review earned is by the appartment in Paris with 330 and the price is 70 which is cheaper than most apartments.
    Most owners have only 1 listing and the most listing is 123 in Paris."""),

    # Histogram Plot with Price
    html.Div([
        dcc.Graph(id='histogram-id'),
        dcc.Markdown("Select x axis column to compare with Price"),
        dcc.Dropdown(
            id='histogram-x-axis-col',
            options=[{'label': i, 'value': i} for i in categorical_cols],
            value='Neighbourhood Cleansed'
        ),

        dcc.Markdown("Select Country to Visualize"),
        dcc.Dropdown(
            id='histogram-drop-id',
            options=[{'label': i, 'value': i} for i in df['Smart Location'].unique()],
            value='London, United Kingdom'
        ),
    ], style={'width': '100%', 'display': 'inline-block'}),

    dcc.Markdown("""
        Map Plot Observations :
        Most rented in Paris are apartments and the gap between apartments and other property type are pretty big as well as the gap for the price.
        In London sum of price and the property type have a big gap where apartments have the highest sum of price as high as 270.2k (entire house/room) and for the private room
        is only 69.3k. For the gap to all other property types are below 50k for all categories (entire home, private room, shared room) however, for the house in the category of
        entire home is still above 52k. As for Paris, except apartments who have the highest sul of price for apartments in the category of private room above 500k
        the rest of the property type is below 10k for all categories as well.
    """)
])


# Map plot
@app.callback(
    Output('map-id', 'figure'),
    Input('drop-id', 'value'))
def update_figure(selected_location):
    filtered_df = df[df['Smart Location'] == selected_location]

    fig = px.scatter_mapbox(filtered_df, lat="Latitude", lon="Longitude", hover_name="Smart Location",
                            hover_data=["Neighbourhood Cleansed", "Price"],
                            color='Property Type', size='Price',
                            title='Map: ' + str(selected_location),
                            height=800)
    fig.update_layout(mapbox_style="open-street-map")

    return fig


@app.callback(
    Output('pie-chart-id', 'figure'),
    Input('pie-dropdown-id', 'value')
)
def update_figure(selected_category):
    filtered_df = df[selected_category]

    fig = px.pie(filtered_df, values=filtered_df.value_counts(), names=filtered_df.unique(),
                 title='Pie Chart: ' + str(selected_category))

    fig.update_layout(transition_duration=1)

    return fig


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('x-axis-col', 'value'),
    Input('Review-slider', 'value')
)
def update_figure(x_axis_name, selected_review):
    filtered_df = df[df['Review Scores Value'] == selected_review]

    fig = px.scatter(filtered_df, x=x_axis_name, y='Price',
                     color="City", hover_name="Property Type",
                     title="Scatter plot -  Rating: " + str(selected_review),
                     height=800)

    fig.update_layout(transition_duration=1)

    return fig


# Histogram Callback
@app.callback(
    Output('histogram-id', 'figure'),
    Input('histogram-x-axis-col', 'value'),
    Input('histogram-drop-id', 'value')
)
def update_figure(x_axis_name, location):
    filtered_df = df[df['Smart Location'] == location]

    fig = px.histogram(filtered_df, x=x_axis_name, y='Price', color='Room Type', barmode='group',
                       title='Histogram: ' + str(location), height=800)
    fig.update_layout(transition_duration=1)

    return fig


app.run_server()
