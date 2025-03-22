import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os

# -------------------------------------------------
# Define Color & Font Variables (Inspired by Berkeley Haas MBA website)
# -------------------------------------------------
PRIMARY_COLOR = "#003262"       # Berkeley Blue for navbar & headers
ACCENT_COLOR = "#FDB515"        # Cal Gold for key accents ("Berkeley")
INFO_COLOR = "#0072BB"          # Complementary blue for info cards (e.g., Equities)
WARNING_COLOR = "#DA291C"       # Haas Red for fixed income
SECONDARY_COLOR = "#BDC3C7"     # Silver for neutral elements (e.g., Cash)
DARK_COLOR = "#2C3E50"          # Dark grey-blue for dark cards (e.g., Real Assets)
TABLE_HEADER_COLOR = PRIMARY_COLOR
TABLE_DATA_BG = "#ffffff"       # White for table data background
FONT_FAMILY = "'Montserrat', sans-serif"  # Compelling font for headings and text

BACKGROUND_STYLE = {
    "background": "linear-gradient(to right, #d0e7f9, #ffffff)",
    "padding": "20px",
    "fontFamily": FONT_FAMILY
}

# -------------------------------------------------
# External Stylesheets: Using FLATLY Bootstrap, Animate.css, and Montserrat Google Font
# -------------------------------------------------
external_stylesheets = [
    dbc.themes.FLATLY,
    "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css",
    "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap"
]

# -------------------------------------------------
# Data: Key Metrics Extracted from Each Report
# -------------------------------------------------
data = {
    "Year": [
        "2007-2008", "2008-2009", "2009-2010", "2010-2011", "2011-2012", "2012-2013",
        "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019",
        "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"
    ],
    "Fund_Value": [1.25, 1.25, 1.50, 1.70, 1.90, 2.10, 2.20, 2.50, 2.80, 3.10, 3.40, 3.80, 3.45, 4.60, 4.54, 4.09, 4.30],
    "Return": [0.0, -3.5, 17.0, 10.0, 8.0, 12.0, 13.72, 5.0, 6.0, 4.5, 7.0, 8.0, 0.62, 40.9, -8.8, 5.93, 13.87],
    "Equities": [0, 31, 53, 55, 60, 62, 68, 70, 70, 70, 68, 65, 65, 65, 65, 73, 60],
    "Fixed_Income": [0, 0, 0, 0, 0, 0, 16, 15, 15, 15, 16, 18, 18, 18, 20, 10, 35],
    "Cash": [100, 69, 47, 45, 40, 38, 8, 10, 10, 10, 10, 10, 10, 10, 5, 5, 13],
    "Real_Assets": [0, 0, 0, 0, 0, 0, 8, 5, 5, 5, 6, 7, 7, 7, 10, 12, 5],
    "ESG_Score": [None, None, None, 50, 55, 60, 65, 68, 70, 72, 73, 75, 74, 78, 76, 77, 80]
}
df = pd.DataFrame(data)

# -------------------------------------------------
# Sort DataFrames (most recent first)
# -------------------------------------------------
df_sorted = df.sort_values(by="Year", ascending=False)
df_display = df_sorted.copy()
df_plot = df.sort_values(by="Year", ascending=False)

# -------------------------------------------------
# Insights Data: Aggregated Findings from Reports
# -------------------------------------------------
insights_data = {
    "Category": [
        "Early Years (2007-2010)",
        "Mid Years (2010-2014)",
        "Recent Years (2014-2024)",
        "Future Projections"
    ],
    "Key Insights": [
        ("The early reports detail the fund’s launch with strong philanthropic support, "
         "a high cash position to weather the financial crisis, and an early recovery with a 17% return in 2009–2010."),
        ("Between 2010–2014, the fund refined its investment processes with structured mini‑pitches, "
         "improved portfolio management, and introduced ESG metrics, setting the stage for more nuanced analysis."),
        ("From 2014 onward, the fund scaled from $2.2M to over $4M through strategic divestitures, asset diversification, "
         "and technology upgrades—maintaining robust performance even during turbulent times such as the COVID‑19 pandemic."),
        ("Future strategies include leveraging enhanced ESG analytics, expanding into alternative investments and fixed income, "
         "adopting next‑generation portfolio management platforms, and sustaining a dual focus on financial returns and social impact.")
    ]
}
df_insights = pd.DataFrame(insights_data)

