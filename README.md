# Tetris

一个使用 Python 和 Pygame 编写的现代风格俄罗斯方块。包含经典玩法、等级加速、下一方块预览、暂停和本地排行榜。

## 运行

```powershell
pip install pygame-ce
python -m tetris.tetris
```

也可以运行：

```powershell
python .\tetris\tetris.py
```

## 操作

| 按键 | 功能 |
| --- | --- |
| `←` / `→` | 左右移动 |
| `↑` | 旋转 |
| `↓` | 加速下落 |
| `Space` | 暂停或继续 |
| `R` | 游戏结束后重新开始 |
| `M` | 返回菜单或保存分数 |
| `Q` | 游戏结束后退出 |

## 结构

```text
tetris/
├── core.py       # 游戏规则
├── rank.py       # 本地排行榜
├── settings.py   # 配置与配色
├── tetris.py     # 事件与主循环
└── ui.py         # 界面绘制
```

## 测试

```powershell
python -m unittest discover -s tests -t . -v
```

## 许可证

[Apache-2.0](LICENSE)
