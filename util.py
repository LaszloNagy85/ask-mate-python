def get_story_id(existing_data):

    if len(existing_data) == 0:
        return '1'

    return str(int(existing_data[-1]['id']) + 1)
