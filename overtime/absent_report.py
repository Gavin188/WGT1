import json
from io import BytesIO

import xlsxwriter


# Lab
def absent_report(content):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name='Sheet')
    merge_format = workbook.add_format({
        # 'bold': True,
        # 'bg_color': 'gray',
        'font_name': '新細明體',  # 字体
        'border': 1,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'font_size': 12,  # 字体大小
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
    worksheet.set_column("B:B", 15)
    worksheet.set_column("C:C", 15)
    worksheet.set_column("D:D", 15)
    worksheet.set_column("E:E", 15)
    worksheet.set_column("F:F", 15)
    worksheet.set_column("G:G", 15)
    worksheet.set_column("H:H", 15)
    worksheet.set_column("I:I", 15)
    worksheet.set_column("J:J", 15)
    worksheet.set_column("K:K", 15)
    # worksheet.set_row("E:E", 15)   #行的高

    content_format.set_text_wrap()

    worksheet.write('A1', '工號', merge_format)
    worksheet.write('B1', '姓名', merge_format)
    worksheet.write('C1', '工作日', merge_format)
    worksheet.write('D1', '刷卡日期', merge_format)
    worksheet.write('E1', '刷卡時間', merge_format)
    worksheet.write('F1', '刷卡類型', merge_format)
    worksheet.write('G1', '異常原因', merge_format)
    worksheet.write('H1', '備注', merge_format)

    content = json.loads(content)
    print('***', content)
    row = 1
    col = 0
    for it in content:
        if it['card_type'] == '1':
            card_type = '第一段上班卡'
        elif it['card_type'] == '2':
            card_type = '第一段下班卡'
        elif it['card_type'] == '3':
            card_type = '第二段上班卡'
        elif it['card_type'] == '4':
            card_type = '第二段下班卡'
        elif it['card_type'] == '5':
            card_type = '补缺上班卡'
        elif it['card_type'] == '6':
            card_type = '补缺下班卡'

        if it['absent_type'] == '1':
            absent_type = '漏刷卡'
        elif it['absent_type'] == '2':
            absent_type = '办卡中'
        elif it['absent_type'] == '3':
            absent_type = '卡机异常'
        elif it['absent_type'] == '4':
            absent_type = '公务处理'
        elif it['absent_type'] == '5':
            absent_type = '刷卡地点错误'

        worksheet.write_string(row, col, it['username__name'], content_format)
        worksheet.write_string(row, col + 1, it['username__username'], content_format)
        worksheet.write_string(row, col + 2, it['startTime'], content_format)
        worksheet.write_string(row, col + 3, it['startTime'], content_format)
        worksheet.write_string(row, col + 4, it['time_end_period'], content_format)
        worksheet.write_string(row, col + 5, card_type, content_format)
        worksheet.write_string(row, col + 6, absent_type, content_format)
        worksheet.write_string(row, col + 7, it['reason'], content_format)
        row += 1

    workbook.close()
    return output
