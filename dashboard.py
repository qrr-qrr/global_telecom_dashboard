import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import duckdb

# Функция для получения данных из базы данных
def get_data_from_db():
    conn = duckdb.connect('my.db')
    query = "SELECT * FROM Final_cleaned"
    df = conn.execute(query).fetchdf()
    conn.close()
    return df

# Создание экземпляра Dash
app = dash.Dash(__name__)

# Загрузка данных
df = get_data_from_db()

# Преобразование типов данных для удобства работы с дашбордом
df['Year'] = df['Year'].astype(int)

app.layout = html.Div([
    html.H1("Дашборд глобальных телекоммуникационных трендов"),
    
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['Entity'].unique()],
        value=['Afghanistan'],  # Значения по умолчанию
        multi=True
    ),
    
    dcc.RangeSlider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=[2000, df['Year'].max()],
        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max()+1, 5)},
        step=None
    ),
    
    dcc.Graph(id='digital-divide-graph'),
    dcc.Graph(id='internet-growth-graph'),
    dcc.Graph(id='mobile-vs-broadband-graph'),
    dcc.Graph(id='telecom-trends-graph')
])

@app.callback(
    [Output('digital-divide-graph', 'figure'),
     Output('internet-growth-graph', 'figure'),
     Output('mobile-vs-broadband-graph', 'figure'),
     Output('telecom-trends-graph', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graphs(selected_countries, year_range):
    # Фильтрация данных
    filtered_df = df[(df['Entity'].isin(selected_countries)) & 
                     (df['Year'].between(year_range[0], year_range[1]))]

    # Создание графиков
    digital_divide_fig = px.line(filtered_df, x='Year', y='Internet_Users_Percent', color='Entity', 
                                 title='Цифровой разрыв')
    internet_growth_fig = px.line(filtered_df, x='Year', y='Internet_Users_Percent', color='Entity', 
                                  title='Темпы роста интернет-проникновения')
    mobile_vs_broadband_fig = px.line(filtered_df, x='Year', y='Cellular_Subscription', color='Entity', 
                                      title='Сравнение мобильной связи и широкополосного интернета')
    telecom_trends_fig = px.line(filtered_df, x='Year', y='Broadband_Subscription', color='Entity', 
                                 title='Телекоммуникационные тренды')

    return digital_divide_fig, internet_growth_fig, mobile_vs_broadband_fig, telecom_trends_fig

if __name__ == '__main__':
    app.run_server(debug=True)
