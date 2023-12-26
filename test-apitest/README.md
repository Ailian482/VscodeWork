# 测试平台接口自动化

为提高测试工作效率，编写自动化测试平台。

## 一、目录结构

```text
├── ApiData
├── Common                 // 公共方法
├── Config                 // 配置相关
├── Data                   // 获取数据
├── docs                   // 文档目录
├── Report                 // 报告归档存放
├── TestCase               // 测试用例
├── TestFile               // 测试数据驱动文件
└── Utils                  // 工具类
```

## 二、运行项目

运行本项目，我们建议使用python的虚拟环境，与系统自身相关依赖模块隔离。下面为开发环境搭建过程。

1.软件依赖

- 本项目`python`版本为3.6以上

2.搭建运行所需的环境

python虚拟化环境官网[virtualenv](https://pypi.org/project/virtualenv)

```bash
# 首次运行该项目，需要安装。已安装可忽略。
pip3 install virtualenv
```


3.启动python虚拟环境

```bash
virtualenv .
source bin/activate
```

4.安装项目依赖

```bash
cd test-apitest
# 安装运行环境所需依赖
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
pip install -r requirements.txt -i https://pypi.douban.com/simple
# 启动项目
python run.py
```

5.生成依赖模块

开发完成后，需要同步项目依赖模块。

```bash
pip freeze > requirements.txt
```

【注】项目依赖模块见[requirements.txt](./requirements.txt)

6.退出python虚拟环境

```bash
deactiveate
```

### 三、如何进行测试用例的开发

1.在`TestCase`目录下新增需要编写测试功能的文件夹

按格式：TestCase_{prodcut_fuction}，如`TestCase_train`。

```bash
cd test_apitest/TestCase
mkdir TestCase_train
cd TestCase_train
touch __init__.py
```

【注】可能有其他更加便利的方式，但基本上增加的基础内容如上。

2.在测试用例目录下编写相关代码

测试代码的文件名格式： test_{function}.py

例如，测试用登录后用户是否为后台管理员

```python
# 文件名：test_login.py

class TestLogin(unittest.TestCase):
    def test_getuser(self):
        '''测试登录后用户是否为后台管理员'''
        res = login().baselogin()
        self.response = res.json()
        name = self.jutil.get_values(self.response, "name")
        for i in name:
            assert i == "后台管理员"

    def test_getuser(self):
        '''测试登录后用户是否为后台管理员'''
        res = login().baselogin()
        self.response = res.json()
        name = self.jutil.get_values(self.response, "name")
        for i in name:
            assert i == "商务管理"

if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)
```

## 四、TODO

- 登录态
- 数据依赖
- 完善测试用例编写
