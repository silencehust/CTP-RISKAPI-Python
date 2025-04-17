# CTP_RISK_Python
CTP风控 python接口使用Swig技术开发，可以自己按以下步骤编译，需要安装swig等组件。
## Windows下封装步骤
准备
安装VisualStudio 2022、Swig、Python3、boost、cmake，boost库用到的是locale库，用来转换字符集。
boost库安装教程 ：https://blog.csdn.net/nanke_yh/article/details/124346308

#### 1、新建riskuserapi.i文件，并将FtdcRiskUserApi.h、FtdcRiskUserApiDataType.h、FtdcRiskUserApiStruct.h和riskuserapi.i放到同一文件夹下

#### 2、进入该路径，swig运行命令转换生成

```bash
swig -threads -py3 -c++ -python riskuserapi.i
```

执行完成后会生成riskuserapi.py、riskuserapi\_wrap.cxx、riskuserapi\_wrap.h三个文件

![image](https://github.com/user-attachments/assets/e48ea2cb-c9c7-4eb3-88af-6cb183fbadbc)


#### 3、VS2022创建动态链接库项目，名称为\_riskuserapi，创建完成后删除默认生成的头文件和源文件中的内容。在项目中添加如下文件

![image](https://github.com/user-attachments/assets/22bc6322-3bd0-48b3-addc-d874ec1bed07)



同时取消预编译头配置， 属性--配置属性--C/C++ --预编译头 将预编译头修改为不使用预编译头

![image](https://github.com/user-attachments/assets/2a51f9fe-b2a4-4a0a-a733-5a2238327dd1)



#### 4、添加python头文件和lib库文件以及riskuserapi.lib文件

属性--配置属性--C/C++ -- 常规 下附加包含目录添加python include文件夹。

![image](https://github.com/user-attachments/assets/2091a1d9-02c9-4671-af24-580e098ef9b0)



属性--配置属性--链接器--输入--附加依赖项添加python lib文件以及riskuserapi.lib

![image](https://github.com/user-attachments/assets/bd6fd1ca-d1c9-4840-a73b-d8286b70c11b)



#### 5、添加boost库文件以及修改多线程编译选项

属性--配置属性--C/C++ --代码生成 运行库修改为多线程(/MT)

![image](https://github.com/user-attachments/assets/ed0ac5b8-fd29-4725-b794-a9cffb0292e4)



属性--配置属性--VC++目录 包含目录和库目录添加boost库

![image](https://github.com/user-attachments/assets/ce1ecb0e-f941-49df-be22-1e080909e6a1)


#### 6、编译项目，将生成的\_riskuserapi.dll重命名为\_riskuserapi.pyd，将riskuserapi.py、riskuserapi.dll以及\_riskuserapi.pyd放到同一文件夹内即可使用。

![image](https://github.com/user-attachments/assets/4f03860d-94b7-468b-9919-4d023482e3a4)

## [Linux下封装步骤](https://github.com/silencehust/CTP-RISKAPI-Python/blob/main/linux.md)



