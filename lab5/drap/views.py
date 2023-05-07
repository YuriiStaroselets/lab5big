from django.conf import settings
from django.shortcuts import render
from google.cloud import bigquery
import os
import json


def chart(request):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
    client = bigquery.Client(project=settings.BIGQUERY_PROJECT_ID)
    query = f"""
            SELECT SUBSTR(ReleaseDate, -4) AS year, COUNT(*) AS count
            FROM `{settings.BIGQUERY_TABLE_ID}`
            GROUP BY year
            ORDER BY year
        """
    results = client.query(query)
    data = [(str(row[0]), int(row[1])) for row in results]
    data_json = json.dumps(data)

    return render(request, 'chart.html', {'data_json': data_json})

def search_by_year(request):
    if 'year' in request.GET:
        year = request.GET['year']
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
        client = bigquery.Client(project=settings.BIGQUERY_PROJECT_ID)
        query = f"""
            SELECT ResponseName, ReleaseDate
            FROM `{settings.BIGQUERY_TABLE_ID}`
            WHERE ReleaseDate LIKE '%{year}%'
            ORDER BY ReleaseDate DESC
        """
        results = client.query(query)
        games = [(row[0], str(row[1])) for row in results]
    else:
        games = []
    return render(request, 'search_by_year.html', {'games': games})
