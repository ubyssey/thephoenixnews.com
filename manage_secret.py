import sys

from google.cloud import datastore

def get_secret(client, key):
    query = client.query(kind='Secrets')
    query.add_filter('key', '=', key)

    return list(query.fetch())[0]

def set_secret(client, key, value):
    secret = get_secret(client, key)
    secret[key] = value

    client.put(secret)

if __name__ == "__main__":
    key = sys.argv[1]

    client = datastore.Client()

    if len(sys.argv) > 2:
        value = sys.argv[2]
        set_secret(client, key, value)
    else:
        secret = get_secret(client, key)
        print secret['value']
