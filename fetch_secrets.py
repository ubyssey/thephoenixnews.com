import os

from google.cloud import datastore

def main():
    client = datastore.Client()

    query = client.query(kind='Secrets')
    query.add_filter('key', '=', 'SQL_HOST')

    secret = list(query.fetch())[0]

    os.environ['SQL_HOST'] = secret['value']

    query = client.query(kind='Secrets')
    query.add_filter('key', '=', 'SQL_PASSWORD')

    secret = list(query.fetch())[0]

    os.environ['MYSQL_PWD'] = secret['value']

if __name__ == "__main__":
    main()
