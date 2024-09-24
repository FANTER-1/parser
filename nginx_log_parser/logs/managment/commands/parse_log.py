import re
from datetime import datetime
from django.core.management.base import BaseCommand
from logs.models import LogEntry

class Command(BaseCommand):
    help = 'Разобрать файл журнала Nginx и сохранить данные в базе данных'

    def add_arguments(self, parser):
        parser.add_argument('log_url', type=str, help='URL of the log file')

    def handle(self, *args, **kwargs):
        log_url = kwargs['log_url']
        log_data = self.download_log(log_url)
        self.parse_log(log_data)

    def download_log(self, log_url):
        import requests
        response = requests.get(log_url)
        return response.text

    def parse_log(self, log_data):
        log_pattern = re.compile(
            r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+)'
        )
        for line in log_data.splitlines():
            match = log_pattern.match(line)
            if match:
                ip_address, date_str, request, response_code, response_size = match.groups()
                date = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S %z')
                http_method, uri, _ = request.split(' ')
                LogEntry.objects.create(
                    ip_address=ip_address,
                    date=date,
                    http_method=http_method,
                    uri=uri,
                    response_code=int(response_code),
                    response_size=int(response_size)
                )