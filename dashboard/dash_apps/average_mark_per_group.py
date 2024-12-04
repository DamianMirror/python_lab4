import pandas as pd
from django_plotly_dash import DjangoDash
from dash import dcc
from dash import html
from university.repositories import Repository

app = DjangoDash('AverageMarkPerGroup')

# Fetch data
data = Repository.StudentGroups.average_mark_per_group()
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
            'y': df['average_mark'],
            'type': 'line',
            'name': 'Average Mark',
        }
    ],
    'layout': {
        'title': 'Average Mark per Group'
    }
}

# Layout
app.layout = html.Div([
    html.H1('Average Mark per Group'),
    dcc.Graph(id='average-mark-group', figure=fig)
])
