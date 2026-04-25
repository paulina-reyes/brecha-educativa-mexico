import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# CARGA DE DATOS

df = pd.read_csv("data/clean/brecha_educativa_estados.csv")

orden_rezago = ["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"]

colores_rezago = {
    "Muy bajo": "#065F46",
    "Bajo": "#10B981",
    "Medio": "#F59E0B",
    "Alto": "#EF4444",
    "Muy alto": "#7F1D1D"
}

GITHUB_URL = "https://github.com/paulina-reyes/brecha-educativa-mexico"

# APP

app = Dash(__name__)
server = app.server
app.title = "Brecha educativa en México"

# ESTILOS

PAGE_STYLE = {
    "fontFamily": "'Segoe UI', Arial, sans-serif",
    "background": "linear-gradient(to bottom, #F9FAFB, #EEF2F7)",
    "color": "#1F2933",
    "margin": "0",
    "padding": "0"
}

CONTAINER_STYLE = {
    "maxWidth": "1180px",
    "margin": "0 auto",
    "padding": "42px 28px"
}

CARD_STYLE = {
    "backgroundColor": "#FFFFFF",
    "padding": "30px",
    "borderRadius": "16px",
    "boxShadow": "0 10px 30px rgba(0,0,0,0.06)",
    "marginBottom": "30px",
    "border": "1px solid #E5E7EB"
}

TEXT_STYLE = {
    "fontSize": "17px",
    "lineHeight": "1.75",
    "color": "#374151"
}

SECTION_TITLE = {
    "fontSize": "27px",
    "marginBottom": "12px",
    "color": "#111827"
}

GRAPH_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "toImageButtonOptions": {
        "format": "png",
        "filename": "grafica_brecha_educativa",
        "height": 700,
        "width": 1100,
        "scale": 2
    }
}

def formato_figura(fig):
    fig.update_layout(
        template="plotly_white",
        font=dict(
            family="Segoe UI, Arial, sans-serif",
            size=14,
            color="#1F2933"
        ),
        title=dict(
            font=dict(size=22, color="#111827"),
            x=0.02,
            xanchor="left"
        ),
        legend=dict(
            title="Grado de rezago social",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Segoe UI"
        ),
        margin=dict(l=50, r=30, t=90, b=80),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF"
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E5E7EB",
        zeroline=True,
        zerolinecolor="#CBD5E1"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E5E7EB",
        zeroline=True,
        zerolinecolor="#CBD5E1"
    )

    return fig


# LAYOUT

