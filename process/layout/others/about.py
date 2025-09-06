
from dash.dependencies import Input, Output
from dash import callback_context

def about(app):
    @app.callback(
        Output("about-modal", "style"),
        [Input("about-button", "n_clicks"),
        Input("close-about", "n_clicks")],
        prevent_initial_call=True
    )
    def toggle_modal(open_clicks, close_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return {"display": "none"}
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == "about-button":
            return {
                "display": "flex",
                "position": "fixed",
                "top": "0",
                "left": "0",
                "width": "100%",
                "height": "100%",
                "backgroundColor": "rgba(0,0,0,0.4)",
                "zIndex": "1000",
                "justifyContent": "center",
                "alignItems": "center"
            }
        return {"display": "none"}