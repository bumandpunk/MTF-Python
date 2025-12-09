# 🎉 欢迎使用MTF图像清晰度评估工具！

## 👋 第一次使用？从这里开始

---

## ⚡ 30秒快速开始

```bash
# 1. 安装依赖（只需一次）
pip install -r requirements.txt

# 2. 运行GUI程序
python mtf_gui.py

# 3. 选择图片，点击"开始评估"，完成！
```

---

## 📚 文档导航

根据你的需求选择：

### 🆕 我是新手
→ 阅读 **`QUICKSTART.md`** - 3分钟学会使用

### 📖 我想了解详细功能
→ 阅读 **`README.md`** - 完整使用手册

### 💻 我想打包成Windows程序
→ 阅读 **`WINDOWS_BUILD.md`** - 最简单的打包方法

### 🔧 我想深入了解打包
→ 阅读 **`BUILD_GUIDE.md`** - 所有打包方案详解

### 📊 我想了解项目全貌
→ 阅读 **`PROJECT_OVERVIEW.md`** - 项目总览

---

## 🎯 两种使用方式

### 方式1: GUI图形界面（推荐新手）

```bash
python mtf_gui.py
```

**特点：**
- ✅ 图形化操作，简单直观
- ✅ 支持拖放文件
- ✅ 实时显示进度
- ✅ 结果可视化展示

### 方式2: 命令行（推荐批量处理）

```bash
# 单张图片
python mtf_sharpness.py image.bmp

# 批量处理
python mtf_sharpness.py ./images --output results.txt
```

**特点：**
- ✅ 适合自动化脚本
- ✅ 批量处理快速
- ✅ 可集成到系统

---

## 📦 项目文件说明

```
核心程序：
  mtf_sharpness.py    - 命令行版本（MTF算法核心）
  mtf_gui.py          - GUI图形界面版本

使用文档：
  START_HERE.md       - 你正在读的文件
  QUICKSTART.md       - 快速开始（推荐先读）
  README.md           - 完整手册

打包相关：
  WINDOWS_BUILD.md    - Windows打包快速指南
  BUILD_GUIDE.md      - 详细打包教程
  build_windows.py    - 打包辅助脚本
  mtf_gui.spec        - PyInstaller配置

配置文件：
  requirements.txt    - Python依赖包
  .github/workflows/  - 自动构建配置
```

---

## 🎓 学习路径推荐

### 路径A: 快速使用者（5分钟）
```
1. 看 START_HERE.md（本文）
2. 看 QUICKSTART.md
3. 运行 python mtf_gui.py
4. 完成！
```

### 路径B: 深度用户（15分钟）
```
1. 看 START_HERE.md
2. 看 QUICKSTART.md
3. 看 README.md
4. 尝试命令行版本
5. 了解算法原理
```

### 路径C: 开发者/打包者（30分钟）
```
1. 看 START_HERE.md
2. 看 PROJECT_OVERVIEW.md
3. 看 WINDOWS_BUILD.md
4. 配置GitHub Actions
5. 生成Windows程序
```

---

## ❓ 常见问题速查

### Q: 我想评估图片清晰度
**A:** 运行 `python mtf_gui.py`，选择图片即可

### Q: 我想批量处理很多图片
**A:** 运行 `python mtf_sharpness.py ./图片文件夹 -o 结果.txt`

### Q: 我想生成Windows可执行程序
**A:** 查看 `WINDOWS_BUILD.md`，推荐使用GitHub Actions

### Q: 我在Mac上如何打包Windows程序？
**A:** 3种方法：GitHub Actions（推荐）、Docker、虚拟机
     详见 `WINDOWS_BUILD.md`

### Q: 结果中MTF50是什么意思？
**A:** 清晰度指标，值越大越清晰
     > 0.4 = 非常清晰
     0.3-0.4 = 清晰
     0.2-0.3 = 较清晰
     < 0.2 = 模糊

### Q: 算法是基于什么标准？
**A:** ISO 12233国际标准的MTF刃边法

---

## 🚀 推荐的第一次使用流程

```bash
# 步骤1: 安装
pip install -r requirements.txt

# 步骤2: 测试命令行版本（看看算法效果）
python mtf_sharpness.py ./images/new2-8.bmp

# 步骤3: 尝试GUI版本（体验界面）
python mtf_gui.py

# 步骤4: 批量处理你的图片
python mtf_sharpness.py ./你的图片文件夹 --output 结果.txt

# 完成！🎉
```

---

## 📊 查看示例命令

```bash
# 运行这个脚本看所有示例命令
./example_commands.sh

# 或直接查看
cat example_commands.sh
```

---

## 💡 小贴士

1. **使用BMP或PNG格式** - 避免JPEG压缩损失
2. **测试卡要求** - 最好使用ISO 12233标准测试卡
3. **拍摄要求** - 正面拍摄、对焦准确、光线均匀
4. **批量处理** - GUI版本有进度显示，更直观
5. **结果保存** - 可以导出为txt文件

---

## 🎯 下一步做什么？

### 如果你想立即使用
→ 运行 `python mtf_gui.py`

### 如果你想了解更多
→ 阅读 `QUICKSTART.md`

### 如果你想打包程序
→ 阅读 `WINDOWS_BUILD.md`

### 如果你想看完整功能
→ 阅读 `README.md`

---

## ✨ 核心特点

✅ **算法严谨** - 基于ISO 12233标准  
✅ **操作简单** - GUI + 命令行双模式  
✅ **跨平台** - Windows/Mac/Linux全支持  
✅ **可打包** - 生成独立.exe应用  
✅ **高性能** - 处理速度快  
✅ **文档全** - 从入门到精通  

---

## 🎉 开始你的清晰度评估之旅！

**现在就试试：**
```bash
python mtf_gui.py
```

需要帮助？查看对应的文档文件！

---

*祝使用愉快！* 🚀
