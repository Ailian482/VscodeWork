# 枚举类
class global_var:
	#case_id
	Id = '0'
    #用例名称（描述）
	casename = '1'
    #path
	url = '2'
    #是否运行
	run = '3'
    #请求类型
	request_way = '4'
    #请求头
	header = '5'
    #case依赖
	case_depend = '6'
    #依赖的返回数据
	data_depend = '7'
    #数据依赖字段
	field_depend = '8'
    #请求数据
	data = '9'
    #预期结果
	expect = '10'
    #判断结果
	cmpresult = '11'
    #实际结果
	result ='12'


# 获取caseid
def get_id():
    return global_var.Id



 # 获取用例名称
def get_casenmae():
    return global_var.casename



# 获取url
def get_url():
    return global_var.url

#获取是否运行
def get_run():
    return global_var.run

#
def get_run_way():
    return global_var.request_way


def get_header():
    return global_var.header


def get_case_depend():
    return global_var.case_depend


def get_data_depend():
    return global_var.data_depend


def get_field_depend():
    return global_var.field_depend


def get_data():
    return global_var.data


def get_expect():
    return global_var.expect


def get_result():
    return global_var.result


# def get_cmpresult():
#     return global_var.cmpresult


def get_header_value():
    return global_var.header
