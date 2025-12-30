# MyPyGames

一个使用Python开发的经典游戏集合，包含多款精心制作的休闲游戏。

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Python Versions](https://img.shields.io/badge/Python_Versions-3.x-blue?style=for-the-badge) ![Platforms](https://img.shields.io/badge/Platforms-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge) ![License](https://img.shields.io/github/license/xjn2005/MyPyGames?style=for-the-badge) ![Last Update](https://img.shields.io/github/last-commit/xjn2005/MyPyGames?style=for-the-badge) ![Status](https://img.shields.io/badge/Status-Active-green?style=for-the-badge) ![Game Count](https://img.shields.io/badge/Game_Count-2-blue?style=for-the-badge) ![Dependencies](https://img.shields.io/badge/Dependencies-pygame-yellow?style=for-the-badge)

## 🎮 游戏列表

### 1. [贪吃蛇 (Snake)](https://github.com/xjn2005/MyPyGames/tree/main/snake)
- 经典贪吃蛇游戏，包含两种游戏模式
- 🎯 **游戏模式**：经典模式、无尽障碍模式
- 🎮 **控制方式**：方向键控制蛇的移动
- 📸 **游戏截图**：
  ![Snake Select Mode](snake/select_mode.png)
  ![Snake Gameplay](snake\image.png)

### 2. [俄罗斯方块 (Tetris)](https://github.com/xjn2005/MyPyGames/tree/main/tetris)
- 画风精致的经典俄罗斯方块游戏
- 🎯 **特色功能**：经典玩法、排行榜系统
- 🎮 **控制方式**：
  - 上键：变换方块方向
  - 左右键：左右移动方块
  - 下键：加速方块下坠
- 📸 **游戏截图**：
  ![Tetris Gameplay](https://github.com/user-attachments/assets/a89bdec4-d47c-4e21-8be7-b2ac9513231b)

## 🚀 快速开始

### 环境要求
- Python 3.x
- 依赖库：`pygame`（用于游戏开发）

### 安装依赖
```bash
pip install pygame
```

### 运行方式

#### 本地运行
1. 克隆仓库：
```bash
git clone https://github.com/xjn2005/MyPyGames.git
```
2. 进入游戏目录：
```bash
cd MyPyGames/snake  # 或 cd MyPyGames/tetris
```
3. 运行游戏：
```bash
python game.py  # 贪吃蛇游戏
# 或 python tetris.py  # 俄罗斯方块游戏
```

#### 打包分发
如果你想将游戏打包成可执行文件分发给朋友：

1. 安装打包工具：
   ```bash
pip install pyinstaller
```

2. 打包普通游戏（如俄罗斯方块）：
   ```bash
pyinstaller --onefile --windowed tetris.py
```

3. 打包带有外部资源的游戏（如贪吃蛇）：
   ```bash
pyinstaller --onefile --windowed --add-data "PressStart2P-Regular.ttf;." game.py
```

4. 最终可执行文件将生成在 `dist` 目录下。

## 📁 项目结构
```
MyPyGames/
├── snake/             # 贪吃蛇游戏
│   ├── game.py        # 游戏主程序
│   ├── snake.py       # 蛇类实现
│   ├── food.py        # 食物类实现
│   ├── obstacle.py    # 障碍物类实现
│   ├── screen.py      # 屏幕管理
│   ├── settings.py    # 游戏设置
│   └── PressStart2P-Regular.ttf  # 字体文件
├── tetris/            # 俄罗斯方块游戏
│   ├── tetris.py      # 游戏主程序
│   ├── rank.py        # 排行榜功能
│   └── settings.py    # 游戏设置
├── LICENSE            # 许可证文件
└── README.md          # 项目说明
```

## 📝 贡献指南
欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证
本项目采用 Apache-2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 联系方式
如有问题或建议，欢迎通过 GitHub Issues 与我联系。

---

**享受游戏的乐趣！** 🎉