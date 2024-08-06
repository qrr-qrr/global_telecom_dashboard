import os
import duckdb
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
from dash_iconify import DashIconify

# Путь к базе данных
DB_PATH = 'Final_cleaned.db'

def initialize_db():
    if not os.path.exists(DB_PATH):
        print("Creating new database")
    else:
        print("Database file exists, checking for table")
    
    conn = duckdb.connect(DB_PATH)
    
    try:
        # Проверяем существование таблицы
        result = conn.execute("SELECT COUNT(*) FROM Final_cleaned").fetchone()
        print(f"Table 'Final_cleaned' exists and contains {result[0]} rows")
    except duckdb.CatalogException:
        print("Table 'Final_cleaned' does not exist. Creating it.")
        df = pd.read_csv('source/Final_cleaned.csv')
        conn.execute('CREATE TABLE Final_cleaned AS SELECT * FROM df')
        print("Table 'Final_cleaned' created and populated")
    
    conn.close()

def get_data_from_db():
    conn = duckdb.connect(DB_PATH)
    df = conn.execute("SELECT * FROM Final_cleaned").fetchdf()
    conn.close()
    return df

# Инициализируем базу данных
initialize_db()

# Получаем данные
df = get_data_from_db()

# Преобразование типов данных для удобства работы с дашбордом
df['Year'] = df['Year'].astype(int)

# Создание экземпляра Dash
app = dash.Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600&display=swap'
])

server = app.server  # Для Gunicorn

