import json
from io import BytesIO

import xlsxwriter


# Lab
def addTime_report(content):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name='Sheet')
    # merge_format1 = workbook.add_format({
    #     'font_size': 10,  # 字体大小
    #     'bold': True,
    #     'border': 1,
    #     'align': 'center',  # 水平居中
    #     'valign': 'vcenter',  # 垂直居中
    # })
    merge_format = workbook.add_format({
        # 'bold': True,
        # 'bg_color': 'gray',
        'font_name': '新細明體',  # 字体
        'border': 1,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
    })

    content_format = workbook.add_format({
        'font_size': 10,  # 字体大小
        'bold': False,
        'font_name': '新細明體',  # 字体
        'border': 1,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
    })

    # worksheet.set_column("B:P", 15)  # 设置列宽度
    worksheet.set_column("E:E", 10)
    # worksheet.set_column("F:F", 20)
    # worksheet.set_column("K:K", 20)

    # worksheet.set_row("E:E", 15)   #行的高

    content_format.set_text_wrap()

    worksheet.write('A1', '工號', merge_format)
    worksheet.write('B1', '姓名', merge_format)
    worksheet.write('C1', '工作日', merge_format)
    worksheet.write('D1', '申請時數', merge_format)
    worksheet.write('E1', '加班內容', merge_format)

    content = json.loads(content)
    print('***', content)
    row = 1
    col = 0
    for it in content:
        worksheet.write_string(row, col, it['username__name'], content_format)
        worksheet.write_string(row, col + 1, it['username__username'], content_format)
        worksheet.write_string(row, col + 2, it['data_time'], content_format)
        worksheet.write_string(row, col + 3, it['data_hour'], content_format)
        worksheet.write_string(row, col + 4, it['add_content'], content_format)
        row += 1

    workbook.close()
    return output
