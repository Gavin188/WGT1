from overtime.models import AddTime


def time_tran(data):
    data = data.split('-')
    if len(data) == 10:
        print(data)
    else:
        if len(data[1]) == 1:
            data[1] = '0' + data[1]

        if len(data[2]) == 1:
            data[2] = '0' + data[2]
        da = '{0}-{1}-{2}'.format(data[0], data[1], data[2])

    return da

