# dashboard/views.py
from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard.html')


from django.shortcuts import render
from bokeh.embed import components
from bokeh.layouts import gridplot
from .dash_apps.main_dashboard import create_bokeh_dashboard  # Import the updated function for dashboard creation


def bokeh_dashboard_view(request):
    # Generate Bokeh figures and layout
    layout = create_bokeh_dashboard()

    # Extract components for embedding
    script, div = components(layout)

    # Render the template with Bokeh components
    return render(request, 'bokeh_dashboard.html', {'bokeh_script': script, 'bokeh_div': div})