# -------------------------------------------------
# Detailed Yearly Report Summaries (More Detailed)
# -------------------------------------------------
yearly_summaries = {
    "2007-2008": (
        "HSRIF Beginnings:\n"
        "- **Launch and Vision:** Introduced the Haas Socially Responsible Investment Fund with a $250K gift and major donations from alumni.\n"
        "- **Team Formation:** Assembled a diverse portfolio management team from MBA and MFE programs to gain hands-on experience in ethical investing.\n"
        "- **Focus:** Established a vision for combining social responsibility with investment management in an academic setting."
    ),
    "2008-2009": (
        "Crisis Management:\n"
        "- **Market Turbulence:** The fund navigated the global financial crisis by maintaining a high cash position (69%) to preserve capital.\n"
        "- **Conservative Strategy:** Minimal market exposure resulted in a -3.5% return, emphasizing risk aversion during uncertain times.\n"
        "- **Initial Learning:** Set the stage for future recovery by safeguarding assets."
    ),
    "2009-2010": (
        "Recovery Phase:\n"
        "- **Market Rebound:** Achieved a 17% return on the invested portion as market conditions improved.\n"
        "- **Asset Reallocation:** Increased equity exposure to 53% while reducing cash to 47%, signaling a shift toward market participation.\n"
        "- **Early Lessons:** Detailed analysis of holdings (e.g., strong performance of Cisco Systems and underperformance of Suntech Power) provided valuable insights."
    ),
    "2010-2011": (
        "Market Rebound & Process Enhancement:\n"
        "- **Growth in Value:** Fund value increased to 1.70M USD with a 10% return amid a market rebound.\n"
        "- **Process Improvements:** Introduced improved portfolio management and analytical tools, along with the first ESG score (set at 50).\n"
        "- **Balanced Approach:** Began evaluating investments on both financial and social responsibility criteria."
    ),
    "2011-2012": (
        "Transitional Growth:\n"
        "- **Stable Growth:** Fund value grew to 1.90M USD with an 8% return.\n"
        "- **Shift in Allocation:** Increased equity exposure to 60% and reduced cash to 40%, marking a gradual transition to a more balanced portfolio.\n"
        "- **ESG Integration:** ESG score updated to 55, reflecting initial steps in integrating social metrics."
    ),
    "2012-2013": (
        "Incremental Growth & ESG Integration:\n"
        "- **Improved Performance:** Fund value reached 2.10M USD with a 12% return.\n"
        "- **Research Enhancements:** Introduced systematic ESG tracking and improved research methodologies.\n"
        "- **ESG Progress:** ESG score increased to 60, indicating growing commitment to sustainability."
    ),
    "2013-2014": (
        "Milestone & Strategic Shift:\n"
        "- **Scaling Up:** Fund value increased to 2.20M USD with a 13.72% return.\n"
        "- **Technology Adoption:** Transitioned to Bloomberg’s Portfolio platform and adopted ESG benchmarks like the KLD index.\n"
        "- **Asset Mix Transformation:** Notable shift with equity exposure at 68% and a sharp drop in cash to 8%, plus the introduction of fixed income and real assets.\n"
        "- **ESG Score:** Raised to 65."
    ),
    "2014-2015": (
        "Enhanced Process & ESG Focus:\n"
        "- **Refinement:** Continued process refinements and robust ESG integration.\n"
        "- **Stable Returns:** Fund value increased to 2.50M USD with a 5% return.\n"
        "- **Asset Allocation:** Equity exposure rose to 70% while cash increased modestly to 10%; fixed income and real assets adjusted accordingly.\n"
        "- **ESG Score:** Improved to 68."
    ),
    "2015-2016": (
        "Structural Transition:\n"
        "- **Portfolio Expansion:** Fund value grew to 2.80M USD with a 6% return.\n"
        "- **Consistent Allocation:** Maintained 70% equities and 10% cash; fixed income and real assets stable.\n"
        "- **ESG Maturity:** ESG score reached 70, indicating ongoing refinement."
    ),
    "2016-2017": (
        "Strategic Projects & Detailed Analysis:\n"
        "- **Modest Growth:** Fund value increased to 3.10M USD with a 4.5% return.\n"
        "- **In-Depth Analysis:** Enhanced risk management and detailed performance analysis, with key strategic projects underway.\n"
        "- **ESG Score:** Advanced to 72."
    ),
    "2017-2018": (
        "10‑Year Retrospective:\n"
        "- **Anniversary & Impact:** Celebrated the fund’s tenth anniversary, with alumni impact and long-term performance review.\n"
        "- **Performance:** Fund value reached 3.40M USD with a 7% return; highlighted top performers (e.g., Alphabet Inc. at +35%) and underperformers (e.g., Starbucks at -6%).\n"
        "- **ESG Score:** Increased to 73."
    ),
    "2018-2019": (
        "Expanded Asset Allocation:\n"
        "- **Diversification:** Fund value grew to 3.80M USD with an 8% return.\n"
        "- **Strategic Divestitures:** Expanded asset allocation with increased fixed income (18%) and maintained cash at 10%.\n"
        "- **ESG Excellence:** ESG score rose to 75; strong performance noted from Alphabet Inc. (+40%) and moderate underperformance from PayPal (-5%)."
    ),
    "2019-2020": (
        "Volatile Markets:\n"
        "- **Challenging Conditions:** Fund value slightly decreased to 3.45M USD with a modest return of 0.62% amid market volatility.\n"
        "- **Risk Management:** Asset allocation remained steady with 65% equities; insights from early positions provided valuable lessons.\n"
        "- **ESG Score:** Recorded at 74; top performer Mastercard (+10%) versus underperformer Square (-15%)."
    ),
    "2020-2021": (
        "COVID‑19 Rebound:\n"
        "- **Strong Recovery:** Fund value rebounded to 4.60M USD with a remarkable 40.9% return during the pandemic.\n"
        "- **Portfolio Shifts:** Emphasis on equities (65%), initiation of real asset investments, and adjustments in fixed income.\n"
        "- **ESG Leadership:** ESG score increased to 78; Microsoft (+25%) emerged as a top performer while Hannon Armstrong (-10%) underperformed."
    ),
    "2021-2022": (
        "Challenging Adjustments:\n"
        "- **Turbulent Year:** Fund value slightly decreased to 4.54M USD with an -8.8% return amid shifting market conditions.\n"
        "- **Reallocation:** Increased fixed income exposure (20%) and reduced cash to 5% as part of strategic rebalancing.\n"
        "- **ESG Update:** ESG score settled at 76; strong performance from Visa (+15%) and weaker performance from American Water Works (-8%)."
    ),
    "2022-2023": (
        "Refined Management:\n"
        "- **Modest Growth:** Fund value reached 4.09M USD with a 5.93% return, emphasizing refined portfolio management.\n"
        "- **Aggressive Equity Exposure:** Increased equity to 73% while maintaining cash at 5%; adjustments across other assets for diversification.\n"
        "- **ESG Progress:** ESG score increased to 77; slight underperformance noted in the Aperio Portfolio (-5%)."
    ),
    "2023-2024": (
        "Strategic Shifts for Future Growth:\n"
        "- **Growth & Rebalancing:** Fund value rebounded to 4.30M USD with a 13.87% return.\n"
        "- **Asset Reallocation:** Equity exposure decreased to 60%, cash increased to 13%, and fixed income jumped to 35%, reflecting strategic rebalancing.\n"
        "- **ESG Maturity:** ESG score peaked at 80; Walt Disney Company (+20%) identified as a top performer, while Avalon Bay (-7%) underperformed."
    )
}

