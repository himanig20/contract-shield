"""Plotly chart builders for Contract Shield."""
import plotly.graph_objects as go
import streamlit as st


def render_risk_donut(high: int, medium: int, low: int, total_findings: int):
    """Interactive risk breakdown donut chart."""
    if total_findings == 0:
        st.markdown("""
        <div style="display:flex; align-items:center; justify-content:center;
                    height:200px; color:var(--text-muted); font-size:0.9rem; font-weight: 500;">Clear — No issues detected</div>
        """, unsafe_allow_html=True)
        return

    fig = go.Figure(data=[go.Pie(
        labels=["HIGH", "MEDIUM", "LOW"],
        values=[high, medium, low],
        hole=0.65,
        marker=dict(
            colors=["#ef4444", "#f59e0b", "#10b981"], # Status colors
            line=dict(color="#ffffff", width=2),
        ),
        textinfo="label+value",
        textfont=dict(size=11, color="#ffffff", family="Inter"),
        hovertemplate="%{label}: %{value} clause(s)<extra></extra>",
        sort=False,
    )])
    fig.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=210,
        annotations=[dict(
            text=f"<b style='color:#0f172a'>{total_findings}</b><br><span style='font-size:11px;color:#64748b'>Issues</span>",
            x=0.5, y=0.5, font=dict(size=22, family="Inter"),
            showarrow=False,
        )],
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_radar_chart(category_scores: dict, category_meta: dict):
    """Spider/radar chart for fairness category breakdown."""
    categories = []
    values = []
    for key, sc in category_scores.items():
        meta = category_meta.get(key, {})
        categories.append(meta.get("label", key))
        values.append(sc)
    # Close the loop
    if categories:
        categories.append(categories[0])
        values.append(values[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(13, 148, 136, 0.1)', # Teal 0.1
        line=dict(color='#0d9488', width=2), # Teal
        marker=dict(size=6, color='#0d9488'),
        hovertemplate="%{theta}: %{r}/100<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor='#e2e8f0', # border
                linecolor='#e2e8f0',
            ),
            angularaxis=dict(
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0',
                tickfont=dict(size=11, color='#64748b', family='Inter'), # muted text
            ),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=60, t=30, b=30),
        height=280,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
