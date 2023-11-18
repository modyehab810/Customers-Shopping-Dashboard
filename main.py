# Dash
import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc


# -------------- Start The App ------------------ #
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])

# Nav Bar
navbar = dbc.NavbarSimple(
    dbc.Nav(
        [
            dbc.NavLink(page["name"], href=page["path"], className="btn btn-outline-info")
            for page in dash.page_registry.values()
        ],
    ),
    brand="Customers Shopping Dashboard",
    color="primary",
    dark=True,
    className="mb-2"
)

# ►►► App Layout
app.layout = dbc.Container([
    navbar,
    dash.page_container,
])

if __name__ == "__main__":
    app.run_server(debug=True)

