import os
import datetime


def photo_data(photos: list) -> dict:
    """
    :param photos:
        data to sort
    :return:
        photo data sorted by user name
    """
    photo_data = {}
    for photo in photos:
        photo_date = datetime.datetime.strptime(str(photo.date), '%Y%m%d').strftime("%Y-%m-%d")
        if photo.username.username in photo_data:
            data = []
            count = 0
            for el in photo_data[photo.username.username]:
                if type(el) is list:
                    count += 1
            if count > 1:
                for cur_list in photo_data[photo.username.username]:
                    data.append(cur_list)
            else:
                data.append(photo_data[photo.username.username])
            data.append([os.path.basename(photo.file_name), photo.title, photo_date])
            photo_data.update({photo.username.username: data})
        else:
            photo_data.update({photo.username.username: [os.path.basename(photo.file_name), photo.title, photo_date]})
    return photo_data

