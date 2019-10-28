import json
from io import BytesIO

import xlsxwriter


# Lab
def abnormal_report(content):
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
        'font_name': '細明體',  # 字体
        'border': 1,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
    })

    content_format = workbook.add_format({
        'font_size': 10,  # 字体大小
        'bold': False,
        'font_name': '宋体',  # 字体
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
    worksheet.write('C1', '請假類別', merge_format)
    worksheet.write('D1', '開始工作日', merge_format)
    worksheet.write('E1', '結束工作日', merge_format)
    worksheet.write('F1', '請假開始日期', merge_format)
    worksheet.write('G1', '請假開始時間', merge_format)
    worksheet.write('H1', '請假結束日期', merge_format)
    worksheet.write('I1', '請假結束時間', merge_format)
    worksheet.write('J1', '是否需要代理人', merge_format)
    worksheet.write('K1', '請假原因', merge_format)

    content = json.loads(content)
    # print('content-->', content)
    row = 1
    col = 0
    for it in content:
        if it['leave_type'] == '1':
            leave_type = '事假'
        elif it['leave_type'] == '2':
            leave_type = '路程假'
        elif it['leave_type'] == '3':
            leave_type = '專案事假'
        elif it['leave_type'] == '4':
            leave_type = '年休假'
        elif it['leave_type'] == '5':
            leave_type = '產假'
        elif it['leave_type'] == '6':
            leave_type = '返鄉福利假'
        elif it['leave_type'] == '7':
            leave_type = '婚假'
        elif it['leave_type'] == '8':
            leave_type = '病假'
        elif it['leave_type'] == '9':
            leave_type = '喪假'
        elif it['leave_type'] == '10':
            leave_type = '三八婦女節假'
        else:
            leave_type = '事假'
        if it['agent_worknum'] == None:
            agent_worknum = 'N'
        else:
            agent_worknum = 'Y'
        worksheet.write_string(row, col, it['username__name'], content_format)
        worksheet.write_string(row, col + 1, it['username__username'], content_format)
        worksheet.write_string(row, col + 2, leave_type, content_format)
        worksheet.write_string(row, col + 3, it['startTime'], content_format)
        worksheet.write_string(row, col + 4, it['endTime'], content_format)
        worksheet.write_string(row, col + 5, it['leave_start_time'], content_format)
        worksheet.write_string(row, col + 6, it['leave_end_time'], content_format)
        worksheet.write_string(row, col + 7, it['time_start_period'], content_format)
        worksheet.write_string(row, col + 8, it['time_end_period'], content_format)
        worksheet.write_string(row, col + 9, agent_worknum, content_format)
        worksheet.write_string(row, col + 10, it['reason'], content_format)

        row += 1

    workbook.close()
    return output
