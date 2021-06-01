# -*- coding:utf-8 -*-
'''
@Author  :   zhangchi 
@createtime    :   2021/05/27 10:44:43
@Desc    :   None
'''
import re
import sys
import pdfplumber
sys.path.insert(0,r'D:/RPA_ENV')
import rpa_init
from core.log.rpalog import Logger
from core.config.read_root_path import read_root_path

logger = Logger.getLogger('监管函件录入_上交所警示函信息提取')
'''
@Desc        :   None
@Author      :   zhangchi 
@createtime  :   2021/06/01 14:51:59
@param1      :   None
@return      :   None
'''
def get_reason_group(pdf_text):
    #获取证券代码、证券名称、发函原因
    content = '在[\s]*[\d]{4}[\s\S]*交[\s]*易[\s]*行[\s]*为。[\s]+'
    content_handle = re.compile(content)
    content_result = content_handle.findall(pdf_text)
    content_result = ','.join(content_result).replace("\n","").replace("\r","").replace(" ","")
    content_result = content_result[1:]
    # print(content_result)
    if content_result != '':
        sedurity_name = '[“][\s\S]*[”]'
        sedurity_name_handle = re.compile(sedurity_name)
        sedurity_name_result = sedurity_name_handle.findall(content_result)
        sedurity_name_result = ','.join(sedurity_name_result).replace("\n","").replace("\r","").replace(" ","")
        sedurity_name_result = sedurity_name_result[1:]
        sedurity_name_result = sedurity_name_result[:len(sedurity_name_result) - 1]
        # print(sedurity_name_result)
        security_code = '[(][\d]{6}[)]'
        security_code_handle = re.compile(security_code)
        security_code_result = security_code_handle.findall(content_result)
        security_code_result = ','.join(security_code_result).replace("\n","").replace("\r","").replace(" ","")
        security_code_result = security_code_result[1:]
        security_code_result = security_code_result[:len(security_code_result) - 1]
        if security_code_result == '':
            security_code =  '[（][\d]{6}[）]'
            security_code_handle = re.compile(security_code)
            security_code_result = security_code_handle.findall(content_result)
            security_code_result = ','.join(security_code_result).replace("\n","").replace("\r","").replace(" ","")
            security_code_result = security_code_result[1:]
            security_code_result = security_code_result[:len(security_code_result) - 1]
        # print(security_code_result)
        reason_send_letter = '构成[\s\S]*交[\s]*易[\s]*行[\s]*为。'
        reason_send_letter_handle = re.compile(reason_send_letter)
        reason_send_letter_result = reason_send_letter_handle.findall(content_result)
        reason_send_letter_result = ','.join(reason_send_letter_result).replace("\n","").replace("\r","").replace(" ","").replace("。","")
        # print(reason_send_letter_result)
    if content_result == '':
        sedurity_name_result = ''
        security_code_result = ''
        reason_send_letter_result = ''
    
    result = sedurity_name_result + ';' + security_code_result + ';' + reason_send_letter_result + ';'
    # print(result)
    return result

'''
@Desc        :   None
@Author      :   zhangchi 
@createtime  :   2021/05/27 10:45:33
@param1      :   None
@return      :   None
'''
def get_word_group(pdf_text, file_path, pdf_page):
    #获取账户代码、账户名称、所属营业部
    customer = ''
    customer_code = ''
    business_department = ''
    result_account_infos = []
    with pdfplumber.open(file_path) as pdf:
            page=pdf.pages[int(pdf_page)]
            if page.extract_table():
                for row in page.extract_table():
                    result_account_infos.append(row)
            else:
                head = '客户操作违规 ' 
    account_code = [i[0] for i in result_account_infos]
    account_name = [i[1] for i in result_account_infos]
    department = [i[2] for i in result_account_infos]
    for i in range(len(result_account_infos)):
        if i == 0:
            continue
        customer = customer + account_name[i] + '、'
        customer_code = customer_code + account_code[i] + '、'
        business_department = business_department + department[i] + '、'
    customer = customer.replace("\n", "")
    customer = customer[:len(customer) - 1]
    customer_code = customer_code.replace("\n", "")
    customer_code = customer_code[:len(customer_code) - 1]
    business_department = business_department.replace("\n", "")
    business_department = business_department[:len(business_department) - 1]
    if customer == '' and customer_code == '' and business_department == '':
        get_word_group(pdf_text, file_path, str(int(pdf_page) - 1))
    else:
        result = customer + ';' + customer_code + ';' + business_department + ';' 
        result = result + get_reason_group(pdf_text)
        print(result)
        return(result)
if __name__ == '__main__':
    pdf_text = sys.argv[1]
    file_path = sys.argv[2]
    pdf_page = sys.argv[3]
    get_word_group(pdf_text, file_path, pdf_page)      