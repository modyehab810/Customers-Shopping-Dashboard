# Importing Libraries
import numpy as np
import pandas as pd
import plotly.express as px

# Dash Components
import dash
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

# Set Deafult Options
pd.options.display.float_format = "{:,.2f}".format


# ----------- Data Cleaning & Casting ----------------
# Load Data
df = pd.read_csv("customer_shopping_data.csv")

# Casting Data Type of Date
df["invoice_date"] = pd.to_datetime(df["invoice_date"], format="%d/%m/%Y")

# Add Another Column of Total Sales In Lira
df["total_price"] = df["quantity"] * df["price"]

# Drop Unnecessary Column
df.drop(columns="invoice_no", inplace=True)

# Rearange The Order Of Columns
df = df[["customer_id", "age", "gender", "invoice_date",
         "category", "shopping_mall", "payment_method",
         "quantity", "price", "total_price"]].copy()


# -------------- Start The App ------------------ #
dash.register_page(__name__)
user_colors = ["#1879F4", "#FFED8F", "#2ED381", "#EC3636", "#32E0C4", "#FBA408"]
df_c = df.copy()

drop_down_options = []
drop_down_options.extend(df["shopping_mall"].unique().tolist())

# ---------------------- App Layout -----------------
layout = html.Div([
    dbc.Row([
        html.Br(),
        html.H1("Shopping Malls", style={
            "font-size": "30px",
            "font-weight": "bold",
            "font-family": "tahoma",
            "color": "white",
            "text-align": "center",
            "margin-top": "20px",
            "margin-bottom": "20px"
        }),
    ]),

    # Drop Down Menu
    dbc.Row([
        html.Br(),
        dcc.Dropdown(
            id = "malls-menu",
            options=[

                {"label": html.Span([i], style={'color': 'violet', 'font-size': 20}), "value": i,} for i in  drop_down_options
            ],
            value = [],
            multi=True,
            searchable=True,
            placeholder= "Selct a Shopping Mall",
            clearable=True,
            style={
                "color":"white",
                "border": "0px",
                "font-family": "tahoma",
                "margin-bottom": "15px",
                "background-color": "black"
            },
        )
    ]),

    # Card
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H6("Top Mall in Sales", className="text-info"),
                    html.H3(f'', id='max-sales-mall')
                ], style={"background-color": "#000", "text-align": "center", "border":"1px solid darkblue", "border-radius": "10px"})
            ),
        ], ),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H6("Lowest Mall in Sales", className="text-info"),
                    html.H3(f'', id='min-sales-mall'),
                ], style={"background-color": "#000", "text-align": "center", "border":"1px solid darkblue", "border-radius": "10px"})
            ),
        ], ),


    ], style={"margin-bottom": "20px"}),


    # bar Chart of Genders for Each Mall
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "bar-chart-mall-gender", style={"margin-bottom": "20px", "height": "550px"})
        ], width = 12),
    ], style={"border-bottom" : "1px solid darkcyan"}),

    # scatter Plot
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "scatter-mall-category", style={"margin-top": "20px", "height": "700px"})
        ]),

    ]),
])


# ------------------------------ Callbacks ------------------------------

# bar Chart Count For Each Gender Via Malls
@callback(
    Output(component_id= "max-sales-mall", component_property="children"),
    Output(component_id= "min-sales-mall", component_property="children"),
    Input(component_id= "malls-menu", component_property="value"),
)
def build_max_min_card(option):
    if len(option) == 0:
        top_mall = df.groupby("shopping_mall")["total_price"].sum().idxmax()
        lowest_mall = df.groupby("shopping_mall")["total_price"].sum().idxmin()

    else:
        filt = df["shopping_mall"].isin(option)
        df_filttered = df[filt]
        top_mall = df_filttered.groupby("shopping_mall")["total_price"].sum().idxmax()
        lowest_mall = df_filttered.groupby("shopping_mall")["total_price"].sum().idxmin()

    # Bar Chart For Mall By Gender
    return top_mall, lowest_mall



# bar Chart Count For Each Gender Via Malls
@callback(
    Output(component_id= "bar-chart-mall-gender", component_property="figure"),
    Input(component_id= "malls-menu", component_property="value"),
)
def build_bar_mall_gender(option):
    if len(option) == 0:
        pivot_mall_gender = df.pivot_table(index = "shopping_mall",
                                           columns = df["gender"],
                                           values = "gender",
                                           aggfunc = "count")
        msg_title = "Counts of Gender per Each Mall"


    else:
        filt = df["shopping_mall"].isin(option)
        df_filttered = df[filt]
        pivot_mall_gender = df_filttered.pivot_table(index = "shopping_mall",
                                                     columns = df["gender"],
                                                     values = "gender",
                                                     aggfunc="count")
        msg_title = f"Counts of Gender per {', '.join(option)}" if len(option) <= 2 else "Counts of Gender per Each Mall"


    pivot_mall_gender = pivot_mall_gender.sort_values(by = "Female", ascending=False)

    # Bar Chart For Mall By Gender
    fig = px.bar(pivot_mall_gender,
                 template="plotly_dark",
                 barmode="group",
                 text_auto="0.3s",
                 color_discrete_sequence=user_colors,
                 labels={"value": "Counts", "shopping_mall": "Mall", "gender":"Gender"},
                 title=msg_title)

    fig.update_traces(
        textposition="inside",
        insidetextfont={
            "family": "consolas",
            "size": 12,
        }
    )

    return fig

# Scatter Plot Counts of Catgorry Per Mall
@callback(
    Output(component_id= "scatter-mall-category", component_property="figure"),
    Input(component_id= "malls-menu", component_property="value"),
)
def build_scatter_mall_category(option):
    if len(option) == 0:
        group_mall_category = df.groupby(["shopping_mall", "category"],
                                         as_index=False)["quantity"].sum()
        msg_title = "Quantity Sold Per Each Category In Each Mall"

    else:
        filt = df["shopping_mall"].isin(option)
        df_filttered = df[filt]

        group_mall_category = df_filttered.groupby(["shopping_mall", "category"],
                                                   as_index=False)["quantity"].sum()

        msg_title = f"Quantity Sold Per Each Category In  {', '.join(option)}" if len(option) <= 2 else "Quantity Sold Per Each Category In Each Mall"

    group_mall_category = group_mall_category.sort_values(by = "quantity", ascending=False)

    fig_scatter = px.bar(data_frame=group_mall_category,
                     x="shopping_mall",
                     y="quantity",
                     color="category",
                     template="plotly_dark",
                     title=msg_title,
                     labels = {"category":"Category", "shopping_mall":"Mall"}
                     )


    return fig_scatter