# Обновленная цветовая схема
colors = {
    'background': '#E8F1F5',
    'card_background': '#FFFFFF',
    'text': '#1D1D1F',
    'primary': '#005BBF',
    'secondary': '#86868B',
    'tertiary': '#B3D4E5',
    'accent': '#FF9500'
}
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: ''' + colors['background'] + ''';
                color: ''' + colors['text'] + ''';
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .card {
                background-color: ''' + colors['card_background'] + ''';
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
            }
            .card:hover {
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
                transform: translateY(-5px);
            }
            .menu-item {
                background-color: ''' + colors['tertiary'] + ''';
                color: ''' + colors['text'] + ''';
                padding: 12px 16px;
                border-radius: 8px;
                margin-right: 10px;
                cursor: pointer;
                transition: background-color 0.3s, color 0.3s, transform 0.3s;
            }
            .menu-item:hover, .menu-item.active {
                background-color: ''' + colors['primary'] + ''';
                color: white;
                transform: translateY(-2px);
            }
            .button {
                background-color: ''' + colors['primary'] + ''';
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: 500;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s;
            }
            .button:hover {
                background-color: #004999;
                transform: translateY(-2px);
            }
            .dropdown .Select-control {
                border: 1px solid ''' + colors['tertiary'] + ''';
                border-radius: 8px;
                transition: box-shadow 0.3s;
            }
            .dropdown .Select-control:hover {
                box-shadow: 0 0 0 2px ''' + colors['primary'] + ''';
            }
            .range-slider .rc-slider-track {
                background-color: ''' + colors['primary'] + ''';
            }
            .range-slider .rc-slider-handle {
                border-color: ''' + colors['primary'] + ''';
            }
            .tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 200px;
                background-color: ''' + colors['text'] + ''';
                color: ''' + colors['card_background'] + ''';
                text-align: center;
                border-radius: 6px;
                padding: 5px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -100px;
                opacity: 0;
                transition: opacity 0.3s;
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
            .summary-card {
                background-color: ''' + colors['accent'] + ''';
                color: white;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .authors {
                text-align: center;
                font-style: italic;
                margin-top: 20px;
                color: ''' + colors['secondary'] + ''';
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Обновленный макет приложения
app.layout = html.Div([
    html.Div([
        html.H1("Глобальные телекоммуникационные тренды", 
                style={'textAlign': 'center', 'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '30px'}),
        
        html.Div([
            html.Div([
                html.Label("Выберите страны:", style={'marginBottom': '10px', 'fontWeight': '500'}),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': country, 'value': country} for country in df['Entity'].unique()],
                    value=['Afghanistan'],
                    multi=True,
                    className='dropdown'
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("Выберите диапазон лет:", style={'marginBottom': '10px', 'fontWeight': '500'}),
                dcc.RangeSlider(
                    id='year-slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=[2000, df['Year'].max()],
                    marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max()+1, 5)},
                    step=None,
                    className='range-slider'
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'marginBottom': '30px'}),
        
        html.Div(id='summary-stats', className='summary-card'),
        
        html.Div([
            html.Div("Цифровой разрыв", id='tab-1', className='menu-item', n_clicks=0),
            html.Div("Рост интернета", id='tab-2', className='menu-item', n_clicks=0),
            html.Div("Мобильная связь vs ШПД", id='tab-3', className='menu-item', n_clicks=0),
            html.Div("Телеком тренды", id='tab-4', className='menu-item', n_clicks=0),
            html.Div("Карта пользователей", id='tab-5', className='menu-item', n_clicks=0),
            html.Div("Сравнение связи", id='tab-6', className='menu-item', n_clicks=0),
            html.Div("Рост пользователей", id='tab-7', className='menu-item', n_clicks=0),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),
        
        html.Div(id='tab-content', className='card'),
        
        html.Div([
            html.Button("Обновить данные", id='refresh-button', className='button'),
            html.Div([
                DashIconify(icon="mdi:information", width=20, height=20, style={'marginLeft': '10px', 'verticalAlign': 'middle'}),
                html.Span("Инфо", className="tooltiptext")
            ], className="tooltip")
        ], style={'textAlign': 'center', 'marginTop': '30px'}),

        html.Div("Авторы: Ниёзов Анушервон и Давронов Мустафо", className='authors')
    ], className='container')
])

@app.callback(
    Output('summary-stats', 'children'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_summary_stats(selected_countries, year_range):
    filtered_df = df[(df['Entity'].isin(selected_countries)) & 
                     (df['Year'].between(year_range[0], year_range[1]))]
    
    avg_internet_users = filtered_df['Internet_Users_Percent'].mean()
    avg_mobile_subs = filtered_df['Cellular_Subscription'].mean()
    avg_broadband_subs = filtered_df['Broadband_Subscription'].mean()
    
    return html.Div([
        html.H4("Сводная статистика"),
        html.P(f"Средний процент интернет-пользователей: {avg_internet_users:.2f}%"),
        html.P(f"Среднее количество мобильных подписок: {avg_mobile_subs:.2f}"),
        html.P(f"Среднее количество широкополосных подписок: {avg_broadband_subs:.2f}")
    ])

@app.callback(
    Output('tab-content', 'children'),
    [Input(f'tab-{i}', 'n_clicks') for i in range(1, 8)],
    [State('country-dropdown', 'value'),
     State('year-slider', 'value')]
)
def update_content(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'tab-1'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    selected_countries = args[-2]
    year_range = args[-1]
    
    filtered_df = df[(df['Entity'].isin(selected_countries)) & 
                     (df['Year'].between(year_range[0], year_range[1]))]

    # Создаем стильный фон для графиков
    layout = go.Layout(
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='"SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif', color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode='closest',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.4)', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.4)', zeroline=False),
    )

    if button_id == 'tab-1':
        fig = px.line(filtered_df, x='Year', y='Internet_Users_Percent', color='Entity', 
                      title='Цифровой разрыв')
        description = "Этот график показывает разницу в доступе к интернету между разными странами с течением времени."
    elif button_id == 'tab-2':
        fig = px.line(filtered_df, x='Year', y='Internet_Users_Percent', color='Entity', 
                      title='Темпы роста интернет-проникновения')
        description = "Здесь отображены темпы роста интернет-проникновения в выбранных странах."
    elif button_id == 'tab-3':
        fig = px.line(filtered_df, x='Year', y=['Cellular_Subscription', 'Broadband_Subscription'], color='Entity', 
                      title='Сравнение мобильной связи и широкополосного интернета')
        description = "Сравнение распространения мобильной связи и широкополосного интернета в выбранных странах."
    elif button_id == 'tab-4':
        fig = px.line(filtered_df, x='Year', y='Broadband_Subscription', color='Entity', 
                      title='Телекоммуникационные тренды')
        description = "Общие тенденции в телекоммуникационном секторе для выбранных стран."
    elif button_id == 'tab-5':
        fig = px.choropleth(filtered_df, locations="Entity", locationmode="country names",
                            color="Internet_Users_Percent", hover_name="Entity", 
                            animation_frame="Year", title="Процент пользователей интернета по странам",
                            color_continuous_scale=px.colors.sequential.Viridis)
        description = "Визуализация процента пользователей интернета по странам на карте мира."
    elif button_id == 'tab-6':
        fig = px.pie(filtered_df, values='Cellular_Subscription', names='Entity', 
                     title='Сравнение мобильной связи и широкополосного интернета')
        description = "Круговая диаграмма, показывающая соотношение мобильной связи и широкополосного доступа."
    elif button_id == 'tab-7':
        fig = px.histogram(filtered_df, x='Year', y='Internet_Users_Percent', color='Entity', 
                           title='Рост интернет-пользователей по годам', barmode='group')
        description = "Гистограмма, отображающая рост числа интернет-пользователей по годам."
    
    fig.update_layout(layout)
    
    # Убираем среднюю линию
    fig.update_yaxes(zeroline=False)
    fig.update_xaxes(zeroline=False)
    
    # Добавляем градиентный фон
    fig.add_layout_image(
        dict(
            source="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==",
            xref="paper",
            yref="paper",
            x=0,
            y=1,
            sizex=1,
            sizey=1,
            sizing="stretch",
            opacity=0.1,
            layer="below")
    )
    
    return [
        dcc.Graph(figure=fig),
        html.P(description, style={'marginTop': '10px', 'fontSize': '14px', 'color': colors['secondary']})
    ]

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run_server(debug=False, host='0.0.0.0', port=port)