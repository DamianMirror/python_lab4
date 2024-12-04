import pandas as pd
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
from university.repositories import Repository

app = DjangoDash('AverageMarkPerTeacher')

# Fetch data
data = Repository.Marks.average_mark_per_teacher()
df = pd.DataFrame(list(data))
df.rename(columns={
    'teacher__user_id': 'teacher_id',
    'teacher__user__name': 'teacher_name',
    'teacher__user__surname': 'teacher_surname'
}, inplace=True)

# Unique teacher names
teacher_options = [{'label': f"{row['teacher_name']} {row['teacher_surname']}", 'value': row['teacher_id']} for idx, row in df.iterrows()]
teacher_options.insert(0, {'label': 'All Teachers', 'value': 'all'})

# Layout
app.layout = html.Div([
    html.H1('Average Mark per Teacher'),
    dcc.Dropdown(
        id='teacher-dropdown',
        options=teacher_options,
        value='all',
        placeholder="Select a teacher"
    ),
    dcc.Graph(id='average-mark-teacher-graph')
])

# Callback to update graph
@app.callback(
    Output('average-mark-teacher-graph', 'figure'),
    [Input('teacher-dropdown', 'value')]
)
def update_figure(selected_teacher):
    if selected_teacher == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['teacher_id'] == selected_teacher]
    fig = {
        'data': [
            {
                'x': filtered_df['teacher_name'] + ' ' + filtered_df['teacher_surname'],
                'y': filtered_df['average_mark'],
                'type': 'bar',
                'name': 'Average Mark',
            }
        ],
        'layout': {
            'title': 'Average Mark per Teacher'
        }
    }
    return fig
