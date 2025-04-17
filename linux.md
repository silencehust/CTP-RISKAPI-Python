### 1、安装swig、g++、make、python3-dev、boost
```bash
sudo apt install swig
sudo apt install g++
sudo apt install make
sudo apt install python3-dev
sudo apt install libboost-locale-dev
```
### 2、使用swig转换生成python接口文件
新建riskuserapi.i文件，并将CTP风控API头文件和SO文件放到同一文件夹内。

![image](https://github.com/user-attachments/assets/92aad717-79eb-47ba-8991-baf6d89aa1bd)


运行命令，生成文件riskuserapi.py、riskuserapi_wrap.cxx、riskuserapi_wrap.h
```bash
swig -threads -c++ -python riskuserapi.i
```
![image](https://github.com/user-attachments/assets/b7d9e05b-995b-43df-a8f6-289360a29f4d)

### 3、新建riskapi_make文件，修改riskuserapi.so为libriskuserapi.so
```bash
OBJS = riskuserapi_wrap.o
INCLUDE = -I./ -I/usr/include/python3.12

TARGET = _riskuserapi.so
CPPFLAGS = -shared -fPIC
CC = g++

LDLIBS = -L. -Wl,-rpath='$$ORIGIN' -lriskuserapi -lboost_locale -lboost_thread

$(TARGET): $(OBJS)
	$(CC) $(CPPFLAGS) $(INCLUDE) -o $@ $^ $(LDLIBS)

$(OBJS): %.o: %.cxx
	$(CC) -c -fPIC $(INCLUDE) $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
```
![image](https://github.com/user-attachments/assets/9cf53a97-b73b-4787-b550-7b8bcd58d052)

### 4、执行make命令，生成SO文件
```bash
make -f riskapi_make
```
![image](https://github.com/user-attachments/assets/c0b97f3b-f0d7-43e7-92d1-92cdb08e93ab)

### 5、验证
进入终端，输入以下内容后没有任何报错说明转换正常。
![image](https://github.com/user-attachments/assets/938bdcf7-022d-4827-b9a8-e3b2c6dd948a)

验证无误后，将riskuserapi.py、libriskuserapi.so、_riskuserapi.so文件拷贝至程序目录下即可使用。




