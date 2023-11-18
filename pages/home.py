# Importing Libraries
import numpy as np
import pandas as pd
import plotly.express as px

# Dash Compnents
import dash
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

# Set Deafult Options
pd.options.display.float_format = "{:,.2f}".format


# ----------- Data Cleaning & Casting
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
dash.register_page(__name__, path="/")

user_colors = ["#1879F4", "#FFED8F", "#2ED381", "#EC3636", "#32E0C4", "#FBA408"]

# ---------------------- App Layout -----------------
layout = html.Div([
    dbc.Row([
        html.Br(),
        html.H1("Sales", style={
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
            id = "year-menu",
            options=[
                {
                    "label": html.Span(["All Years"], style={'color': 'tomato', 'font-size': 20}),
                    "value": "all",
                },
                {
                    "label": html.Span([2021], style={'color': '#9818D6', 'font-size': 20}),
                    "value": 2021,
                },
                {
                    "label": html.Span([2022],  style={'color': '#9818D6', 'font-size': 20}),
                    "value": 2022,
                },
                {
                    "label": html.Span([2023],  style={'color': '#9818D6', 'font-size': 20}),
                    "value": 2023,
                },
            ],
            value = "all",
            multi=False,
            searchable=False,
            style={
                "color":"white",
                "border": "0px",
                "font-family": "tahoma",
                "margin-bottom": "15px",
                "background-color": "black"

            }
        )
    ]),

    # Cards
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H3(f"{df['total_price'].sum():,.0f}", id = 'total-sales-card'),
                    html.H4("Sales", className="text-info")
                ], style={"background-color": "#000", "text-align": "center", "border":"1px solid #77ACF1", "border-radius": "10px"})
            ),
        ], ),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H3(f"{df['quantity'].sum():,.0f}", id='sold-quantity-card'),
                    html.H4("Volumes", className="text-info")
                ], style={"background-color": "#000", "text-align": "center", "border":"1px solid #77ACF1", "border-radius": "10px"})
            ),
        ], ),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H3(children=f"{df['customer_id'].nunique():,.0f}", id='total-customers-card'),
                    html.H4("Customers", className="text-info")
                ],style={"background-color": "#000", "text-align": "center", "border":"1px solid #77ACF1", "border-radius": "10px"})
            ),
        ], )

    ], style={"margin-bottom": "20px"}),


    # Line Chart of Months
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "line-chart-month", style={"margin-bottom": "20px", "height":"600px"})
        ], width = 12),
    ], style={"border-bottom" : "1px solid darkcyan"}),

    # Pie Chart & Bar Horizontal Chart
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "pie-chart-gender", style={"margin-top": "20px"})
        ]),

        dbc.Col([
            dcc.Graph(id = "barh-chart-category", style={"margin-top": "20px"})
        ]),

    ]),


    dbc.Row([
        dbc.Col([
            dcc.Graph(id="bar-chart-payment", style={"margin-top": "20px"})
        ]),

        dbc.Col([
            dcc.Graph(id=  "bar-chart-shopping-mall", style={"margin-top": "20px"})
        ]),
    ]),

])


# ------------------------------ Callbacks ------------------------------
# ========== Importnat Part That Connects Graphs With Other Components ===========

# Cards Chart
@callback(
    Output(component_id= "total-sales-card", component_property="children"),
    Output(component_id= "sold-quantity-card", component_property="children"),
    Output(component_id= "total-customers-card", component_property="children"),
    Input(component_id= "year-menu", component_property="value"),
)
def build_card(option):
    if option == "all":
        total_sales = df["total_price"].sum()

        total_sold_quantity = df["quantity"].sum()

        total_number_cutomers = df["customer_id"].nunique()

        return f"{total_sales:,.0f}", f"{total_sold_quantity:,.0f}", f"{total_number_cutomers:,.0f}"

    else:

        filt = df["invoice_date"].dt.year == option

        df_filterd = df[filt]

        total_sales = df_filterd["total_price"].sum()

        total_sold_quantity = df_filterd["quantity"].sum()

        total_number_cutomers = df_filterd["customer_id"].nunique()


        return f"{total_sales:,.0f}", f"{total_sold_quantity:,.0f}", f"{total_number_cutomers:,.0f}"