app.layout = html.Div(
    style=PAGE_STYLE,
    children=[

        # HEADER
        html.Div(
            style={
                "background": "linear-gradient(135deg, #064E3B 0%, #065F46 48%, #10B981 100%)",
                "color": "white",
                "padding": "28px 40px",
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "boxShadow": "0 8px 24px rgba(6, 78, 59, 0.25)"
            },
            children=[
                html.Div(
                    children=[
                        html.Div(
                            "Brecha educativa en México",
                            style={
                                "fontSize": "34px",
                                "fontWeight": "700",
                                "letterSpacing": "-0.5px"
                            }
                        ),
                        html.Div(
                            " La lotería educativa del Sistema Educativo Nacional",
                            style={
                                "fontSize": "17px",
                                "color": "#D1FAE5",
                                "marginTop": "6px"
                            }
                        )
                    ]
                ),

                html.A(
                    "Ver en GitHub",
                    href=GITHUB_URL,
                    target="_blank",
                    style={
                        "border": "1px solid #D1FAE5",
                        "color": "#D1FAE5",
                        "padding": "11px 18px",
                        "borderRadius": "8px",
                        "textDecoration": "none",
                        "fontWeight": "600",
                        "fontSize": "15px",
                        "backgroundColor": "rgba(255,255,255,0.06)"
                    }
                )
            ]
        ),

        html.Div(
            style=CONTAINER_STYLE,
            children=[

                # INTRO
                html.Div(
                    style=CARD_STYLE,
                    children=[
                        html.H1(
                            "¿Dónde naces determina hasta dónde llegas?",
                            style={
                                "fontSize": "40px",
                                "marginTop": "0",
                                "marginBottom": "10px",
                                "color": "#064E3B"
                            }
                        ),

                        html.P(
                            "Una narrativa visual sobre cómo las condiciones sociales se relacionan "
                            "con el analfabetismo, el abandono escolar y la escolaridad promedio en México.",
                            style={
                                "fontSize": "19px",
                                "lineHeight": "1.7",
                                "color": "#4B5563",
                                "marginBottom": "24px"
                            }
                        ),

                        html.H2("Pregunta de investigación", style=SECTION_TITLE),

                        html.P(
                            "¿De qué manera las condiciones de rezago social influyen en las distintas dimensiones de la brecha educativa en México?",
                            style={
                                "fontSize": "21px",
                                "fontWeight": "600",
                                "color": "#065F46",
                                "lineHeight": "1.6"
                            }
                        ),

                        html.P(
                            "El análisis utiliza el Índice de Rezago Social de CONEVAL 2020 y los "
                            "indicadores educativos de la SEP para el ciclo 2022–2023. La comparación "
                            "se realiza a nivel estatal para observar patrones territoriales de desigualdad.",
                            style=TEXT_STYLE
                        )
                    ]
                ),

                # GRAFICA 1
                html.Div(
                    style=CARD_STYLE,
                    children=[
                        html.H2("1. El contexto social también es educativo", style=SECTION_TITLE),

                        html.P(
                            "Esta visualización presenta la relación entre el índice de rezago social y el porcentaje de analfabetismo a nivel estatal. ",
                            style=TEXT_STYLE
                        ),

                        dcc.Graph(
                            config=GRAPH_CONFIG,
                            figure=(
                                lambda fig: (
                                    fig.update_traces(
                                        selector=dict(mode="lines"),
                                        showlegend=False,
                                        line=dict(width=3)
                                    ),
                                    formato_figura(fig)
                                )[1]
                            )(
                                px.scatter(
                                    df,
                                    x="rezago_social",
                                    y="analfabetismo",
                                    size="analfabetismo",
                                    color="grado_rezago_social",
                                    category_orders={"grado_rezago_social": orden_rezago},
                                    color_discrete_map=colores_rezago,
                                    hover_name="estado",
                                    hover_data={
                                        "rezago_social": ":.3f",
                                        "analfabetismo": ":.1f",
                                        "abandono_media_superior": ":.1f",
                                        "escolaridad_promedio": ":.1f",
                                        "grado_rezago_social": True
                                    },
                                    title="Rezago social y analfabetismo por estado",
                                    size_max=46,
                                    trendline="ols",
                                    trendline_scope="overall"
                                ).update_layout(
                                    xaxis_title="Índice de rezago social",
                                    yaxis_title="Analfabetismo (%)",
                                    height=690
                                )
                            )
                        ),
                        html.Div(
                            style={
                                "backgroundColor": "#ECFDF5",
                                "borderLeft": "5px solid #10B981",
                                "padding": "16px 18px",
                                "borderRadius": "10px",
                                "marginTop": "18px"
                            },
                            children=[
                                html.Strong("Interpretación: "),
                                html.Span(
                                    'Los estados con mayor índice de rezago social se concentran en niveles más altos de analfabetismo. ' 
                                    'La distribución de los puntos sugiere una relación positiva entre ambas variables, lo que indica'
                                    'que las carencias sociales están asociadas con desventajas en la educación básica.'
                                )
                            ]
                        )
                    ]
                ),

                # GRAFICA 2
                html.Div(
                    style=CARD_STYLE,
                    children=[
                        html.H2("2. ¿Dónde se rompe la trayectoria escolar?", style=SECTION_TITLE),

                        html.P(
                            "El abandono escolar no debe interpretarse como un fenómeno aislado de un solo "
                            "nivel. Esta visualización permite comparar niveles educativos para observar en " 
                            "qué etapa se concentra el problema en cada entidad.",
                            style=TEXT_STYLE
                        ),

                        html.Div(
                            style={
                                "backgroundColor": "#F9FAFB",
                                "padding": "18px",
                                "borderRadius": "12px",
                                "border": "1px solid #E5E7EB",
                                "marginBottom": "18px"
                            },
                            children=[
                                html.Label(
                                    "Selecciona el nivel educativo:",
                                    style={
                                        "fontWeight": "600",
                                        "color": "#111827",
                                        "marginBottom": "8px",
                                        "display": "block"
                                    }
                                ),
                                dcc.Dropdown(
                                    id="nivel-abandono",
                                    options=[
                                        {"label": "Primaria", "value": "abandono_primaria"},
                                        {"label": "Secundaria", "value": "abandono_secundaria"},
                                        {"label": "Media superior", "value": "abandono_media_superior"},
                                        {"label": "Superior", "value": "abandono_superior"}
                                    ],
                                    value="abandono_media_superior",
                                    clearable=False,
                                    style={"fontSize": "15px"}
                                )
                            ]
                        ),

                        dcc.Graph(id="grafica-abandono", config=GRAPH_CONFIG),

                        html.Div(
                            style={
                                "backgroundColor": "#F0FDF4",
                                "borderLeft": "5px solid #22C55E",
                                "padding": "16px 18px",
                                "borderRadius": "10px",
                                "marginTop": "18px"
                            },
                            children=[
                                html.Strong("Interpretación: "),
                                html.Span(
                                    'El abandono escolar no se distribuye de manera uniforme entre niveles educativos. ' 
                                    'En varios estados, los niveles más altos de abandono se concentran en media superior,'
                                    'lo que sugiere que esta etapa representa un punto crítico en la trayectoria educativa. ' 
                                    'Sin embargo, el comportamiento varía por entidad, lo que indica diferencias estructurales en el sistema educativo.'
                                )
                            ]
                        )
                    ]
                ),

                # GRAFICA 3
                html.Div(
                    style=CARD_STYLE,
                    children=[
                        html.H2("3. El resultado final: escolaridad alcanzada", style=SECTION_TITLE),

                        html.P(
                            "La escolaridad promedio resume hasta dónde llega, en promedio, la población "
                            "de cada estado. Al compararla con el índice de rezago social, se observa como "
                            "las condiciones estructurales están asociadas con los niveles educativos "
                            "alcanzados.",
                            style=TEXT_STYLE
                        ),

                        dcc.Graph(
                            config=GRAPH_CONFIG,
                            figure=(
                                lambda fig: (
                                    fig.update_traces(
                                        selector=dict(mode="lines"),
                                        showlegend=False,
                                        line=dict(width=3)
                                    ),
                                    formato_figura(fig)
                                )[1]
                            )(
                                px.scatter(
                                    df,
                                    x="rezago_social",
                                    y="escolaridad_promedio",
                                    size="escolaridad_promedio",
                                    color="grado_rezago_social",
                                    category_orders={"grado_rezago_social": orden_rezago},
                                    color_discrete_map=colores_rezago,
                                    hover_name="estado",
                                    hover_data={
                                        "rezago_social": ":.3f",
                                        "escolaridad_promedio": ":.1f",
                                        "analfabetismo": ":.1f",
                                        "grado_rezago_social": True
                                    },
                                    title="Rezago social y escolaridad promedio",
                                    size_max=46,
                                    trendline="ols",
                                    trendline_scope="overall"
                                ).update_layout(
                                    xaxis_title="Índice de rezago social",
                                    yaxis_title="Escolaridad promedio",
                                    height=690
                                )
                            )
                        ),
                        html.Div(
                            style={
                                "backgroundColor": "#ECFDF5",
                                "borderLeft": "5px solid #065F46",
                                "padding": "16px 18px",
                                "borderRadius": "10px",
                                "marginTop": "18px"
                            },
                            children=[
                                html.Strong("Interpretación: "),
                                html.Span(
                                    'Se observa una relación negativa entre el rezago social y la escolaridad promedio:'
                                    'a medida que aumentan las carencias sociales, disminuye el nivel educativo alcanzado. ' 
                                    'La tendencia sugiere que las condiciones estructurales no solo afectan el acceso,' 
                                    'sino también la permanencia y culminación de los estudios.'
                                )
                            ]
                        )
                    ]
                ),

                # CONCLUSION
                html.Div(
                    style=CARD_STYLE,
                    children=[
                        html.H2("Conclusión", style=SECTION_TITLE),

                        html.P(
                            'Las visualizaciones muestran que la brecha educativa en México no puede entenderse de manera aislada, ' 
                            'ya que está estrechamente vinculada con las condiciones sociales de cada entidad federativa.',
                            style=TEXT_STYLE
                        ),

                        html.P(
                            'Por un lado, los estados con mayor rezago social tienden a concentrar mayores niveles de analfabetismo,' 
                            'lo que refleja desventajas desde las etapas más básicas del sistema educativo. Por otro lado, el análisis' 
                            'del abandono escolar evidencia que la interrupción de la trayectoria educativa ocurre con mayor intensidad' 
                            'en ciertos niveles, particularmente en media superior, aunque con variaciones importantes entre estados.',
                            style=TEXT_STYLE
                        ),

                        html.P(
                            'Finalmente, la relación entre rezago social y escolaridad promedio sugiere que estas condiciones estructurales' 
                            'no solo afectan el acceso a la educación, sino también la permanencia y el nivel educativo alcanzado.', 
                            style=TEXT_STYLE
                        ),

                        html.P(
                            'En conjunto, los resultados refuerzan la idea de que la desigualdad educativa en México tiene una dimensión' 
                            'territorial clara, donde el contexto social sigue siendo un factor determinante en las oportunidades educativas' 
                            'de la población.', 
                            style=TEXT_STYLE
                        ),

                        html.P(
                            'En conjunto, los datos refuerzan la idea de que el lugar de nacimiento sigue siendo, para la mayoría de las personas, un factor determinante en sus oportunidades educativas.',
                            style={
                                "fontSize": "18px",
                                "fontWeight": "600",
                                "color": "#065F46",
                                "lineHeight": "1.7"
                            }
                        )
                    ]
                ),

                # FUENTES
                html.Div(
                    style={
                        "textAlign": "center",
                        "fontSize": "14px",
                        "color": "#6B7280",
                        "padding": "20px"
                    },
                    children=[
                        html.P(
                            "Fuentes: CONEVAL, Índice de Rezago Social 2020; "
                            "SEP, indicadores educativos por entidad federativa, ciclo 2022–2023."
                        )
                    ]
                )
            ]
        )
    ]
)


