import pandas as pd
from django_plotly_dash import DjangoDash
from dash import dcc
from dash import html
from university.repositories import Repository

app = DjangoDash('StudentCountPerTeacher')

# Fetch data
data = Repository.Teachers.student_count_per_teacher()
df = pd.DataFrame(list(data))
df.rename(columns={
    'user_id': 'teacher_id',
    'user__name': 'teacher_name',
    'user__surname': 'teacher_surname'
}, inplace=True)

# Create figure
fig = {
    'data': [
        {
            'x': df['teacher_name'] + ' ' + df['teacher_surname'],
            'y': df['student_count'],
            'type': 'bar',
            'name': 'Student Count',
        }
    ],
    'layout': {
        'title': 'Student Count per Teacher'
    }
}

# Layout
app.layout = html.Div([
    html.H1('Student Count per Teacher'),
    dcc.Graph(id='student-count-teacher', figure=fig)
])
