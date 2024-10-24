此项目/软件的主要功能是连点器 自动脚本 以及QQ消息快速发送
因为软件与服务端有网络连接 所以为了安全性考虑 把部分网络通信部分隐藏了
此开源项目是离线版的 无与服务端的连接

另外 做一些解释:
Fuchen.py 是主程序 所有代码都在此开始
Image_pic.py 是用于释放一些固定的图片文件：默认头像 微信收款码 以及支付宝收款码 import后 会释放三个图片到temp文件夹中
Login.py 是登录窗口的UI界面
ReWord.py 是重置密码窗口的UI界面 因客户端与服务端无连接 所以该文件只被import而无具体使用
Signin.py 是注册窗口窗口的UI界面 因客户端与服务端无连接 所以该文件只被import而无具体使用
Agreement.py 是用户使用协议的窗口UI 在本开源项目中无使用
click.cpp 是连点器的C++源代码 因为Python执行效率低 所以使用C++进行调用 提升点击效率

因项目庞大 在此提及一些主要功能的函数 各位可以直接搜索定位来查找用法:
def QQ_image_update(self):  # QQ个人信息资料一键更新
def Click_Record(self):  # 记录自动脚本
def Click_Record_execute(self):  # 执行自动脚本
def download_image(self):  # 随机下载QQ头像
def QQ_Group_information(self):  #QQ群信息获取
def new_click(self):  # 开启连点器部分
def Update_weather(self,type):  #获取天气部分
此处不是所有的功能 还有很多功能 各位可以具体查看代码中的注释

我有我自己的个人网站 https://fcyang.cn/ 各位可以前往查看更多信息!
另外 在此提及一下 我只是一位在校高二学生 个人能力以及时间有限 可能软件有很多不完善的地方 请谅解

联系方式: QQ3046447554