# -------------------------------------------------
# Additional Data: Major Investment Shifts
# -------------------------------------------------
data_shifts = {
    "Year": [
        "2007-2008", "2008-2009", "2009-2010", "2010-2011", "2011-2012", "2012-2013",
        "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019",
        "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"
    ],
    "Divestitures": [0, 0, 1, 1, 1, 1, 2, 2, 1, 2, 2, 3, 1, 2, 1, 1, 2],
    "New_Positions": [0, 0, 1, 2, 1, 1, 3, 2, 2, 3, 2, 3, 1, 4, 2, 1, 3],
    "Key_Shifts": [
        "Fund launched.",
        "High cash maintained during crisis.",
        "Sold Suntech; initiated recovery.",
        "Introduced new analytics.",
        "Minor divestitures during transition.",
        "Early ESG signals observed.",
        "Expanded portfolio; divested underperformers.",
        "Improved ESG integration and diversification.",
        "Balanced new positions with divestitures.",
        "Strategic projects increased divestitures.",
        "Board influence; rebalancing initiated.",
        "Significant divestitures with quality new additions.",
        "Maintained stability during volatility.",
        "Strong rebound with reallocation.",
        "Adjusted positions amid downturn.",
        "Steady shifts for sustained growth.",
        "Rebalanced for future opportunities."
    ]
}
df_shifts = pd.DataFrame(data_shifts).sort_values(by="Year", ascending=False)

