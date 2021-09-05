import gradio as gr
import plotly.express as px
import pandas as pd

def get_plot(dataframe, x_axis, y_axis, plot_type):
    try:
        df = pd.read_csv(dataframe.name)
        if any(df.columns.str.contains('^Unnamed')):
            df = pd.read_csv(dataframe.name, index_col=0)

    except UnicodeDecodeError:
        return None, "Upload a CSV file"

    if plot_type == 'Scatter':
        try:
            fig = px.scatter(df, x=x_axis, y=y_axis)

            fig.write_html("output.html")

        except Exception:
            return None, "One or both columns are not present"

        return "output.html", "OK"

    elif plot_type == "Bar":
        try:
            fig = px.bar(df, x=x_axis, y=y_axis)

            fig.write_html("output.html")

        except Exception:
            return None, "One or both columns are not present"

        return "output.html", "OK"

    elif plot_type == "Line":
        try:
            fig = px.line(df, x=x_axis, y=y_axis)

            fig.write_html("output.html")

        except Exception:
            return None, "One or both columns are not present"

        return "output.html", "OK"

    elif plot_type == "Sunburst":
        try:
            fig = px.sunburst(df, parents=x_axis, values=y_axis)

            fig.write_html("output.html")

        except Exception:
            return None, "One or both columns are not present"

        return "output.html", "OK"

iface = gr.Interface(get_plot, 
        inputs=["file", "text", "text", 
                gr.inputs.Dropdown(["Scatter", "Bar", "Line", "Sunburst"])],
        outputs=[gr.outputs.File(label="Plot"), 
                gr.outputs.Textbox(label="Message")], 
        examples=[["datasets/iris_data.csv", "sepal width", "sepal length", "Scatter"]])

if __name__ == "__main__":
    iface.launch()