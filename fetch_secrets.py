# Imports the Google Cloud client library
from google.cloud import datastore


def main():
    client = datastore.Client()

    query = client.query(kind='Secret')
    query.add_filter('name', '=', 'SQL_HOST')
    print list(query.fetch())

if __name__ == "__main__":
    main()