# CALLBACK GRAFICA 2

@app.callback(
    Output("grafica-abandono", "figure"),
    Input("nivel-abandono", "value")
)
def actualizar_abandono(nivel):

    nombres = {
        "abandono_primaria": "primaria",
        "abandono_secundaria": "secundaria",
        "abandono_media_superior": "media superior",
        "abandono_superior": "superior"
    }

    datos = df.sort_values(nivel, ascending=False).copy()
    orden_estados = datos["estado"].tolist()

    fig = px.bar(
        datos,
        x="estado",
        y=nivel,
        color=nivel,
        color_continuous_scale="YlGn",
        hover_name="estado",
        hover_data={
            "rezago_social": ":.3f",
            "grado_rezago_social": True,
            "analfabetismo": ":.1f",
            "escolaridad_promedio": ":.1f",
            nivel: ":.1f"
        },
        category_orders={"estado": orden_estados},
        title=f"Abandono escolar en educación {nombres[nivel]} por estado"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Estado",
        yaxis_title="Abandono escolar (%)",
        xaxis_tickangle=-45,
        height=670,
        font=dict(
            family="Segoe UI, Arial, sans-serif",
            size=14,
            color="#1F2933"
        ),
        title=dict(
            font=dict(size=22, color="#111827"),
            x=0.02,
            xanchor="left"
        ),
        coloraxis_colorbar=dict(
            title="Abandono (%)"
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Segoe UI"
        ),
        margin=dict(l=50, r=30, t=90, b=130),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF"
    )

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E5E7EB",
        zeroline=True,
        zerolinecolor="#CBD5E1"
    )

    return fig

server = app.server
if __name__ == "__main__":
    app.run(debug=True)