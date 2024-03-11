import requests
import csv

def download_and_save_to_csv(api_url, csv_filename, headers=None):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status() 
        data = response.json()

        if isinstance(data, (list, dict)):
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)

                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                    csv_writer.writerow(data[0].keys())

                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            csv_writer.writerow(item.values())
                elif isinstance(data, dict):
                    csv_writer.writerow(data.values())

            print(f'Data downloaded and saved to {csv_filename}')
        else:
            print('Unexpected data format in API response.')

    except requests.exceptions.RequestException as e:
        print(f'Error downloading data: {e}')
        print(f'Response content: {response.content}')

        print(f'Error downloading data: {e}')

api_url = 'http://127.0.0.1:8000/api/pr/'
csv_filename = 'output.csv'
download_and_save_to_csv(api_url, csv_filename)
