# StellarisModExtractor
将从steam创意工坊订阅的Stellaris mod文件提取至本地mod文件夹

可能适用于其他Paradox游戏（如hoi4），未测试

## 下载

### 从发布页面下载
[发布页面](https://github.com/Lycreal/StellarisModExtractor/releases)
### 从源码构建
```Shell
git clone https://github.com/Lycreal/StellarisModExtractor.git
cd StellarisModExtractor
pyinstaller -F main.py
```
## 用法

将 run.exe 置于任何文件夹.

使用任何方式运行程序（双击,命令行,etc），不需要参数。

### 配置
1. 运行`run.exe`: 生成config.ini文件.

2. 编辑config.ini.如下:
```INI
[global]
workshop = F:\SteamLibrary\steamapps\workshop\content\281990
modpath = F:\SteamLibrary\steamapps\common\Stellaris\mod
```

3. 再次运行`run.exe`: 读取创意工坊目录.

经过以上步骤，应该得到config.ini如下:
```INI
[mod]
684509615\ui_overhaul_1080.zip = 0
810204739\folk_tinyoutliner.zip = 0

[global]
workshop = F:\SteamLibrary\steamapps\workshop\content\281990
modpath = F:\SteamLibrary\steamapps\common\Stellaris\mod
```
    
### 工作

1. 编辑 config.ini .
    ```ini
    684509615\ui_overhaul_1080.zip = 1
    ```

2. 运行`run.exe`: 提取mod文件至`modpath`.
    ```
      结果: mod
            │ ui_overhaul_1080.mod
            └─ui_overhaul_1080
                │ descriptor.mod
                ├─gfx
                ├─interface
                └─localisation
    ```

## License
[MIT LICENSE](https://github.com/Lycreal/StellarisModExtractor/blob/master/LICENSE)
