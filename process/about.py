
from dash import html

ABOUT_TEXT_TOP = html.P(
    "This dashboard visualizes global Input-Output trade flows (using OECD 2020 inter-country table). "
    "It allows you to explore trade relationships between countries and industries, "
    "highlighting both major and secondary trade partners."
)

ABOUT_TEXT_BULLETS = html.Ul([
    html.Li("Select an importer country from the left panel."),
    html.Li("Choose an industry to focus on."),
    html.Li("Adjust the number of top trading partners to display."),
    html.Li("Enable or disable secondary partners and trading volume thickness."),
    html.Li("Switch between Map, Pie or Risk profile Chart views."),
])

ABOUT_TEXT_BOTTOM = html.P(
    "The map shows directional trade flows, while the pie chart breaks down "
    "contributions by partner industries. "
    "Tip: Start with fewer top partners for clearer visualization, then expand to see more details."
)

ABOUT_WEIGHTED_HHI = html.P(
    "The risk profile is illustrated by The Weighted Herfindahl-Hirschman Index (HHI), which is a measure of concentration "
    "used to assess the risk associated with the diversity of input sources in the supply chain. "
    "A higher weighted HHI indicates less diversity and potentially higher risk from relying on fewer suppliers."
)

ABOUT_AUTHOR = html.P(
    "The dashboard is created by Sijin ZHANG, any comments please reach out zsjzyhzp@gmail.com. The Code can be accessed at https://github.com/jzanetti/input-output-dashboard"
)