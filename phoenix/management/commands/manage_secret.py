from google.cloud import datastore

from django.core.management.base import BaseCommand

def get_secret(client, key):
    query = client.query(kind='Secrets')
    query.add_filter('key', '=', key)

    return list(query.fetch())[0]

def set_secret(client, key, value):
    secret = get_secret(client, key)
    secret[key] = value

    client.put(secret)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('key', nargs='?', type=str)
        parser.add_argument('value', nargs='?', type=str)

    def handle(self, **options):
        key = options.get('key')
        value = options.get('value')

        client = datastore.Client()

        if value is not None:
            set_secret(client, key, value)
        else:
            secret = get_secret(client, key)
            print secret['value']