# -------------------------------------------------
# Additional Data: Top-Performing & Underperforming Investments
# -------------------------------------------------
data_top_under = {
    "Year": [
        "2007-2008", "2008-2009", "2009-2010", "2010-2011", 
        "2011-2012", "2012-2013", "2013-2014", "2014-2015", 
        "2015-2016", "2016-2017", "2017-2018", "2018-2019", 
        "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"
    ],
    "Top_Performer": [
        "N/A",  
        "Cisco Systems (CSCO) +19.26%",
        "Cisco Systems (CSCO) +19.26%",
        "Cisco Systems (CSCO) +22%",
        "Microsoft (MSFT) +18%",
        "Apple Inc. (AAPL) +20%",
        "Alphabet Inc. (GOOGL) +25%",
        "Microsoft (MSFT) +30%",
        "Mastercard Inc. (MA) +28%",
        "Microsoft (MSFT) +32%",
        "Alphabet Inc. (GOOGL) +35%",
        "Alphabet Inc. (GOOGL) +40%",
        "Mastercard Inc. (MA) +10%",
        "Microsoft (MSFT) +25%",
        "Visa Inc. (V) +15%",
        "Alphabet Inc. (GOOGL) +18%",
        "Walt Disney Company (DIS) +20%"
    ],
    "Underperformer": [
        "N/A",
        "Suntech Power Holdings (STP) -60.83%",
        "Suntech Power Holdings (STP) -60.83%",
        "Suntech Power Holdings (STP) -65%",
        "Starbucks (SBUX) -12%",
        "Qualcomm (QCOM) -15%",
        "Mastercard (MA) -5%",
        "SolarCity (SCTY) -10%",
        "Eaton Corp (ETN) -8%",
        "Hanes Brand -7%",
        "Starbucks (SBUX) -6%",
        "PayPal (PYPL) -5%",
        "Square (SQ) -15%",
        "Hannon Armstrong -10%",
        "American Water Works (AWK) -8%",
        "Aperio Portfolio -5%",
        "Avalon Bay -7%"
    ]
}
df_top_under = pd.DataFrame(data_top_under).sort_values(by="Year", ascending=False)

# -------------------------------------------------
# Prepare DataFrames for Plotting and Display (handle missing values)
# -------------------------------------------------
df_plot.loc[df_plot["Year"] == "2007-2008", ["Return", "Equities", "Fixed_Income", "Cash", "Real_Assets", "ESG_Score"]] = None
df_display.loc[df_display["Year"] == "2007-2008", ["Return", "Equities", "Fixed_Income", "Cash", "Real_Assets", "ESG_Score"]] = "N/A"

# -------------------------------------------------
# Create Navigation Bar (Centered) with "Berkeley" in Yellow
# -------------------------------------------------
navbar = dbc.NavbarSimple(
    brand=html.Span([
        html.Span("Berkeley", className="animate__animated animate__pulse animate__infinite", style={"color": ACCENT_COLOR}),
        " Haas Sustainable Investment Fund Annual Reports Dashboard"
    ]),
    brand_href="#",
    color=PRIMARY_COLOR,
    dark=True,
    sticky="top",
    className="justify-content-center"
)

# -------------------------------------------------
# Initialize the Dash App with External Stylesheets
# -------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.title = "Haas SIF Annual Reports Dashboard"

# -------------------------------------------------
# App Layout: Multi-Tab Design with Navbar & Custom Background, Wrapped in a Loading Component
# -------------------------------------------------
app.layout = dbc.Container([
    navbar,
    html.Br(),
    dbc.Tabs([
        dbc.Tab(label="Overview", tab_id="overview"),
        dbc.Tab(label="Comparisons & Insights", tab_id="comparisons"),
        dbc.Tab(label="Key Visualizations", tab_id="additional"),
        dbc.Tab(label="Findings & Future Projections", tab_id="projections")
    ], id="tabs", active_tab="overview", className="mb-4"),
    dcc.Loading(
        id="loading-main",
        type="circle",
        children=html.Div(id="tab-content", className="animate__animated animate__fadeIn")
    )
], fluid=True, style=BACKGROUND_STYLE)

