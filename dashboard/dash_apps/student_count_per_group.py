import pandas as pd
from django_plotly_dash import DjangoDash
from dash import dcc
from dash import html
from university.repositories import Repository

app = DjangoDash('StudentCountPerGroup')

# Fetch data
data = Repository.StudentGroups.student_count_per_group()
df = pd.DataFrame(list(data))
df.rename(columns={
    'id': 'group_id',
    'name': 'group_name'
}, inplace=True)

# Create figure
fig = {
    'data': [
        {
            'x': df['group_name'],
            'y': df['student_count'],
            'type': 'bar',
            'name': 'Student Count',
        }
    ],
    'layout': {
        'title': 'Student Count per Group'
    }
}

# Layout
app.layout = html.Div([
    html.H1('Student Count per Group'),
    dcc.Graph(id='student-count-group', figure=fig)
])
