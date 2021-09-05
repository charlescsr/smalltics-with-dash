import gradio as gr
import plotly.express as px
import pandas as pd

def get_plot(dataframe, x_axis, y_axis, plot_type):
    try:
        df = pd.read_csv(dataframe.name)

    except UnicodeDecodeError:
        return None, "Upload a CSV file"

    if plot_type == 'Scatter':
        try:
            fig = px.bar(df, x=x_axis, y=y_axis)

            fig.write_html("output.html")

            with open("output.html") as html:
                html_string = html.read()

        except Exception:
            return None, "One or both columns are not present"

        return html_string, "OK"

    elif plot_type == "Bar":
        try:
            fig = px.bar(df, x=x_axis, y=y_axis)

            fig.write_html("output.html")

            with open("output.html") as html:
                html_string = html.read()

        except Exception:
            return None, "One or both columns are not present"

        return html_string, "OK"

    elif plot_type == "Line":
        try:
            fig = px.bar(df, x=x_axis, y=y_axis)

            fig.write_html("output.html")

            with open("output.html") as html:
                html_string = html.read()

        except Exception:
            return None, "One or both columns are not present"

        return html_string, "OK"

    elif plot_type == "Sunburst":
        try:
            fig = px.bar(df, x=x_axis, y=y_axis)

            fig.write_html("output.html")

            with open("output.html") as html:
                html_string = html.read()

        except Exception:
            return None, "One or both columns are not present"

        return html_string, "OK"

iface = gr.Interface(get_plot, 
        inputs=["file", "text", "text", 
                gr.inputs.Dropdown(["Scatter", "Bar", "Line", "Sunburst"])],
        outputs=[gr.outputs.HTML(label="Plot"), 
                gr.outputs.Texbox(label="Message")])

if __name__ == "__main__":
    iface.launch()