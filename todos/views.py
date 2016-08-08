from django.http import HttpResponse
from django.db import connection


def home(request):
    cursor = connection.cursor()
    cursor.execute('SELECT 1')
    row = cursor.fetchone()
    print(row)
    return HttpResponse("Hello, world! Result: %s" % row)
