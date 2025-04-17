# CTP_RISK_Python
CTP风控 python接口使用Swig技术开发，可以自己按以下步骤编译，需要安装swig等组件。

准备
安装VisualStudio 2022、Swig、Python3、boost、cmake，boost库用到的是locale库，用来转换字符集。
boost库安装教程 ：https://blog.csdn.net/nanke_yh/article/details/124346308

#### 1、新建riskuserapi.i文件，并将FtdcRiskUserApi.h、FtdcRiskUserApiDataType.h、FtdcRiskUserApiStruct.h和riskuserapi.i放到同一文件夹下

#### 2、进入该路径，swig运行命令转换生成

```bash
swig -threads -py3 -c++ -python riskuserapi.i
```

执行完成后会生成riskuserapi.py、riskuserapi\_wrap.cxx、riskuserapi\_wrap.h三个文件

![image](https://github.com/user-attachments/assets/3dcf683b-1ec5-4956-8b76-f6820f4466e6)

#### 3、VS2022创建动态链接库项目，名称为\_riskuserapi，创建完成后删除默认生成的头文件和源文件中的内容。在项目中添加如下文件

![image](https://github.com/user-attachments/assets/dd006dc8-15f6-4423-98c5-0bdcfe5eeb89)


同时取消预编译头配置， 属性--配置属性--C/C++ --预编译头 将预编译头修改为不使用预编译头

![image](https://github.com/user-attachments/assets/704f7245-d300-4ef6-8fe7-88237b04b513)


#### 4、添加python头文件和lib库文件以及riskuserapi.lib文件

属性--配置属性--C/C++ -- 常规 下附加包含目录添加python include文件夹。

![image](https://github.com/user-attachments/assets/0155e79b-83d4-4ff1-8b0a-cf3eb5bf9bdd)


属性--配置属性--链接器--输入--附加依赖项添加python lib文件以及riskuserapi.lib

![image](https://github.com/user-attachments/assets/5ccb102a-8afc-4820-a0eb-959e9541f021)


#### 5、添加boost库文件以及修改多线程编译选项

属性--配置属性--C/C++ --代码生成 运行库修改为多线程(/MT)

![image](https://github.com/user-attachments/assets/ed88f486-b05f-4c2b-95d5-f33bca194e68)


属性--配置属性--VC++目录 包含目录和库目录添加boost库

![image](https://github.com/user-attachments/assets/ffa76c3f-97b0-4fad-86fe-c8f5a9c917b0)


#### 6、编译项目，将生成的\_riskuserapi.dll重命名为\_riskuserapi.pyd，将riskuserapi.py、riskuserapi.dll以及\_riskuserapi.pyd放到同一文件夹内即可使用。

![image](https://github.com/user-attachments/assets/fcb9e3ea-fa21-4921-8397-f2d6dd94d9e1)




