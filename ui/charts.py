"""Plotly chart builders for Contract Shield."""
import plotly.graph_objects as go
import streamlit as st


def render_risk_donut(high: int, medium: int, low: int, total_findings: int):
    """Interactive risk breakdown donut chart."""
    if total_findings == 0:
        st.markdown("""
        <div style="display:flex; align-items:center; justify-content:center;
                    height:200px; color:#7888aa; font-size:0.9rem;">✅ Clean — no issues!</div>
        """, unsafe_allow_html=True)
        return

    fig = go.Figure(data=[go.Pie(
        labels=["HIGH", "MEDIUM", "LOW"],
        values=[high, medium, low],
        hole=0.65,
        marker=dict(
            colors=["#ff4444", "#ff9f43", "#ffd166"],
            line=dict(color="#0a0f1e", width=3),
        ),
        textinfo="label+value",
        textfont=dict(size=11, color="#e8eaf6", family="Inter"),
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
            text=f"<b>{total_findings}</b><br><span style='font-size:10px;color:#7888aa'>Issues</span>",
            x=0.5, y=0.5, font=dict(size=22, color="#e8eaf6", family="Inter"),
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
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(0,255,136,0.1)',
        line=dict(color='#00ff88', width=2),
        marker=dict(size=6, color='#00ff88'),
        hovertemplate="%{theta}: %{r}/100<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor='rgba(255,255,255,0.06)',
                linecolor='rgba(255,255,255,0.06)',
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.06)',
                linecolor='rgba(255,255,255,0.06)',
                tickfont=dict(size=10, color='#c8cfe8', family='Inter'),
            ),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=60, t=20, b=20),
        height=280,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
