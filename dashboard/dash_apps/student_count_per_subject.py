import pandas as pd
from django_plotly_dash import DjangoDash
from dash import dcc
from dash import html
from university.repositories import Repository

app = DjangoDash('StudentCountPerSubject')

# Fetch data
data = Repository.Subjects.student_count_per_subject()
df = pd.DataFrame(list(data))
df.rename(columns={
    'id': 'subject_id',
    'name': 'subject_name'
}, inplace=True)

# Create figure
fig = {
    'data': [
        {
            'labels': df['subject_name'],
            'values': df['student_count'],
            'type': 'pie',
            'name': 'Student Count',
        }
    ],
    'layout': {
        'title': 'Student Count per Subject'
    }
}

# Layout
app.layout = html.Div([
    html.H1('Student Count per Subject'),
    dcc.Graph(id='student-count-subject', figure=fig)
])
