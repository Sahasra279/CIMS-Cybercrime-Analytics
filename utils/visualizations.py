# ============================================================
# utils/visualizations.py
# Cybercrime Analytics & Visualization System (CIMS)
# ============================================================
# Reusable charting functions built on Matplotlib, Seaborn
# and Plotly. Configured for responsive, non-overflowing
# dark theme rendering on all screen sizes.
# ============================================================

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for Streamlit
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from config import (
    COLORS,
    CHART_BG_COLOR,
    CHART_PAPER_BG,
    CHART_FONT_COLOR,
    CHART_GRID_COLOR,
    PLOTLY_COLOR_SEQUENCE,
    MPL_PALETTE,
)

# ── Matplotlib / Seaborn shared theme ────────────────────────

def apply_dark_mpl_style():
    """Apply dark theme to all subsequent Matplotlib/Seaborn figures."""
    plt.rcParams.update({
        "figure.facecolor":  CHART_BG_COLOR,
        "axes.facecolor":    CHART_BG_COLOR,
        "axes.edgecolor":    CHART_GRID_COLOR,
        "axes.labelcolor":   CHART_FONT_COLOR,
        "axes.titlecolor":   CHART_FONT_COLOR,
        "xtick.color":       CHART_FONT_COLOR,
        "ytick.color":       CHART_FONT_COLOR,
        "text.color":        CHART_FONT_COLOR,
        "grid.color":        CHART_GRID_COLOR,
        "grid.linestyle":    "--",
        "grid.alpha":        0.35,
        "legend.facecolor":  "#1a2235",
        "legend.edgecolor":  CHART_GRID_COLOR,
        "legend.labelcolor": CHART_FONT_COLOR,
        "figure.dpi":        100,
    })
    sns.set_palette(MPL_PALETTE)


# ── Plotly shared layout helper ───────────────────────────────

def plotly_dark_layout(title: str = "", **kwargs) -> dict:
    """
    Return a Plotly layout dict pre-styled for the dark theme.
    Configured with horizontal legends and tight margins to avoid
    horizontal clipping and overflow.
    """
    base = dict(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(color=CHART_FONT_COLOR, size=13),
            x=0.01,
            y=0.96,
        ),
        paper_bgcolor=CHART_PAPER_BG,
        plot_bgcolor=CHART_BG_COLOR,
        font=dict(color=CHART_FONT_COLOR, family="Inter, system-ui, sans-serif", size=11),
        xaxis=dict(gridcolor=CHART_GRID_COLOR, zeroline=False),
        yaxis=dict(gridcolor=CHART_GRID_COLOR, zeroline=False),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.28,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(26,34,53,0.75)",
            bordercolor=CHART_GRID_COLOR,
            borderwidth=1,
            font=dict(color=CHART_FONT_COLOR, size=10),
        ),
        margin=dict(l=35, r=25, t=42, b=38),
        autosize=True,
    )
    base.update(kwargs)
    return base


