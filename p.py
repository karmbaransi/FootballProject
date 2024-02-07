#from django.shortcuts import render
from chartit import DataPool, Chart

def chartit_view(request):
    # Data for the example
    data = {'X': [1, 2, 3, 4, 5], 'Y': [2, 3, 5, 7, 11]}
    data_series = DataPool(series=[data])

    # Create a line chart using Django Chartit
    chart = Chart(
        datasource=data_series,
        series_options=[{'options': {'type': 'line', 'stacking': False}, 'terms': {'X': ['Y']}}],
        chart_options={'title': {'text': 'Django Chartit Line Chart'}}
    )

    context = {'chart': chart}
    return render(request, 'chartit_template.html', context)
#karam was here 
