import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Importar procesador de datos
from data_processor import DataProcessor

# Inicializar app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Para deployment

app.title = "Case Counter Pro - Análisis de Impacto"

# Colores corporativos
colors = {
    'background': '#f8f9fa',
    'text': '#212529',
    'primary': '#0d6efd',
    'success': '#198754',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'light': '#e9ecef'
}

# Layout principal
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("📊 Case Counter Pro - Dashboard de Análisis de Impacto",
                style={'textAlign': 'center', 'color': colors['primary'], 'marginBottom': 10, 'fontSize': '2.5em'}),
        html.P("Análisis de correlación entre uso de extensión y desempeño del equipo",
               style={'textAlign': 'center', 'color': colors['text'], 'fontSize': 18, 'marginBottom': 0})
    ], style={'backgroundColor': 'white', 'padding': '30px', 'marginBottom': '20px', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
    
    # Filtros
    html.Div([
        html.Div([
            html.Label("📅 Seleccionar Día:", style={'fontWeight': 'bold', 'fontSize': 16, 'marginBottom': 10}),
            dcc.Dropdown(
                id='day-filter',
                options=[
                    {'label': '🗓️ 19/11/2025 - Miércoles', 'value': '19/11/2025'},
                    {'label': '🗓️ 20/11/2025 - Jueves', 'value': '20/11/2025'},
                    {'label': '🗓️ 21/11/2025 - Viernes', 'value': '21/11/2025'},
                    {'label': '🗓️ 24/11/2025 - Lunes', 'value': '24/11/2025'},
                    {'label': '📊 Todos los días (Promedio)', 'value': 'all'}
                ],
                value='all',
                clearable=False,
                style={'fontSize': 14}
            )
        ], style={'width': '100%'}),
    ], style={'backgroundColor': 'white', 'padding': '20px', 'marginBottom': '20px', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
    
    # KPIs principales
    html.Div(id='kpi-cards', style={'marginBottom': '20px'}),
    
    # Gráficos principales - Fila 1
    html.Div([
        html.Div([
            dcc.Graph(id='scatter-uso-productividad')
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        html.Div([
            dcc.Graph(id='bar-top-performers')
        ], style={'width': '49%', 'display': 'inline-block', 'marginLeft': '2%', 'verticalAlign': 'top'})
    ], style={'marginBottom': '20px'}),
    
    # Gráficos principales - Fila 2
    html.Div([
        html.Div([
            dcc.Graph(id='heatmap-uso')
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        html.Div([
            dcc.Graph(id='line-evolucion')
        ], style={'width': '49%', 'display': 'inline-block', 'marginLeft': '2%', 'verticalAlign': 'top'})
    ], style={'marginBottom': '20px'}),
    
    # Tabla de anomalías
    html.Div([
        html.H3("⚠️ Anomalías Detectadas", style={'color': colors['danger'], 'marginBottom': 15}),
        html.Div(id='anomalias-table')
    ], style={'backgroundColor': 'white', 'padding': '25px', 'marginBottom': '20px', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
    
    # Análisis detallado
    html.Div([
        html.H3("📋 Análisis Detallado por Representante", style={'color': colors['primary'], 'marginBottom': 15}),
        html.Div(id='detailed-analysis')
    ], style={'backgroundColor': 'white', 'padding': '25px', 'marginBottom': '20px', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
    
    # Recomendaciones
    html.Div([
        html.H3("💡 Recomendaciones Accionables", style={'color': colors['success'], 'marginBottom': 15}),
        html.Div(id='recommendations')
    ], style={'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
    
    # Footer
    html.Div([
        html.P("📊 Dashboard creado para análisis de Case Counter Pro | Actualizado: Noviembre 2025", 
               style={'textAlign': 'center', 'color': 'gray', 'fontSize': 12, 'margin': 0})
    ], style={'marginTop': '30px', 'padding': '15px'})
    
], style={'backgroundColor': colors['background'], 'padding': '20px', 'fontFamily': 'Arial, sans-serif', 'maxWidth': '1400px', 'margin': '0 auto'})


# Callbacks
@app.callback(
    [Output('kpi-cards', 'children'),
     Output('scatter-uso-productividad', 'figure'),
     Output('bar-top-performers', 'figure'),
     Output('heatmap-uso', 'figure'),
     Output('line-evolucion', 'figure'),
     Output('anomalias-table', 'children'),
     Output('detailed-analysis', 'children'),
     Output('recommendations', 'children')],
    [Input('day-filter', 'value')]
)
def update_dashboard(selected_day):
    # Cargar datos
    processor = DataProcessor()
    
    # KPIs
    kpis = processor.calculate_kpis(selected_day)
    kpi_cards = create_kpi_cards(kpis)
    
    # Scatter plot
    scatter_fig = processor.create_scatter_plot(selected_day)
    
    # Barras top performers
    bar_fig = processor.create_top_performers_bar(selected_day)
    
    # Heatmap
    heatmap_fig = processor.create_heatmap()
    
    # Líneas evolución
    line_fig = processor.create_evolution_lines()
    
    # Anomalías
    anomalias = processor.detect_anomalies(selected_day)
    anomalias_table = create_anomalies_table(anomalias)
    
    # Análisis detallado
    detailed = processor.detailed_rep_analysis(selected_day)
    detailed_div = create_detailed_analysis(detailed)
    
    # Recomendaciones
    recommendations = processor.generate_recommendations()
    recommendations_div = create_recommendations(recommendations)
    
    return kpi_cards, scatter_fig, bar_fig, heatmap_fig, line_fig, anomalias_table, detailed_div, recommendations_div


def create_kpi_cards(kpis):
    """Crear tarjetas de KPIs"""
    kpi_style_base = {
        'backgroundColor': 'white', 
        'padding': '25px', 
        'borderRadius': '15px', 
        'textAlign': 'center',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'transition': 'transform 0.3s ease'
    }
    
    return html.Div([
        # Correlación
        html.Div([
            html.Div("📊", style={'fontSize': '3em', 'marginBottom': 10}),
            html.H4("Correlación", style={'color': colors['text'], 'marginBottom': 10, 'fontSize': 16}),
            html.H2(f"{kpis['correlacion']:.2f}", 
                   style={'color': colors['primary'], 'margin': 0, 'fontSize': '2.5em'}),
            html.P("Uso vs Productividad", style={'fontSize': 12, 'color': 'gray', 'marginTop': 10})
        ], style={**kpi_style_base, 'width': '23%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        # Promedio uso
        html.Div([
            html.Div("🔧", style={'fontSize': '3em', 'marginBottom': 10}),
            html.H4("Uso Promedio", style={'color': colors['text'], 'marginBottom': 10, 'fontSize': 16}),
            html.H2(f"{kpis['uso_promedio']:.1f}%", 
                   style={'color': colors['success'], 'margin': 0, 'fontSize': '2.5em'}),
            html.P("Extensión CCP", style={'fontSize': 12, 'color': 'gray', 'marginTop': 10})
        ], style={**kpi_style_base, 'width': '23%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        # Productividad promedio
        html.Div([
            html.Div("⚡", style={'fontSize': '3em', 'marginBottom': 10}),
            html.H4("Productividad", style={'color': colors['text'], 'marginBottom': 10, 'fontSize': 16}),
            html.H2(f"{kpis['productividad_promedio']:.1f}", 
                   style={'color': colors['warning'], 'margin': 0, 'fontSize': '2.5em'}),
            html.P("Casos/Jornada", style={'fontSize': 12, 'color': 'gray', 'marginTop': 10})
        ], style={**kpi_style_base, 'width': '23%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        # Casos totales
        html.Div([
            html.Div("📦", style={'fontSize': '3em', 'marginBottom': 10}),
            html.H4("Casos Totales", style={'color': colors['text'], 'marginBottom': 10, 'fontSize': 16}),
            html.H2(f"{kpis['casos_totales']}", 
                   style={'color': colors['danger'], 'margin': 0, 'fontSize': '2.5em'}),
            html.P("Periodo analizado", style={'fontSize': 12, 'color': 'gray', 'marginTop': 10})
        ], style={**kpi_style_base, 'width': '23%', 'display': 'inline-block'})
    ])


def create_anomalies_table(anomalias):
    """Crear tabla de anomalías"""
    if anomalias.empty:
        return html.Div([
            html.Div("✅", style={'fontSize': '4em', 'textAlign': 'center', 'marginBottom': 15}),
            html.P("No se detectaron anomalías significativas", 
                   style={'color': colors['success'], 'fontSize': 18, 'textAlign': 'center', 'fontWeight': 'bold'})
        ])
    
    return dash_table.DataTable(
        data=anomalias.to_dict('records'),
        columns=[{"name": i, "id": i} for i in anomalias.columns],
        style_cell={
            'textAlign': 'left', 
            'padding': '12px',
            'fontSize': 14,
            'fontFamily': 'Arial'
        },
        style_header={
            'backgroundColor': colors['danger'], 
            'color': 'white', 
            'fontWeight': 'bold',
            'fontSize': 15
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_table={'overflowX': 'auto'}
    )


def create_detailed_analysis(detailed):
    """Crear análisis detallado"""
    if not detailed:
        return html.P("No hay datos disponibles para análisis detallado", style={'textAlign': 'center', 'color': 'gray'})
    
    elements = []
    for rep, data in detailed.items():
        elements.append(html.Div([
            html.H4(f"👤 {rep}", style={'color': colors['primary'], 'marginBottom': 12, 'fontSize': 20}),
            dcc.Markdown(data['analisis'], style={'lineHeight': '1.8', 'fontSize': 14}),
            html.Hr(style={'margin': '20px 0', 'border': '1px solid #e9ecef'})
        ]))
    return html.Div(elements)


def create_recommendations(recommendations):
    """Crear recomendaciones"""
    if not recommendations:
        return html.P("No hay recomendaciones disponibles", style={'textAlign': 'center', 'color': 'gray'})
    
    elements = []
    for i, rec in enumerate(recommendations, 1):
        elements.append(html.Div([
            html.H4(f"{i}. {rec['titulo']}", style={'color': colors['success'], 'marginBottom': 12, 'fontSize': 19}),
            html.P(rec['descripcion'], style={'lineHeight': '1.7', 'fontSize': 15, 'marginBottom': 15}),
            html.Ul([html.Li(action, style={'marginBottom': 8, 'fontSize': 14}) for action in rec['acciones']]),
            html.Hr(style={'margin': '25px 0', 'border': '1px solid #e9ecef'})
        ], style={'marginBottom': 20}))
    return html.Div(elements)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
