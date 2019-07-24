import csv


DATA_HEADER_QUESTION = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_data_from_file(file_name):
    with open(f"sample_data/{file_name}.csv", "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [dict(row) for row in csv_reader]


def write_data_to_file(data, file_name, data_header, append=True):

    existing_data = get_all_data_from_file(file_name)

    with open(f"sample_data/{file_name}.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_header)
        writer.writeheader()

        for row in existing_data:
            if not append:
                if data is list:
                    for data_row in data:
                        if row['id'] == data_row['id']:
                            row = data_row
                else:
                    if row['id'] == data['id']:
                        row = data

            writer.writerow(row)

            if append:
                if data is list:
                    for data_row in data:
                        writer.writerow(data_row)
                else:
                    writer.writerow(data_row)
