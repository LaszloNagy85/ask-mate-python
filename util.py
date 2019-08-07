from _datetime import datetime


# def get_id(existing_data, change=1):
#
#     if len(existing_data) == 0:
#         return '1'
#
#     return str(int(existing_data[-1]['id']) + change)


# def get_epoch():
#     return str(int(time.time()))
#
#
# def convert_epoch_to_readable(time_epoch):
#     return time.strftime('%Y. %m. %d. %H:%M:%S', time.localtime(int(time_epoch)))


def get_timestamp():
    dt = datetime.now()

    return dt.strftime("%Y-%m-%d %H:%M")
