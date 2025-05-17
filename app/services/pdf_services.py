import pdfplumber
import re
from ..models.data_table import TableData, ExtractResponse, ExtractPdf
from ..models.file_request import FileResponse
from typing import List
from num2words import num2words
import base64
import boto3
currency_map = {
    'VND': 'đồng',
    'USD': 'đô la Mỹ',
    'EUR': 'euro',
    'JPY': 'yên Nhật',
    'GBP': 'bảng Anh',
    'AUD': 'đô la Úc',
    'CNY': 'nhân dân tệ',
    'KRW': 'won',
}

bucket_name = 'iamtest001122-save-pdf-bucket'
s3 = boto3.client('s3')
def check_valid_sum(list_data : List[TableData], total_amount : str, total_by_text : str, type_of_money : str) -> str: 
    totals = 0
    for data in list_data:
        money = data.moneyPay.replace(',', '.') if ',' in data.moneyPay else data.moneyPay.replace('.', '')
        totals += (int)(float(money))
    cast_total_amount = (int)(float(total_amount.replace(',', '.') if ',' in total_amount else total_amount.replace('.', '')))
    if totals != cast_total_amount: 
        return 'Tổng số tiền không đúng' 
    to_text_total = num2words(totals, lang='vi')
    text_total_1 = to_text_total + ' ' + currency_map[type_of_money].lower()
    text_total_2 = total_by_text.lower().split('chẳn')[0].strip().replace('.', '')
    if (text_total_1 != text_total_2): 
        return 'Tổng số tiền bằng chữ không đúng !'
    return 'success'

def read_file_pdf(fileData : str, fileName : str) -> ExtractResponse:
    if fileData == None or fileData == '': 
        return ExtractResponse (
                code=400, 
                status=False,
                message='Không tìm thấy file',
                data=None
            ) 
    data_checked = []
    list_data = []
    total_amount_by_text = ''
    total_amount_by_num = 0
    name_company = ''
    money_type = ''
    turn = ''
    file_bytes = base64.b64decode(fileData)
    
    with open(f'{fileName}', 'wb') as pdf_file: 
        pdf_file.write(file_bytes)

    with pdfplumber.open(f'{fileName}') as pdf:
        for index, page in enumerate(pdf.pages):
            text = page.extract_text()
            split_text = text.split('\n')
            get_table_data = page.extract_table()
            if (len(split_text) <= 9 or not split_text[9].strip()) and index == 0:
                return ExtractResponse(
                    code=400,
                    status=False,
                    message='PDF sai định dạng',
                    data=None
                )
            if (len(split_text) <= 10 or 'Đợt :' not in split_text[10].strip()) and index == 0:
                return ExtractResponse(
                    code=400,
                    status=False,
                    message='PDF sai định dạng',
                    data=None
                )
            if (len(split_text) <= 11 or 'Loại tiền :' not in split_text[11]) and index == 0:
                return ExtractResponse(
                    code=400,
                    status=False,
                    message='PDF sai định dạng',
                    data=None
                )
            if get_table_data == None: 
                continue
            start_index = 1 if index == 0 else 0 
            if index == 0:    
                name_company = split_text[9]
                turn = split_text[10].split('Đợt :')[1].strip()
                money_type = split_text[11].split('Loại tiền : ')[1]
                for i in split_text[6:9]: 
                    split_value = [item.strip() for item in i.split('.') if item.strip()]
                    for j in split_value[1:]:
                        if '\uf0fe' in j:
                            clean_item = re.sub(r'\s*\d+$', '', j.replace('\uf0fe', ''))
                            data_checked.append(clean_item)
            for line in split_text: 
                if 'Tổng số tiền ' in line: 
                    total_amount_by_num = line.split('Tổng số tiền ')[1]
                elif 'Số tiền bằng chữ: ' in line: 
                    total_amount_by_text = line.split('Số tiền bằng chữ: ')[1]
            for data in get_table_data[start_index:]:
                data_table = TableData(idReceive=data[1], nameBankReceive=data[2], accountNumber=data[3], nameAccount=data[4], description=data[5], moneyPay=data[6], content=data[7])
                list_data.append(data_table)
    
        validate_data = check_valid_sum(list_data, total_amount_by_num, total_amount_by_text, money_type)

        if len(data_checked) == 0:
            return ExtractResponse (
                code=400, 
                status=False,
                message='Không có mục nào được tick',
                data=None
            )
        if validate_data != 'success': 
            return ExtractResponse(
                code=400,
                status=False,
                message=validate_data,
                data=None
            )
        if name_company == '' or name_company == None: 
            return ExtractResponse(
                code=400,
                status=False,
                message='Tên công ty không tìm thấy',
                data=None
            )
        extract_pdf = ExtractPdf(name_company=name_company, checked_data=data_checked, data_table=list_data, money_type=money_type, turn=turn, total_by_num=total_amount_by_num, total_by_text=total_amount_by_text)
        try:
            s3.upload_file(fileName, bucket_name, f"pdfs/{fileName}")
            print("===> Upload thành công!")
        except Exception as e:
            print("===> Lỗi khi upload:", e)
            return ExtractResponse(
                code=400, 
                status=True,
                message='Fail khi upload file len S3, vui long thu lai',
                data=None
            )
        return ExtractResponse(
            code=200, 
            status=True, 
            message='success',
            data=extract_pdf
        )


def download_file(fileName : str): 
    object_download = f'pdfs/{fileName}'
    try: 
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_download},
            ExpiresIn=3600
        )
        return FileResponse(
            code=200,
            message='Download success',
            fileName=fileName,
            url=url,
            expires_in=3600
        )
    except Exception as e: 
        return FileResponse(
            code=400,
            message='File not found'
        )