# -------------------------------------------------
# Callback: Render Tab Content Based on Active Tab
# -------------------------------------------------
@app.callback(Output("tab-content", "children"),
              Input("tabs", "active_tab"))
def render_tab_content(active_tab):
    if active_tab == "overview":
        return overview_layout()
    elif active_tab == "comparisons":
        return comparisons_layout()
    elif active_tab == "additional":
        return additional_layout()
    elif active_tab == "projections":
        return projections_layout()
    return html.P("This tab is not yet implemented.")

# -------------------------------------------------
# Layout for Overview Tab: Dropdown, Cards, Charts, and Yearly Summary
# -------------------------------------------------
def overview_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Overview", className="text-center animate__animated animate__fadeInDown", 
                        style={"fontWeight": "bold", "fontSize": "2rem"}),
                html.Label("Select Academic Year", className="fw-bold", style={"fontSize": "1.1rem"}),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': year, 'value': year} for year in df["Year"]],
                    value="2023-2024",
                    clearable=False,
                    style={"color": "#000"}
                )
            ], width=4)
        ], className="mb-4"),
        dbc.Row(id="cards-row", className="mb-4 animate__animated animate__fadeIn"),
        dbc.Row([
            dbc.Col([
                html.H3("Yearly Report Summary", className="mt-4 animate__animated animate__fadeIn", style={"fontSize": "1.2rem"}),
                dcc.Markdown(id="year-summary", style={
                    "backgroundColor": "#ffffff",
                    "padding": "15px",
                    "borderRadius": "5px",
                    "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                    "color": "black",
                    "fontSize": "1rem"
                })
            ])
        ], className="mb-4 animate__animated animate__fadeInUp"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fund-value-chart', className="animate__slow-pulse"), width=6),
            dbc.Col(dcc.Graph(id='return-chart', className="animate__slow-pulse"), width=6)
        ], className="animate__animated animate__fadeIn"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='asset-allocation-chart', className="animate__slow-pulse"), width=12)
        ], className="animate__animated animate__fadeIn"),
        dbc.Row([
            dbc.Col(
                html.Div(
                    dash_table.DataTable(
                        id='performance-table',
                        columns=[{"name": col, "id": col} for col in df_display.columns],
                        data=df_display.to_dict('records'),
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'center', "color": "black", "fontSize": "0.9rem"},
                        page_size=len(df_display),
                        style_header={'backgroundColor': TABLE_HEADER_COLOR, 'color': 'white', 'fontWeight': 'bold'},
                        style_data={'backgroundColor': TABLE_DATA_BG},
                        style_data_conditional=[{
                            'if': {'state': 'active'},
                            'backgroundColor': '#e1f5fe',
                            'fontWeight': 'bold',
                            'transition': 'background-color 0.3s ease'
                        }]
                    ),
                    className="animate__animated animate__fadeInUp"
                )
            )
        ], className="animate__animated animate__fadeInUp")
    ], fluid=True)

# -------------------------------------------------
# Layout for Comparisons & Insights Tab with Detailed Descriptions
# -------------------------------------------------
def comparisons_layout():
    fig_value = px.line(
        df_plot,
        x="Year",
        y="Fund_Value",
        markers=True,
        title="Fund Value Trend (in Millions USD)",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_value.update_layout(transition=dict(duration=600, easing='cubic-in-out'))
    
    fig_return = px.bar(
        df_plot,
        x="Year",
        y="Return",
        title="Annual Return (%)",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_return.update_layout(transition=dict(duration=600, easing='cubic-in-out'))
    
    description_value = dcc.Markdown(
        """
**Fund Value Trend:**  
This line chart displays the progression of the fund’s total value (in millions USD) across academic years. It highlights significant growth phases driven by strategic initiatives—such as increased equity exposure, process enhancements, and technological upgrades—while also reflecting periods of elevated cash reserves during market downturns.
        """,
        style={"fontSize": "1rem", "padding": "10px"}
    )
    
    description_return = dcc.Markdown(
        """
**Annual Return (%):**  
This bar chart presents the annual percentage returns, facilitating clear comparisons across years. It emphasizes outstanding performance periods and volatility, showcasing the impact of strategic rebalancing and market conditions on fund performance.
        """,
        style={"fontSize": "1rem", "padding": "10px"}
    )
    
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Comparisons & Insights", className="text-center animate__animated animate__fadeInDown", 
                               style={"fontWeight": "bold"}), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_value, className="animate__animated animate__fadeIn"),
                description_value
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_return, className="animate__animated animate__fadeIn"),
                description_return
            ], width=6)
        ])
    ], fluid=True)

