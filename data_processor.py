import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

class DataProcessor:
    def __init__(self):
        """Inicializar con los datos del reporte"""
        self.data = self.load_data()
        self.days = ['19/11/2025', '20/11/2025', '21/11/2025', '24/11/2025']
        
    def load_data(self):
        """Cargar datos desde el reporte"""
        data = {
            '19/11/2025': [
                {'rep': 'agaravito', 'casos': 22, 'uso_ext': 94, 'productividad': 3.7},
                {'rep': 'dancastrosal', 'casos': 30, 'uso_ext': 85, 'productividad': 4.1},
                {'rep': 'jcolmenares', 'casos': 32, 'uso_ext': 100, 'productividad': 3.6},
                {'rep': 'jsolerovalle', 'casos': 8, 'uso_ext': 32, 'productividad': 4.0},
                {'rep': 'mdiazgaray', 'casos': 10, 'uso_ext': 88, 'productividad': 3.8},
                {'rep': 'mlosadavarga', 'casos': 39, 'uso_ext': 82, 'productividad': 4.5},
                {'rep': 'uaguerrero', 'casos': 32, 'uso_ext': 89, 'productividad': 4.1}
            ],
            '20/11/2025': [
                {'rep': 'agaravito', 'casos': 18, 'uso_ext': 95, 'productividad': 3.9},
                {'rep': 'dancastrosal', 'casos': 16, 'uso_ext': 0, 'productividad': 5.2},
                {'rep': 'jcolmenares', 'casos': 17, 'uso_ext': 97, 'productividad': 6.5},
                {'rep': 'jsolerovalle', 'casos': 13, 'uso_ext': 25, 'productividad': 1.7},
                {'rep': 'mdiazgaray', 'casos': 12, 'uso_ext': 50, 'productividad': 2.8},
                {'rep': 'mlosadavarga', 'casos': 14, 'uso_ext': 95, 'productividad': 7.8},
                {'rep': 'tarango', 'casos': 14, 'uso_ext': 100, 'productividad': 4.5},
                {'rep': 'uaguerrero', 'casos': 17, 'uso_ext': 94, 'productividad': 5.2}
            ],
            '21/11/2025': [
                {'rep': 'agaravito', 'casos': 7, 'uso_ext': 94, 'productividad': 5.5},
                {'rep': 'bsarmiento', 'casos': 11, 'uso_ext': 96, 'productividad': 4.6},
                {'rep': 'dancastrosal', 'casos': 10, 'uso_ext': 19, 'productividad': 3.3},
                {'rep': 'jcolmenares', 'casos': 10, 'uso_ext': 94, 'productividad': 5.9},
                {'rep': 'jsolerovalle', 'casos': 15, 'uso_ext': 8, 'productividad': 3.3},
                {'rep': 'mdiazgaray', 'casos': 12, 'uso_ext': 75, 'productividad': 3.7},
                {'rep': 'mlosadavarga', 'casos': 18, 'uso_ext': 100, 'productividad': 5.3},
                {'rep': 'tarango', 'casos': 15, 'uso_ext': 100, 'productividad': 3.8},
                {'rep': 'uaguerrero', 'casos': 15, 'uso_ext': 100, 'productividad': 6.7}
            ],
            '24/11/2025': [
                {'rep': 'agaravito', 'casos': 25, 'uso_ext': 114, 'productividad': 3.1},
                {'rep': 'bsarmiento', 'casos': 21, 'uso_ext': 91, 'productividad': 4.5},
                {'rep': 'dancastrosal', 'casos': 23, 'uso_ext': 40, 'productividad': 5.1},
                {'rep': 'jcolmenares', 'casos': 24, 'uso_ext': 100, 'productividad': 3.0},
                {'rep': 'jsolerovalle', 'casos': 17, 'uso_ext': 53, 'productividad': 4.6},
                {'rep': 'mdiazgaray', 'casos': 20, 'uso_ext': 100, 'productividad': 3.7},
                {'rep': 'mlosadavarga', 'casos': 29, 'uso_ext': 100, 'productividad': 6.2},
                {'rep': 'tarango', 'casos': 7, 'uso_ext': 93, 'productividad': 6.0},
                {'rep': 'uaguerrero', 'casos': 24, 'uso_ext': 100, 'productividad': 5.2}
            ]
        }
        
        # Convertir a DataFrame
        all_data = []
        for day, records in data.items():
            for record in records:
                if record.get('productividad', 0) > 0:  # Solo incluir registros válidos
                    record['dia'] = day
                    all_data.append(record)
        
        return pd.DataFrame(all_data)
    
    def calculate_kpis(self, selected_day='all'):
        """Calcular KPIs principales"""
        df = self.data if selected_day == 'all' else self.data[self.data['dia'] == selected_day]
        
        if df.empty:
            return {
                'correlacion': 0,
                'uso_promedio': 0,
                'productividad_promedio': 0,
                'casos_totales': 0
            }
        
        return {
            'correlacion': df['uso_ext'].corr(df['productividad']),
            'uso_promedio': df['uso_ext'].mean(),
            'productividad_promedio': df['productividad'].mean(),
            'casos_totales': int(df['casos'].sum())
        }
    
    def create_scatter_plot(self, selected_day='all'):
        """Crear scatter plot Uso vs Productividad"""
        df = self.data if selected_day == 'all' else self.data[self.data['dia'] == selected_day]
        
        if df.empty:
            return go.Figure().add_annotation(text="No hay datos disponibles", showarrow=False)
        
        fig = px.scatter(
            df, 
            x='uso_ext', 
            y='productividad',
            size='casos',
            color='rep',
            hover_data=['dia', 'casos'],
            title='📈 Uso de Extensión vs Productividad',
            labels={'uso_ext': 'Uso Extensión (%)', 'productividad': 'Productividad (casos/jornada)', 'rep': 'Representante'},
            trendline='ols'
        )
        
        fig.update_layout(
            xaxis_title='Uso de Extensión (%)',
            yaxis_title='Productividad (casos/jornada)',
            height=500,
            showlegend=True,
            template='plotly_white',
            font=dict(size=12)
        )
        
        return fig
    
    def create_top_performers_bar(self, selected_day='all'):
        """Crear gráfico de barras top performers"""
        df = self.data if selected_day == 'all' else self.data[self.data['dia'] == selected_day]
        
        if df.empty:
            return go.Figure().add_annotation(text="No hay datos disponibles", showarrow=False)
        
        # Agrupar por rep y promediar si es "all"
        if selected_day == 'all':
            df = df.groupby('rep').agg({
                'productividad': 'mean',
                'uso_ext': 'mean',
                'casos': 'sum'
            }).reset_index()
        
        # Top 5 por productividad
        top_5 = df.nlargest(5, 'productividad')
        
        fig = go.Figure()
        
        # Barras de productividad
        fig.add_trace(go.Bar(
            name='Productividad',
            x=top_5['rep'],
            y=top_5['productividad'],
            yaxis='y',
            marker_color='#0d6efd',
            text=top_5['productividad'].round(1),
            textposition='outside'
        ))
        
        # Línea de uso extensión
        fig.add_trace(go.Scatter(
            name='Uso Extensión (%)',
            x=top_5['rep'],
            y=top_5['uso_ext'],
            yaxis='y2',
            marker_color='#198754',
            mode='lines+markers',
            line=dict(width=3)
        ))
        
        fig.update_layout(
            title='📊 Top 5 Performers: Productividad vs Uso de Extensión',
            xaxis_title='Representante',
            yaxis=dict(title='Productividad', side='left'),
            yaxis2=dict(title='Uso Extensión (%)', overlaying='y', side='right', range=[0, 120]),
            height=500,
            template='plotly_white',
            font=dict(size=12)
        )
        
        return fig
    
    def create_heatmap(self):
        """Crear heatmap de uso de extensión"""
        pivot = self.data.pivot_table(values='uso_ext', index='rep', columns='dia', aggfunc='mean')
        
        if pivot.empty:
            return go.Figure().add_annotation(text="No hay datos disponibles", showarrow=False)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='RdYlGn',
            text=np.round(pivot.values, 0),
            texttemplate='%{text:.0f}%',
            textfont={"size": 11},
            colorbar=dict(title="Uso (%)")
        ))
        
        fig.update_layout(
            title='🔥 Heatmap: Uso de Extensión por Rep y Día',
            xaxis_title='Día',
            yaxis_title='Representante',
            height=500,
            template='plotly_white',
            font=dict(size=12)
        )
        
        return fig
    
    def create_evolution_lines(self):
        """Crear líneas de evolución por grupos de uso"""
        # Clasificar reps por uso promedio
        uso_promedio = self.data.groupby('rep')['uso_ext'].mean()
        
        def clasificar_uso(rep):
            if rep not in uso_promedio.index:
                return 'Sin datos'
            uso = uso_promedio[rep]
            if uso >= 80:
                return 'Alto uso (≥80%)'
            elif uso >= 50:
                return 'Uso medio (50-79%)'
            else:
                return 'Bajo uso (<50%)'
        
        self.data['grupo_uso'] = self.data['rep'].apply(clasificar_uso)
        
        # Productividad promedio por grupo y día
        df_grouped = self.data.groupby(['dia', 'grupo_uso'])['productividad'].mean().reset_index()
        
        if df_grouped.empty:
            return go.Figure().add_annotation(text="No hay datos disponibles", showarrow=False)
        
        fig = px.line(
            df_grouped,
            x='dia',
            y='productividad',
            color='grupo_uso',
            markers=True,
            title='📉 Evolución de Productividad por Grupo de Uso',
            labels={'productividad': 'Productividad Promedio', 'dia': 'Día', 'grupo_uso': 'Grupo'}
        )
        
        fig.update_layout(
            height=500,
            template='plotly_white',
            font=dict(size=12)
        )
        
        return fig
    
    def detect_anomalies(self, selected_day='all'):
        """Detectar anomalías en los datos"""
        df = self.data if selected_day == 'all' else self.data[self.data['dia'] == selected_day]
        
        if df.empty:
            return pd.DataFrame()
        
        anomalias = []
        
        # Anomalía 1: Alta productividad con bajo uso
        high_prod_low_use = df[(df['productividad'] >= 5.0) & (df['uso_ext'] < 50)]
        for _, row in high_prod_low_use.iterrows():
            anomalias.append({
                'Tipo': '⚠️ Alta productividad - Bajo uso',
                'Rep': row['rep'],
                'Día': row['dia'],
                'Uso': f"{row['uso_ext']:.0f}%",
                'Productividad': f"{row['productividad']:.1f}",
                'Casos': int(row['casos']),
                'Observación': 'Potencial para mejorar con más uso de extensión'
            })
        
        # Anomalía 2: Uso muy bajo consistente
        uso_muy_bajo = df[df['uso_ext'] < 30]
        for _, row in uso_muy_bajo.iterrows():
            anomalias.append({
                'Tipo': '❌ Uso crítico de extensión',
                'Rep': row['rep'],
                'Día': row['dia'],
                'Uso': f"{row['uso_ext']:.0f}%",
                'Productividad': f"{row['productividad']:.1f}",
                'Casos': int(row['casos']),
                'Observación': 'Requiere coaching urgente sobre uso de herramienta'
            })
        
        return pd.DataFrame(anomalias)
    
    def detailed_rep_analysis(self, selected_day='all'):
        """Análisis detallado por representante"""
        df = self.data if selected_day == 'all' else self.data[self.data['dia'] == selected_day]
        
        if df.empty:
            return {}
        
        analysis = {}
        
        for rep in df['rep'].unique():
            rep_data = df[df['rep'] == rep]
            
            uso_prom = rep_data['uso_ext'].mean()
            prod_prom = rep_data['productividad'].mean()
            casos_total = int(rep_data['casos'].sum())
            dias_trabajados = len(rep_data)
            
            # Clasificación
            if uso_prom >= 80 and prod_prom >= 4.5:
                clasificacion = "⭐ **EXCELENTE**"
            elif uso_prom >= 80:
                clasificacion = "✅ **Buen uso de herramienta**"
            elif prod_prom >= 4.5:
                clasificacion = "💪 **Alto rendimiento** (puede mejorar con más uso)"
            else:
                clasificacion = "📈 **Oportunidad de mejora**"
            
            analisis_texto = f"""
{clasificacion}

- 📊 **Uso promedio extensión**: {uso_prom:.1f}%
- ⚡ **Productividad promedio**: {prod_prom:.1f} casos/jornada
- 📦 **Total casos gestionados**: {casos_total} en {dias_trabajados} día(s)
            """
            
            analysis[rep] = {'analisis': analisis_texto}
        
        return analysis
    
    def generate_recommendations(self):
        """Generar recomendaciones accionables"""
        df = self.data
        
        if df.empty:
            return []
        
        # Identificar grupos
        high_use_high_prod = df[(df['uso_ext'] >= 80) & (df['productividad'] >= 4.5)]['rep'].unique()
        low_use_any_prod = df[df['uso_ext'] < 50]['rep'].unique()
        high_prod_low_use = df[(df['productividad'] >= 5.0) & (df['uso_ext'] < 50)]['rep'].unique()
        
        recommendations = []
        
        # Recomendación 1: Best practices
        if len(high_use_high_prod) > 0:
            recommendations.append({
                'titulo': '⭐ Replicar Best Practices',
                'descripcion': f'Los siguientes reps combinan alto uso de extensión (≥80%) con alta productividad (≥4.5): **{", ".join(high_use_high_prod[:5])}**',
                'acciones': [
                    'Realizar sesiones de shadowing para compartir técnicas',
                    'Documentar sus flujos de trabajo como estándar',
                    'Reconocer públicamente su desempeño para motivar al equipo'
                ]
            })
        
        # Recomendación 2: Coaching uso bajo
        if len(low_use_any_prod) > 0:
            recommendations.append({
                'titulo': '🎯 Coaching Prioritario en Uso de Extensión',
                'descripcion': f'Los siguientes reps tienen uso bajo (<50%): **{", ".join(low_use_any_prod)}**',
                'acciones': [
                    'Sesión 1:1 para identificar barreras de adopción',
                    'Capacitación práctica sobre beneficios y funciones clave',
                    'Establecer metas incrementales de uso (ej: 70% en 2 semanas)',
                    'Seguimiento semanal para verificar mejoras'
                ]
            })
        
        # Recomendación 3: Potencial sin explotar
        if len(high_prod_low_use) > 0:
            recommendations.append({
                'titulo': '💎 Potencial Sin Explotar',
                'descripcion': f'Los siguientes reps tienen alta productividad pero bajo uso de extensión: **{", ".join(high_prod_low_use)}**',
                'acciones': [
                    'Son candidatos ideales para mostrar el valor incremental de la extensión',
                    'Pueden convertirse en top performers con mejor adopción',
                    'Enfatizar cómo la extensión puede llevar su desempeño al siguiente nivel'
                ]
            })
        
        # Recomendación 4: Monitoreo continuo
        recommendations.append({
            'titulo': '📊 Monitoreo y Análisis Continuo',
            'descripcion': 'Implementar seguimiento sistemático de métricas',
            'acciones': [
                'Dashboard semanal con estas métricas',
                'Revisiones mensuales de correlación uso-productividad',
                'Ajustar metas y estrategias basadas en datos',
                'Celebrar wins y mejoras en adopción'
            ]
        })
        
        return recommendations
