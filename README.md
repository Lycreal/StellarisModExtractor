# StellarisModExtractor
[中文说明](https://github.com/Lycreal/StellarisModExtractor/blob/master/README_cn.md)

Extract Stellaris mod files subscribed from Steam workshop to local mod directory.

May work for other Paradox games (e.g. hoi4), but not tested.

## Download

### Download from release page
[release page](https://github.com/Lycreal/StellarisModExtractor/releases)
### Build from source
```Shell
git clone https://github.com/Lycreal/StellarisModExtractor.git
cd StellarisModExtractor
pyinstaller -F main.py
```
## Usage

Put run.exe into any clean directory.

Use commandline or double-click or whatever to open it. No parameters needed.

### Configuration
1. `run.exe`: generates config.ini file.

2. Edit config.ini . For example:
    ```INI
    [global]
    workshop = F:\SteamLibrary\steamapps\workshop\content\281990
    modpath = F:\SteamLibrary\steamapps\common\Stellaris\mod
    ```

3. `run.exe` again: load workshop.

After these steps, you should get config.ini:
```INI
[mod]
684509615\ui_overhaul_1080.zip = 0
810204739\folk_tinyoutliner.zip = 0

[global]
workshop = F:\SteamLibrary\steamapps\workshop\content\281990
modpath = F:\SteamLibrary\steamapps\common\Stellaris\mod
```
    
### Work

1. Edit config.ini .
    ```ini
    684509615\ui_overhaul_1080.zip = 1
    ```

2. `run.exe`: Extract mod file to `modpath`.
    ```
    result: mod
            │ ui_overhaul_1080.mod
            └─ui_overhaul_1080
                │ descriptor.mod
                ├─gfx
                ├─interface
                └─localisation
    ```

## License
[MIT LICENSE](https://github.com/Lycreal/StellarisModExtractor/blob/master/LICENSE)
