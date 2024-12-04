import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from university.repositories import Repository


def create_bokeh_dashboard():
    # Fetch and process data
    data_student_subject = convert_queryset_to_unique_dict(
        Repository.Marks.average_mark_per_student_per_subject(),
        x_field="subject__name",
        y_field="average_mark"
    )
    data_teacher = convert_queryset_to_unique_dict(
        Repository.Marks.average_mark_per_teacher(),
        x_field="teacher__user__name",
        y_field="average_mark"
    )


    # Create bar charts
    plot1 = create_bar_chart(data_student_subject, "Average Mark per Student per Subject", "Subjects", "Marks")
    plot2 = create_bar_chart(data_teacher, "Average Mark per Teacher", "Teachers", "Marks")

    # Arrange plots in a grid
    grid = gridplot([[plot1, plot2]])
    return grid


def convert_queryset_to_unique_dict(queryset, x_field, y_field):
    """
    Convert a Django QuerySet to a dictionary with unique x values for Bokeh's ColumnDataSource.
    """
    df = pd.DataFrame.from_records(queryset)
    if x_field not in df.columns or y_field not in df.columns:
        raise ValueError(f"Fields '{x_field}' or '{y_field}' not found in the QuerySet data.")

    # Ensure y_field is numeric
    df[y_field] = pd.to_numeric(df[y_field], errors='coerce')
    df = df.dropna(subset=[y_field])  # Drop rows where y_field could not be converted

    # Group by x_field and calculate the mean for y_field
    aggregated_df = df.groupby(x_field, as_index=False)[y_field].mean()

    return {
        'x': aggregated_df[x_field].astype(str).tolist(),  # Ensure x-axis values are strings
        'y': aggregated_df[y_field].tolist()
    }


def create_bar_chart(data, title, x_label, y_label):
    """
    Create a bar chart using Bokeh.
    """
    source = ColumnDataSource(data=data)
    p = figure(title=title, x_range=data['x'], sizing_mode="stretch_width", height=400)
    p.vbar(x='x', top='y', source=source, width=0.5)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.axis_label = x_label
    p.yaxis.axis_label = y_label
    return p