# Line Chart
@callback(
    Output(component_id= "line-chart-month", component_property="figure"),
    Input(component_id= "year-menu", component_property="value"),
)
def build_line_chart(option):
    month_as_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if option == "all":
        group_year = df.groupby(df["invoice_date"].dt.year)["total_price"].sum()
        group_year.index = ["2021", "2022", "2023"]

        fig = px.bar(group_year,
                     x = group_year.index,
                     y = group_year,
                     template="plotly_dark",
                     text_auto="0.4s",
                     color = group_year.index,
                     color_discrete_sequence=["#1879F4", "#1879F4", 'darkcyan'],
                     title=f"Total Sales Per Year (Geoupped Match Months Together in Each Year)",
                     labels={"index": f"Year", "value": "Total Price in Liras"}, )

        fig.update_layout(showlegend=False)
        fig.update_traces(
            textposition="inside",
            insidetextfont={
                "family": "consolas",
                "size": 20,
            }
        )

        return fig

    else:

        filt = df["invoice_date"].dt.year == option

        df_filterd = df[filt]
        df_filterd_group = df_filterd.groupby(df_filterd["invoice_date"].dt.month)["total_price"].sum()
        df_filterd_group.index = month_as_names[0 : len(df_filterd_group)]

        fig = px.line(df_filterd_group,
                      markers=True,
                      template= "plotly_dark",
                      title= f"Total Sales Per Month via Year {option}",
                      labels={"index": f"Months of {option}", "value": "Total Price in Liras"}, )

        fig.update_layout(showlegend=False)

        return fig



# Pie Chart & bar Horizontal chart
@callback(
    Output(component_id= "pie-chart-gender", component_property="figure"),
    Output(component_id= "barh-chart-category", component_property="figure"),
    Input(component_id= "year-menu", component_property="value"),
)
def build_pie_bar(option):
    if option == "all":
        group_gender = df.groupby(df["gender"])["total_price"].sum()
        group_category = df.groupby(df["category"])["quantity"].sum().sort_values()

        msg_title_gender =  f"Total Sales Per Gender"
        msg_title_category = f"Sold Quantity Per Category"

    else:
        filt = df["invoice_date"].dt.year == option
        df_filterd = df[filt]
        group_gender = df_filterd.groupby(df_filterd["gender"])["total_price"].sum()
        group_category = df_filterd.groupby(df_filterd["category"])["quantity"].sum().sort_values()
        msg_title_gender = f"Total Sales Per Gender via Year {option}"
        msg_title_category = f"Sold Quantity Per Category via Year {option}"


    # Pie Chart For Gender
    pie_fig = px.pie(values=group_gender, names = group_gender.index,
                    template= "plotly_dark",
                    title=msg_title_gender,
                    color_discrete_sequence= user_colors,
                    hole=0.50
                 )

    pie_fig.update_traces(
        textposition="inside",
        insidetextfont={
            "family": "consolas",
            "size": 20,
        }
    )

    # --------------------------------------

    # Bar Chart For Category
    bar_fig = px.bar(group_category,
                    template="plotly_dark",
                    title=msg_title_category,
                    orientation="h",
                    text_auto="0.3s",
                    color_discrete_sequence=user_colors,
                    labels={"category": "Category", "value":"Quantity Sold"}
                     )

    bar_fig.update_traces(
        textposition="inside",
        insidetextfont={
            "family": "consolas",
            "size": 15,
        }
    )

    bar_fig.update_layout(showlegend=False)

    return pie_fig, bar_fig



# Bar Chart
@callback(
    Output(component_id= "bar-chart-payment", component_property="figure"),
    Output(component_id= "bar-chart-shopping-mall", component_property="figure"),
    Input(component_id= "year-menu", component_property="value"),
)
def build_pie_bar(option):
    if option == "all":
        payment_methods = df["payment_method"].value_counts()
        shopping_malls = df.groupby("shopping_mall")["total_price"].sum().sort_values(ascending=False)
        msg_title_payment = f"Popularity of Each Payment Methods"
        msg_title_shopping_mall = f"Total Sales For Each Shopping Malls"

    else:
        filt = df["invoice_date"].dt.year == option
        df_filterd = df[filt]
        payment_methods = df_filterd["payment_method"].value_counts()
        shopping_malls = df_filterd.groupby("shopping_mall")["total_price"].sum().sort_values(ascending=False)

        msg_title_payment = f"Popularity of Payment Methods via Year {option}"
        msg_title_shopping_mall = f"Total Sales For Shopping Malls In Year {option}"


    # Bar Chart For Category
    bar_fig = px.bar(payment_methods,
                     template="plotly_dark",
                     title=msg_title_payment,
                     text_auto="0.4s",
                     color=payment_methods.index,
                     color_discrete_sequence=user_colors,
                     labels={"payment_method": "Payment Method", "value":"Frequncey"}
                     )

    bar_fig.update_traces(
        textposition="inside",
        insidetextfont={
            "family": "consolas",
            "size": 15,
        }
    )

    bar_fig.update_layout(showlegend=False)

    # =================================
    # Bar Chart For Category
    bar_horiz_fig = px.bar(shopping_malls,
                     template="plotly_dark",
                     title=msg_title_shopping_mall,
                     text_auto="0.3s",
                     orientation="h",
                     color=shopping_malls.index,
                     color_discrete_sequence= ["#1879F4"],
                     labels={"shopping_mall": "Shopping Mall", "value": "Total Sales In Liras"},
                     )

    bar_horiz_fig.update_traces(
        textposition="inside",
        insidetextfont={
            "family": "consolas",
            "size": 15,
        },

    )

    bar_horiz_fig.update_layout(showlegend=False)




    return  bar_fig, bar_horiz_fig



