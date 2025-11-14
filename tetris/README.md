# Tetris
## 项目说明
- 这是一款画风精致的俄罗斯方块。
- 采用了经典的玩法，还包括了排行榜的功能。
## 运行展示
<img width="689" height="943" alt="屏幕截图 2025-11-14 181732" src="https://github.com/user-attachments/assets/a89bdec4-d47c-4e21-8be7-b2ac9513231b" />

## 玩法说明
根据方向键来进行俄罗斯方块的移动，变换和加速下坠。
- 上键：变换方向。
- 左右键：左右移动。
- 下键：加速下坠。
## 运行方式
- 如果只想要自己在本地运行：`git clone https://github.com/xjn2005/MyPyGames.git`
- 如果想要分发给自己的同学或者朋友玩：
  1. `git clone https://github.com/xjn2005/MyPyGames.git`
  2. `pip install pyinstaller`
  3. 在vscode终端敲：`pyinstaller --onefile --windowed tetris.py`即可。  
  最终会得到一个dist目录下的exe文件，点开即可。
