import sys

from google.cloud import datastore

def main(key):
    client = datastore.Client()

    query = client.query(kind='Secrets')
    query.add_filter('key', '=', key)

    secret = list(query.fetch())[0]

    print secret['value']

if __name__ == "__main__":
    key = sys.argv[1]
    main(key)
