# 自动生成指定长度的 字符串
import random
import secrets
import string

class GenerateChinese():

    def unicode_chinese(self, num):
        chinese = ""

        for _ in range(num):
            # 获取 Unicode 编码范围内的随机数
            unicode_range = (0x4E00, 0x9FA5)

            # 根据 Unicode 编码范围生成随机汉字
            char = chr(random.randint(*unicode_range))

            # 将生成的汉字添加到结果字符串中
            chinese += char
        # 生成的字符串是不带 空格的
        return chinese
    
    def gbk_chinese(self, num):
        chinese = ""

        for _ in range(num):
            # 获取 GBK2312 编码范围内的随机数
            gbk_range_1 = (0xB0, 0xF7)
            gbk_range_2 = (0xA1, 0xFE)

            # 根据 GBK2312 编码范围生成随机汉字
            char_1 = random.randint(*gbk_range_1)
            char_2 = random.randint(*gbk_range_2)
            val = f'{char_1:x} {char_2:x}'
            # print(val)
            char = bytes.fromhex(val).decode('gb2312')

            # 将生成的汉字添加到结果字符串中
            chinese += char
        
        return chinese
    
    def ascii_string(sefl, num):
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(num))

# print(GenerateChinese().unicode_chinese(10))
# print(GenerateChinese().gbk_chinese(300))
print(GenerateChinese().ascii_string(1) + (GenerateChinese().unicode_chinese(10)))

"""
python 随机生成汉字的三种方法
1. Unicode 码
    汉字范围是 (0x4E00, 0x9FA5)
    unicode 码中收录了 2 万多个汉字，包含很多生僻字的繁体字
2. GBK2312
    GBK2312 对字符的编码采用两个字节相组合，第一个字节范围是 (0xB0, 0xF7), 第二个字节的范围是 (0xA1, 0xFE)
    GBK2312 收录了 6 千多个常用汉字
3. 列表读取
"""
"""
可以用 replace() 方法去除字符串中的 所有空格
    string = "Hello World"
    new_string = string.replace(" ", "")
    print(new_string)
"""