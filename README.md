# MyPyGames
> 每款游戏的具体说明会放在各自的文件夹中。

![Github License](https://img.shields.io/badge/Language-Python-blue?logo=cplusplus) ![GitHub License](https://img.shields.io/github/license/xjn2005/MyPyGames) 
1. [Tetris](https://github.com/xjn2005/MyPyGames/tree/main/tetris)
2. [Snake](https://github.com/xjn2005/MyPyGames/tree/main/snake)
# 运行方式
- 如果只想要自己在本地运行：`git clone https://github.com/xjn2005/MyPyGames.git`
- 如果想要分发给自己的同学或者朋友玩：
  1. `git clone https://github.com/xjn2005/MyPyGames.git`
  2. `pip install pyinstaller`
  3. 在vscode终端敲：`pyinstaller --onefile --windowed <game>.py`，其中`<game>`指相应的文件名。最终会得到一个dist目录下的exe文件，点开即可。

特别地，对于有外部加载文件的游戏，比如说[Snake](https://github.com/xjn2005/MyPyGames/tree/main/snake)，需要使用此种命令：`pyinstaller --onefile --windowed --add-data <filename;.> game.py`，`<filename>`指相应加载的文件。在[Snake](https://github.com/xjn2005/MyPyGames/tree/main/snake)中就是`"PressStart2P-Regular.ttf:."`。

