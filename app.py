import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Importar procesador de datos
from data_processor import DataProcessor

# Inicializar app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Case Counter Pro - Análisis de Impacto"

# Colores corporativos
colors = {
    'background': '#f8f9fa',
    'text': '#212529',
    'primary': '#0d6efd',
    'success': '#198754',
    'warning': '#ffc107',
    'danger': '#dc3545'
}

# Layout principal
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("📊 Case Counter Pro - Análisis de Impacto en Productividad",
                style={'textAlign': 'center', 'color': colors['primary'], 'marginBottom': 10}),
        html.P("Análisis de correlación entre uso de extensión y desempeño del equipo",
               style={'textAlign': 'center', 'color': colors['text'], 'fontSize': 16})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'marginBottom': '20px', 'borderRadius': '10px'}),
    
    # Filtros
    html.Div([
        html.Div([
            html.Label("📅 Seleccionar Día:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='day-filter',
                options=[
                    {'label': '19/11/2025 - Miércoles', 'value': '19/11/2025'},
                    {'label': '20/11/2025 - Jueves', 'value': '20/11/2025'},
                    {'label': '21/11/2025 - Viernes', 'value': '21/11/2025'},
                    {'label': '24/11/2025 - Lunes', 'value': '24/11/2025'},
                    {'label': 'Todos los días (Promedio)', 'value': 'all'}
                ],
                value='all',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("👥 Seleccionar Representante:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='rep-filter',
                options=[{'label': 'Todos', 'value': 'all'}],
                value='all',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'marginBottom': '20px', 'borderRadius': '10px'}),
    
    # KPIs principales
    html.Div(id='kpi-cards', style={'marginBottom': '20px'}),
    
    # Gráficos principales
    html.Div([
        # Scatter plot
        html.Div([
            dcc.Graph(id='scatter-uso-productividad')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        # Barras top performers
        html.Div([
            dcc.Graph(id='bar-top-performers')
        ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
    ], style={'marginBottom': '20px'}),
    
    # Heatmap y evolución
    html.Div([
        # Heatmap uso extensión
        html.Div([
            dcc.Graph(id='heatmap-uso')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        # Líneas evolución
        html.Div([
            dcc.Graph(id='line-evolucion')
        ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
    ], style={'marginBottom': '20px'}),
    
    # Tabla de anomalías
    html.Div([
        html.H3("⚠️ Anomalías Detectadas", style={'color': colors['danger']}),
        html.Div(id='anomalias-table')
    ], style={'backgroundColor': 'white', 'padding': '20px', 'marginBottom': '20px', 'borderRadius': '10px'}),
    
    # Análisis detallado
    html.Div([
        html.H3("📋 Análisis Detallado por Representante", style={'color': colors['primary']}),
        html.Div(id='detailed-analysis')
    ], style={'backgroundColor': 'white', 'padding': '20px', 'marginBottom': '20px', 'borderRadius': '10px'}),
    
    # Recomendaciones
    html.Div([
        html.H3("💡 Recomendaciones Accionables", style={'color': colors['success']}),
        html.Div(id='recommendations')
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px'})
    
], style={'backgroundColor': colors['background'], 'padding': '20px', 'fontFamily': 'Arial, sans-serif'})


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
    [Input('day-filter', 'value'),
     Input('rep-filter', 'value')]
)
def update_dashboard(selected_day, selected_rep):
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
    return html.Div([
        # Correlación
        html.Div([
            html.H4("📊 Correlación", style={'color': colors['text'], 'marginBottom': 5}),
            html.H2(f"{kpis['correlacion']:.2f}", 
                   style={'color': colors['primary'], 'margin': 0}),
            html.P("Uso vs Productividad", style={'fontSize': 12, 'color': 'gray'})
        ], style={'width': '23%', 'display': 'inline-block', 'backgroundColor': 'white', 
                 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center', 'marginRight': '2%'}),
        
        # Promedio uso
        html.Div([
            html.H4("🔧 Uso Promedio", style={'color': colors['text'], 'marginBottom': 5}),
            html.H2(f"{kpis['uso_promedio']:.1f}%", 
                   style={'color': colors['success'], 'margin': 0}),
            html.P("Extensión CCP", style={'fontSize': 12, 'color': 'gray'})
        ], style={'width': '23%', 'display': 'inline-block', 'backgroundColor': 'white', 
                 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center', 'marginRight': '2%'}),
        
        # Productividad promedio
        html.Div([
            html.H4("⚡ Productividad", style={'color': colors['text'], 'marginBottom': 5}),
            html.H2(f"{kpis['productividad_promedio']:.1f}", 
                   style={'color': colors['warning'], 'margin': 0}),
            html.P("Casos/Jornada", style={'fontSize': 12, 'color': 'gray'})
        ], style={'width': '23%', 'display': 'inline-block', 'backgroundColor': 'white', 
                 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center', 'marginRight': '2%'}),
        
        # Casos totales
        html.Div([
            html.H4("📦 Casos Totales", style={'color': colors['text'], 'marginBottom': 5}),
            html.H2(f"{kpis['casos_totales']}", 
                   style={'color': colors['danger'], 'margin': 0}),
            html.P("Periodo analizado", style={'fontSize': 12, 'color': 'gray'})
        ], style={'width': '23%', 'display': 'inline-block', 'backgroundColor': 'white', 
                 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center'})
    ])


def create_anomalies_table(anomalias):
    """Crear tabla de anomalías"""
    if anomalias.empty:
        return html.P("✅ No se detectaron anomalías significativas", 
                     style={'color': colors['success'], 'fontSize': 16})
    
    return dash_table.DataTable(
        data=anomalias.to_dict('records'),
        columns=[{"name": i, "id": i} for i in anomalias.columns],
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': colors['danger'], 'color': 'white', 'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )


def create_detailed_analysis(detailed):
    """Crear análisis detallado"""
    elements = []
    for rep, data in detailed.items():
        elements.append(html.Div([
            html.H4(f"👤 {rep}", style={'color': colors['primary'], 'marginBottom': 10}),
            html.P(data['analisis'], style={'lineHeight': '1.6'}),
            html.Hr()
        ]))
    return html.Div(elements)


def create_recommendations(recommendations):
    """Crear recomendaciones"""
    elements = []
    for i, rec in enumerate(recommendations, 1):
        elements.append(html.Div([
            html.H4(f"{i}. {rec['titulo']}", style={'color': colors['success'], 'marginBottom': 10}),
            html.P(rec['descripcion'], style={'lineHeight': '1.6'}),
            html.Ul([html.Li(action) for action in rec['acciones']]),
            html.Hr()
        ]))
    return html.Div(elements)


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
