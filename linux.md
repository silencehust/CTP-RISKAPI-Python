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

运行命令，生成文件riskuserapi.py、riskuserapi_wrap.cxx、riskuserapi_wrap.h
```bash
swig -threads -c++ -python riskuserapi.i
```

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


### 4、执行make命令，生成SO文件
```bash
make -f riskapi_make
```

### 5、验证
进入终端，输入以下内容后没有任何报错说明转换正常。
![image](https://github.com/user-attachments/assets/7a3de99f-17e2-4246-be94-d71946e9b022)


验证无误后，将riskuserapi.py、libriskuserapi.so、_riskuserapi.so文件拷贝至程序目录下即可使用。