# -------------------------------------------------
# Layout for Findings & Future Projections Tab
# -------------------------------------------------
def projections_layout():
    insights_md = """
### Key Findings & Future Projections

**Early Years (2007-2010):**  
- Launched with robust philanthropic backing and a high cash reserve during the financial crisis, yielding a 17% return in 2009–2010.  

**Mid Years (2010-2014):**  
- Investment processes were refined through structured mini‑pitches and enhanced portfolio management, with initial ESG integration (ESG Score rising from 50 to 60).  

**Recent Years (2014-2024):**  
- The fund scaled from a $2.2M asset base to over $4M through strategic divestitures, diversification, and technology enhancements, with ESG scores increasing gradually to 80.  
    
**Future Projections:**  
- **Enhanced ESG Analytics:** Leverage AI-driven tools for real-time ESG metrics to refine investment decisions.  
- **Alternative Investments & Diversification:** Expand into green bonds, renewable energy funds, and sustainable alternatives while increasing fixed income exposure.  
- **Technological Integration:** Adopt advanced portfolio management platforms and blockchain reporting to enhance transparency and predictive analytics.  
- **Sustainable Growth & Impact:** Maintain a dual focus on robust financial returns and measurable social/environmental impact.
    """
    investment_plan_md = """
### Investment Plan for 2025-2026

Building on historical successes and emerging market trends, our strategy for the 2025-2026 academic year includes:

- **Trend Analysis:** Monitor global recovery patterns, sustainability regulations, and rapid clean technology adoption.
- **Portfolio Rebalancing:** Adjust asset allocations by increasing exposure to ESG leaders and diversifying through alternative investments.
- **Data-Driven Decisions:** Leverage AI and machine learning for real-time portfolio monitoring and enhanced ESG assessment.
- **Stakeholder Engagement:** Improve transparency and collaboration with stakeholders to align strategies with evolving priorities.
- **Long-Term Impact:** Prioritize investments that deliver strong financial performance alongside significant social and environmental benefits.
    """
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Findings & Future Projections", className="text-center animate__animated animate__fadeInDown", 
                               style={"fontWeight": "bold"}), width=12)
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Markdown(insights_md, style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "5px",
                "boxShadow": "2px 2px 8px rgba(0,0,0,0.2)",
                "color": "black",
                "fontSize": "1rem"
            }), className="animate__animated animate__fadeInUp"), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(html.H2("Investment Plan for 2025-2026", className="text-center animate__animated animate__fadeInDown", 
                               style={"fontWeight": "bold"}), width=12)
        ], className="mb-2"),
        dbc.Row([
            dbc.Col(html.Div(dcc.Markdown(investment_plan_md, style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "5px",
                "boxShadow": "2px 2px 8px rgba(0,0,0,0.2)",
                "color": "black",
                "fontSize": "1rem"
            }), className="animate__animated animate__fadeInUp"), width=12)
        ], className="mb-4")
    ], fluid=True)

