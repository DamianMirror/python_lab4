import pandas as pd
from django_plotly_dash import DjangoDash
import dash
from dash import html, dcc
import plotly.express as px
from university.repositories import Repository  # Використовуйте правильний шлях до репозиторію

# Отримуємо дані
data = Repository.Marks.average_mark_per_student_per_subject()
df = pd.DataFrame(list(data))
df.rename(columns={
    'student__user_id': 'student_id',
    'student__user__name': 'student_name',
    'student__user__surname': 'student_surname',
    'subject__id': 'subject_id',
    'subject__name': 'subject_name',
}, inplace=True)

# Створюємо додаток Dash
app = DjangoDash('AverageMarkPerStudentPerSubject')

# Макет додатку
app.layout = html.Div(
    children=[
        html.H1(
            'Середня оцінка студента по предмету',
            style={'textAlign': 'center', 'marginBottom': '20px'}
        ),
        dcc.Dropdown(
            id='subject-dropdown',
            options=[{'label': sub, 'value': sub} for sub in df['subject_name'].unique()],
            value=df['subject_name'].unique()[0],
            style={'marginBottom': '20px'}
        ),
        dcc.Graph(
            id='average-mark-graph',
            style={'height': '85vh', 'width': '100%'}  # Графік займає майже всю висоту блоку
        )
    ],
    style={
        'height': '100vh',  # Контейнер займає всю висоту вікна
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'space-between',
        'padding': '10px'
    }
)

# Колбеки для інтерактивності
@app.callback(
    dash.dependencies.Output('average-mark-graph', 'figure'),
    [dash.dependencies.Input('subject-dropdown', 'value')]
)
def update_graph(selected_subject):
    filtered_df = df[df['subject_name'] == selected_subject]
    fig = px.bar(
        filtered_df,
        x='student_name',
        y='average_mark',
        title=f'Середня оцінка по {selected_subject}'
    )
    fig.update_layout(
        height=700,  # Висота графіка у фігурі
        margin=dict(l=20, r=20, t=40, b=40),  # Відступи
        title={'x': 0.5},  # Центрування заголовка
        xaxis_title="Ім'я студента",
        yaxis_title="Середня оцінка"
    )
    return fig