def create_empty_figure(message: str = "No data available for selected filters") -> go.Figure:
    """Display a clean placeholder figure when filtered data is empty."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=13, color=COLORS["text_secondary"])
    )
    fig.update_layout(**plotly_dark_layout(title="No Data", height=280))
    return fig


# ============================================================
# 1. Plotly interactive charts
# ============================================================

def plotly_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color_col: str | None = None,
    orientation: str = "v",
    text_col: str | None = None,
    show_legend: bool = False,
) -> go.Figure:
    """Interactive bar chart styled for CIMS dark theme."""
    if df.empty:
        return create_empty_figure()

    fig = px.bar(
        df, x=x, y=y,
        color=color_col or x,
        orientation=orientation,
        color_discrete_sequence=PLOTLY_COLOR_SEQUENCE,
        text=text_col or y,
        title=title,
    )
    fig.update_layout(**plotly_dark_layout(title, showlegend=show_legend))
    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
    )
    return fig


def plotly_pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str = "",
    hole: float = 0.45,
) -> go.Figure:
    """Interactive donut / pie chart."""
    if df.empty:
        return create_empty_figure()

    fig = px.pie(
        df, names=names, values=values,
        color_discrete_sequence=PLOTLY_COLOR_SEQUENCE,
        hole=hole,
    )
    fig.update_layout(**plotly_dark_layout(title, showlegend=True))
    fig.update_traces(
        textinfo="percent+label",
        textfont_color=CHART_FONT_COLOR,
        textposition="inside",
        marker=dict(line=dict(color=CHART_PAPER_BG, width=1.5)),
    )
    return fig


def plotly_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str | list,
    title: str = "",
    markers: bool = True,
    fill: str | None = "tozeroy",
) -> go.Figure:
    """Interactive line / area chart with markers."""
    if df.empty:
        return create_empty_figure()

    fig = px.line(
        df, x=x, y=y,
        markers=markers,
        color_discrete_sequence=PLOTLY_COLOR_SEQUENCE,
        title=title,
    )
    if fill:
        fig.update_traces(fill=fill, fillcolor="rgba(0, 212, 255, 0.12)")
    fig.update_layout(**plotly_dark_layout(title, showlegend=False))
    return fig


def plotly_loss_bar(
    df: pd.DataFrame,
    x: str = "incident_type",
    y: str = "total_loss",
    title: str = "Financial Loss by Crime Vector (INR)",
) -> go.Figure:
    """Formatted financial loss bar chart with INR currency indicators."""
    if df.empty:
        return create_empty_figure()

    temp = df.copy()
    temp["formatted_loss"] = temp[y].apply(lambda v: f"₹{v:,.0f}")

    fig = px.bar(
        temp, x=x, y=y,
        color=x,
        color_discrete_sequence=PLOTLY_COLOR_SEQUENCE,
        text="formatted_loss",
        title=title,
    )
    fig.update_layout(**plotly_dark_layout(title, showlegend=False, yaxis_title="Loss (INR)"))
    fig.update_traces(textposition="outside", marker_line_width=0)
    return fig


def plotly_scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color_col: str | None = None,
    size_col: str | None = None,
    title: str = "",
) -> go.Figure:
    """Interactive scatter plot."""
    if df.empty:
        return create_empty_figure()

    fig = px.scatter(
        df, x=x, y=y,
        color=color_col,
        size=size_col,
        color_discrete_sequence=PLOTLY_COLOR_SEQUENCE,
        title=title,
    )
    fig.update_layout(**plotly_dark_layout(title, showlegend=True))
    return fig


def plotly_treemap(
    df: pd.DataFrame,
    path_cols: list,
    values_col: str,
    title: str = "",
) -> go.Figure:
    """Interactive treemap for hierarchical proportions."""
    if df.empty:
        return create_empty_figure()

    fig = px.treemap(
        df,
        path=path_cols,
        values=values_col,
        color=values_col,
        color_continuous_scale=["#1a2235", "#3b82f6", "#00d4ff"],
        title=title,
    )
    fig.update_layout(**plotly_dark_layout(title))
    return fig


# ============================================================
# 2. Matplotlib / Seaborn Static Figures (Fitted & Responsive)
# ============================================================

def mpl_bar_chart(
    labels: list,
    values: list,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    color: str | None = None,
) -> plt.Figure:
    """Static bar chart via Matplotlib sized to fit without clipping."""
    apply_dark_mpl_style()
    color = color or COLORS["accent_cyan"]

    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    bars = ax.bar(labels, values, color=color, edgecolor="none", width=0.55)
    ax.set_title(title, fontsize=11, pad=8, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    plt.xticks(rotation=22, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    return fig


def mpl_line_chart(
    x: list | np.ndarray,
    y: list | np.ndarray,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    color: str | None = None,
) -> plt.Figure:
    """Static line chart via Matplotlib."""
    apply_dark_mpl_style()
    color = color or COLORS["accent_blue"]

    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    ax.plot(x, y, color=color, linewidth=2.2, marker="o", markersize=3.5)
    ax.fill_between(x, y, alpha=0.15, color=color)
    ax.set_title(title, fontsize=11, pad=8, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    plt.xticks(rotation=20, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    return fig


def seaborn_heatmap(
    data: pd.DataFrame,
    title: str = "",
    fmt: str = ".0f",
    cmap: str = "Blues",
) -> plt.Figure:
    """Correlation / pivot heatmap using Seaborn sized to fit container."""
    apply_dark_mpl_style()

    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    sns.heatmap(
        data,
        ax=ax,
        annot=True,
        fmt=fmt,
        cmap=cmap,
        linewidths=0.5,
        linecolor=CHART_BG_COLOR,
        cbar_kws={"shrink": 0.75},
        annot_kws={"size": 9},
    )
    ax.set_title(title, fontsize=11, pad=8, fontweight="bold")
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    return fig


def seaborn_boxplot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
) -> plt.Figure:
    """Boxplot using Seaborn."""
    apply_dark_mpl_style()

    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    sns.boxplot(
        data=df, x=x, y=y,
        palette=MPL_PALETTE,
        ax=ax,
        linewidth=1.1,
    )
    ax.set_title(title, fontsize=11, pad=8, fontweight="bold")
    ax.set_xlabel(x.replace("_", " ").title(), fontsize=9)
    ax.set_ylabel(y.replace("_", " ").title(), fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    plt.xticks(rotation=20, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    return fig


def seaborn_histogram(
    series: pd.Series,
    bins: int = 12,
    title: str = "",
    xlabel: str = "",
    color: str | None = None,
) -> plt.Figure:
    """Distribution histogram using Seaborn with KDE overlay."""
    apply_dark_mpl_style()
    color = color or COLORS["accent_purple"]

    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    sns.histplot(series.dropna(), bins=bins, kde=True, color=color, ax=ax,
                 line_kws={"linewidth": 1.8})
    ax.set_title(title, fontsize=11, pad=8, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel("Frequency", fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    return fig