# -------------------------------------------------
# Layout for Key Visualizations Tab (formerly Additional Visualizations)
# -------------------------------------------------
def additional_layout():
    # ESG Score Trends Section: Create the ESG graph
    fig_esg = px.line(
        df_plot,
        x="Year",
        y="ESG_Score",
        markers=True,
        title="",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_esg.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        transition=dict(duration=600, easing='cubic-in-out'),
        xaxis_title="Academic Year",
        yaxis_title="ESG Score"
    )
    
    esg_section = dbc.Card(
        [
            dbc.CardHeader(
                html.H4(
                    "ESG Score Trends & Analysis",
                    className="text-center",
                    style={"color": PRIMARY_COLOR, "fontWeight": "bold", "fontSize": "1.5rem"}
                )
            ),
            dbc.CardBody(
                [
                    dcc.Graph(figure=fig_esg, className="animate__animated animate__slideInRight"),
                    html.P(
                        ("This graph illustrates the evolution of the fund’s ESG score over the academic years. The score, "
                         "derived from environmental, social, and governance metrics, shows a steady upward trend that reflects "
                         "the fund’s enhanced commitment to sustainable investing. This improvement is attributed to refined ESG "
                         "integration, rigorous due diligence, and strategic adjustments aimed at long-term sustainability."),
                        style={"fontSize": "1rem", "padding": "10px", "textAlign": "justify"}
                    )
                ],
                style={"backgroundColor": "#f7f7f7", "padding": "20px"}
            )
        ],
        className="mb-4 shadow-lg",
        outline=True
    )
    
    # Correlation Heatmap Section: Create the heatmap
    numeric_cols = ["Fund_Value", "Return", "Equities", "Fixed_Income", "Cash", "Real_Assets", "ESG_Score"]
    df_corr = df[numeric_cols].corr()
    heatmap_fig = px.imshow(
        df_corr,
        text_auto=True,
        aspect="auto",
        title="",
        color_continuous_scale="RdBu_r",
        template="plotly_white"
    )
    heatmap_fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        transition=dict(duration=600, easing='cubic-in-out'),
        xaxis_title="Metrics",
        yaxis_title="Metrics"
    )
    
    heatmap_section = dbc.Card(
        [
            dbc.CardHeader(
                html.H4(
                    "Correlation Heatmap & Analysis",
                    className="text-center",
                    style={"color": PRIMARY_COLOR, "fontWeight": "bold", "fontSize": "1.5rem"}
                )
            ),
            dbc.CardBody(
                [
                    dcc.Graph(figure=heatmap_fig, className="animate__animated animate__slideInLeft"),
                    html.P(
                        ("This heatmap visualizes the correlation between key financial metrics and the ESG score. Each cell indicates "
                         "the strength and direction of the correlation between two variables, with color intensity representing the magnitude. "
                         "Such insights enable stakeholders to understand how various aspects—like equity exposure, cash holdings, and fixed income—"
                         "interact and impact overall performance, guiding more informed strategic decisions."),
                        style={"fontSize": "1rem", "padding": "10px", "textAlign": "justify"}
                    )
                ],
                style={"backgroundColor": "#f7f7f7", "padding": "20px"}
            )
        ],
        className="mb-4 shadow-lg",
        outline=True
    )
    
    # Major Investment Shifts Table with hover effect
    shifts_table = html.Div(
        dash_table.DataTable(
            id='shifts-table',
            columns=[{"name": col, "id": col} for col in df_shifts.columns],
            data=df_shifts.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center', "color": "black", "fontSize": "0.9rem"},
            page_size=len(df_shifts),
            style_header={'backgroundColor': TABLE_HEADER_COLOR, 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': TABLE_DATA_BG},
            style_data_conditional=[{
                'if': {'state': 'active'},
                'backgroundColor': '#fffbcc',
                'fontWeight': 'bold',
                'transition': 'background-color 0.3s ease'
            }]
        ),
        className="animate__animated animate__flipInY"
    )
    
    # Top-Performing & Underperforming Investments Table with hover effect
    top_under_table = html.Div(
        dash_table.DataTable(
            id='top-under-table',
            columns=[{"name": col, "id": col} for col in df_top_under.columns],
            data=df_top_under.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center', "color": "black", "fontSize": "0.9rem"},
            page_size=len(df_top_under),
            style_header={'backgroundColor': TABLE_HEADER_COLOR, 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': TABLE_DATA_BG},
            style_data_conditional=[{
                'if': {'state': 'active'},
                'backgroundColor': '#fffbcc',
                'fontWeight': 'bold',
                'transition': 'background-color 0.3s ease'
            }]
        ),
        className="animate__animated animate__fadeInDown"
    )
    
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Key Visualizations", className="text-center animate__animated animate__fadeInDown", 
                               style={"fontWeight": "bold"}), width=12)
        ]),
        dbc.Row([
            dbc.Col(esg_section, width=12)
        ]),
        dbc.Row([
            dbc.Col(heatmap_section, width=12)
        ]),
        dbc.Row([
            dbc.Col(html.H3("Major Investment Shifts", className="animate__animated animate__flipInY", 
                               style={"fontWeight": "bold"}), width=12)
        ]),
        dbc.Row([
            dbc.Col(shifts_table, width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(html.H3("Top-Performing & Underperforming Investments", className="animate__animated animate__fadeInDown", 
                               style={"fontWeight": "bold"}), width=12)
        ]),
        dbc.Row([
            dbc.Col(top_under_table, width=12)
        ])
    ], fluid=True)

