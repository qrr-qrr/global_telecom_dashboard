import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import duckdb
from dash_iconify import DashIconify
import dash_daq as daq

def get_data_from_db():
    try:
        conn = duckdb.connect('Final_cleaned.db')
        query = "SELECT * FROM Final_cleaned"
        df = conn.execute(query).fetchdf()
        conn.close()
        return df
    except duckdb.CatalogException as e:
        print(f"Ошибка при доступе к базе данных: {e}")
        return pd.DataFrame(columns=['Entity', 'Year', 'Internet_Users_Percent', 'Cellular_Subscription', 'Broadband_Subscription'])

app = dash.Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600&display=swap'
])

df = get_data_from_db()
df['Year'] = df['Year'].astype(int)

colors = {
    'background': '#E6F3FF',
    'card_background': '#FFFFFF',
    'text': '#1D1D1F',
    'primary': '#0071E3',
    'secondary': '#86868B',
    'tertiary': '#E8E8ED',
    'accent': '#FF3B30'
}

dark_colors = {
    'background': '#1C1C1E',
    'card_background': '#2C2C2E',
    'text': '#FFFFFF',
    'primary': '#0A84FF',
    'secondary': '#86868B',
    'tertiary': '#3A3A3C',
    'accent': '#FF453A'
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
                transition: all 0.3s ease;
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
                transition: all 0.3s ease;
            }
            .card:hover {
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
                transform: translateY(-5px);
            }
            .menu-item {
                background-color: ''' + colors['tertiary'] + ''';
                color: ''' + colors['text'] + ''';
                padding: 12px 16px;
                border-radius: 8px;
                margin-right: 10px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .menu-item:hover, .menu-item.active {
                background-color: ''' + colors['primary'] + ''';
                color: ''' + colors['card_background'] + ''';
                transform: translateY(-2px);
            }
            .button {
                background-color: ''' + colors['primary'] + ''';
                color: ''' + colors['card_background'] + ''';
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .button:hover {
                background-color: ''' + colors['accent'] + ''';
                transform: translateY(-2px);
            }
            .dropdown .Select-control {
                border: 1px solid ''' + colors['tertiary'] + ''';
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            .dropdown .Select-control:hover {
                box-shadow: 0 0 0 2px ''' + colors['primary'] + ''';
            }
            .range-slider .rc-slider-track {
                background-color: ''' + colors['primary'] + ''';
            }
            .range-slider .rc-slider-handle {
                border-color: ''' + colors['primary'] + ''';
                background-color: ''' + colors['card_background'] + ''';
            }
            .summary-card {
                background-color: ''' + colors['primary'] + ''';
                color: ''' + colors['card_background'] + ''';
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            .summary-card:hover {
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
                transform: translateY(-5px);
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

app.layout = html.Div([
    html.Div([
        html.H1("Глобальные телекоммуникационные тренды", 
                style={'textAlign': 'center', 'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '30px', 'color': colors['text']}),
        
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
                html.Div([
                    dcc.RangeSlider(
                        id='year-slider',
                        min=df['Year'].min(),
                        max=df['Year'].max(),
                        value=[2000, df['Year'].max()],
                        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max()+1, 5)},
                        step=None,
                        className='range-slider'
                    ),
                ], id='year-slider-container'),
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
                DashIconify(icon="mdi:information", width=20, height=20, style={'marginLeft': '10px', 'verticalAlign': 'middle', 'color': colors['secondary']}),
                html.Span("Информация о данных", className="tooltiptext")
            ], className="tooltip")
        ], style={'textAlign': 'center', 'marginTop': '30px'}),

        html.Div([
            "Разработано: ",
            html.Span("Ниёзов Анушервон", style={'color': colors['primary']}),
            " и ",
            html.Span("Давронов Мустафо", style={'color': colors['accent']})
        ], className='authors'),

        daq.ToggleSwitch(
            id='theme-switch',
            label='Тёмная тема',
            value=False,
            style={'margin': '20px 0'}
        )
    ], className='container')
], id='main-container')

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
        html.H4("Сводная статистика", style={'color': colors['card_background'], 'marginBottom': '10px'}),
        html.P(f"Средний процент интернет-пользователей: {avg_internet_users:.2f}%", style={'marginBottom': '5px'}),
        html.P(f"Среднее количество мобильных подписок: {avg_mobile_subs:.2f}", style={'marginBottom': '5px'}),
        html.P(f"Среднее количество широкополосных подписок: {avg_broadband_subs:.2f}")
    ])

@app.callback(
    Output('tab-content', 'children'),
    [Input(f'tab-{i}', 'n_clicks') for i in range(1, 8)] +
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
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

    layout = go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='"SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif', color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode='closest',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),
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
    
    return [
        dcc.Graph(figure=fig, config={'displayModeBar': False}),
        html.P(description, style={'marginTop': '10px', 'fontSize': '14px', 'color': colors['secondary']})
    ]

@app.callback(
    [Output('main-container', 'style'),
     Output('tab-content', 'style'),
     Output('refresh-button', 'style')],
    [Input('theme-switch', 'value')]
)
def update_theme(dark_theme):
    if dark_theme:
        return [
            {'backgroundColor': dark_colors['background'], 'color': dark_colors['text']},
            {'backgroundColor': dark_colors['card_background']},
            {'backgroundColor': dark_colors['primary'], 'color': dark_colors['text']}
        ]
    else:
        return [
            {'backgroundColor': colors['background'], 'color': colors['text']},
            {'backgroundColor': colors['card_background']},
            {'backgroundColor': colors['primary'], 'color': colors['card_background']}
        ]

@app.callback(
    Output('country-dropdown', 'style'),
    [Input('theme-switch', 'value')]
)
def update_dropdown_style(dark_theme):
    if dark_theme:
        return {'backgroundColor': dark_colors['card_background'], 'color': dark_colors['text']}
    else:
        return {'backgroundColor': colors['card_background'], 'color': colors['text']}

@app.callback(
    Output('year-slider-container', 'style'),
    [Input('theme-switch', 'value')]
)
def update_slider_container_style(dark_theme):
    if dark_theme:
        return {'backgroundColor': dark_colors['card_background'], 'padding': '10px', 'borderRadius': '8px'}
    else:
        return {'backgroundColor': colors['card_background'], 'padding': '10px', 'borderRadius': '8px'}

@app.callback(
    [Output(f'tab-{i}', 'style') for i in range(1, 8)],
    [Input('theme-switch', 'value')]
)
def update_menu_item_style(dark_theme):
    if dark_theme:
        return [{'backgroundColor': dark_colors['tertiary'], 'color': dark_colors['text']}] * 7
    else:
        return [{'backgroundColor': colors['tertiary'], 'color': colors['text']}] * 7

@app.callback(
    Output('df-store', 'data'),
    [Input('refresh-button', 'n_clicks')]
)
def refresh_data(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    return get_data_from_db().to_json(date_format='iso', orient='split')

if __name__ == '__main__':
    app.run_server(debug=True)

server = app.server
    