# -------------------------------------------------
# Callback: Update Overview Charts, Cards, and Yearly Summary Based on Selected Year
# -------------------------------------------------
@app.callback(
    [
        Output('fund-value-chart', 'figure'),
        Output('return-chart', 'figure'),
        Output('asset-allocation-chart', 'figure'),
        Output('cards-row', 'children'),
        Output('year-summary', 'children')
    ],
    Input('year-dropdown', 'value')
)
def update_overview_charts(selected_year):
    filtered = df_plot[df_plot["Year"] == selected_year]
    if filtered.empty:
        filtered = df_plot.iloc[[0]]
    sd = filtered.iloc[0]
    
    # Chart 1: Fund Value Trend with highlight.
    fig1 = px.line(
        df_plot,
        x="Year",
        y="Fund_Value",
        markers=True,
        title="Fund Value Trend (in Millions USD)",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig1.add_scatter(
        x=filtered["Year"],
        y=filtered["Fund_Value"],
        mode="markers",
        marker=dict(color="red", size=12),
        name="Selected Year"
    )
    fig1.update_layout(transition=dict(duration=600, easing='cubic-in-out'))
    
    # Chart 2: Annual Return Bar Chart with selected year highlighted in red.
    df_bar = df_plot.reset_index(drop=True).copy()
    colors = ["#FFA600"] * len(df_bar)
    sel_idx = df_bar.index[df_bar["Year"] == selected_year]
    if len(sel_idx) > 0:
        colors[sel_idx[0]] = "red"
    
    fig2 = px.bar(
        df_bar,
        x="Year",
        y="Return",
        title="Annual Return (%)",
        template="plotly_white",
        color_discrete_sequence=["#FFA600"]
    )
    fig2.update_traces(marker_color=colors)
    fig2.update_layout(transition=dict(duration=600, easing='cubic-in-out'))
    
    # Chart 3: Asset Allocation Pie Chart.
    sd_numeric = df[df["Year"] == selected_year].iloc[0]
    asset_values = {
        "Equities": sd_numeric["Equities"],
        "Fixed Income": sd_numeric["Fixed_Income"],
        "Cash": sd_numeric["Cash"],
        "Real Assets": sd_numeric["Real_Assets"]
    }
    fig3 = px.pie(
        names=list(asset_values.keys()),
        values=list(asset_values.values()),
        title=f"Asset Allocation for {selected_year}",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig3.update_layout(transition=dict(duration=600, easing='cubic-in-out'))
    
    # Cards: Key metrics for the selected year.
    sd_cards = df[df["Year"] == selected_year].iloc[0]
    cards = dbc.CardGroup([
        dbc.Card(
            [dbc.CardHeader("Fund Value (M USD)"),
             dbc.CardBody(html.H4(f"{sd_cards['Fund_Value']:.2f}", className="card-title"))],
            color=PRIMARY_COLOR,
            inverse=True
        ),
        dbc.Card(
            [dbc.CardHeader("Annual Return (%)"),
             dbc.CardBody(html.H4(f"{sd_cards['Return']:.2f}", className="card-title"))],
            color=ACCENT_COLOR,
            inverse=True
        ),
        dbc.Card(
            [dbc.CardHeader("Equities (%)"),
             dbc.CardBody(html.H4(f"{sd_cards['Equities']}%", className="card-title"))],
            color=INFO_COLOR,
            inverse=True
        ),
        dbc.Card(
            [dbc.CardHeader("Fixed Income (%)"),
             dbc.CardBody(html.H4(f"{sd_cards['Fixed_Income']}%", className="card-title"))],
            color=WARNING_COLOR,
            inverse=True
        ),
        dbc.Card(
            [dbc.CardHeader("Cash (%)"),
             dbc.CardBody(html.H4(f"{sd_cards['Cash']}%", className="card-title"))],
            color=SECONDARY_COLOR,
            inverse=True
        ),
        dbc.Card(
            [dbc.CardHeader("Real Assets (%)"),
             dbc.CardBody(html.H4(f"{sd_cards['Real_Assets']}%", className="card-title"))],
            color=DARK_COLOR,
            inverse=True
        )
    ], className="mb-4")
    
    summary_text = yearly_summaries.get(selected_year, "No summary available for this year.")
    
    return fig1, fig2, fig3, cards, summary_text

# -------------------------------------------------
# Run the App
# -------------------------------------------------
if __name__ == '__main__':
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port, debug=True)
