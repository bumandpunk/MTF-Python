# 打包指南 - 在Mac上生成Windows应用程序

本指南介绍如何在Mac上将Python程序打包成Windows可执行文件（.exe）。

## 🎯 方案概览

| 方案 | 难度 | 推荐度 | 说明 |
|------|------|--------|------|
| GitHub Actions | ⭐ | ⭐⭐⭐⭐⭐ | 自动化，最简单 |
| Docker | ⭐⭐ | ⭐⭐⭐⭐ | 可靠，一次配置 |
| 虚拟机 | ⭐⭐⭐ | ⭐⭐⭐ | 传统方法 |
| 云服务器 | ⭐⭐ | ⭐⭐⭐ | 需要付费 |

---

## ✅ 方案1: GitHub Actions（推荐）

### 优点
- ✅ 完全自动化
- ✅ 免费（公开仓库）
- ✅ 同时生成Windows/Mac/Linux版本
- ✅ 不需要本地Windows环境

### 步骤

#### 1. 创建GitHub仓库

```bash
cd /Users/zfj/CodeBuddy/20251208110159

# 初始化git（如果还没有）
git init

# 添加所有文件
git add .
git commit -m "Initial commit: MTF清晰度评估工具"

# 创建GitHub仓库并推送
# 在GitHub上创建新仓库后：
git remote add origin https://github.com/你的用户名/mtf-sharpness-tool.git
git branch -M main
git push -u origin main
```

#### 2. 触发自动构建

**方法A: 推送标签（自动构建发布版）**
```bash
git tag v1.0.0
git push origin v1.0.0
```

**方法B: 手动触发**
1. 进入GitHub仓库页面
2. 点击 "Actions" 标签
3. 选择 "打包MTF应用程序"
4. 点击 "Run workflow"

#### 3. 下载构建的程序

1. 在Actions页面等待构建完成（约5-10分钟）
2. 下载生成的文件：
   - **Windows版本**: `MTF-Windows` 压缩包
   - **macOS版本**: `MTF-macOS` 压缩包

#### 4. 发布Release（可选）

如果推送了tag，会自动创建Release，可以在GitHub的Releases页面下载。

---

## ⚙️ 方案2: Docker（本地构建）

### 优点
- ✅ 在Mac上直接构建Windows程序
- ✅ 环境隔离，不污染系统
- ✅ 可重复使用

### 步骤

#### 1. 安装Docker Desktop
```bash
# 下载安装
open https://www.docker.com/products/docker-desktop

# 或使用Homebrew
brew install --cask docker
```

#### 2. 使用预配置的Docker镜像打包

```bash
cd /Users/zfj/CodeBuddy/20251208110159

# 使用专门的PyInstaller Windows构建镜像
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows \
  "pip install -r requirements.txt && \
   pyinstaller --onefile --windowed --name 'MTF清晰度评估工具' mtf_gui.py"

# 生成的exe文件在: dist/Windows/MTF清晰度评估工具.exe
```

#### 3. 测试程序（需要Windows环境）

将生成的.exe文件传到Windows电脑测试。

---

## 💻 方案3: Windows虚拟机

### 优点
- ✅ 最可靠的方法
- ✅ 可以直接测试

### 步骤

#### 1. 安装虚拟机软件

**Parallels Desktop（推荐，收费）**
```bash
# 下载: https://www.parallels.com/
# 优点：与Mac集成度高，速度快
```

**VMware Fusion（收费，但个人版免费）**
```bash
# 下载: https://www.vmware.com/products/fusion.html
```

**VirtualBox（免费）**
```bash
brew install --cask virtualbox
# 下载: https://www.virtualbox.org/
```

#### 2. 安装Windows 10/11

1. 下载Windows ISO镜像
2. 在虚拟机中安装Windows
3. 安装Python和依赖

#### 3. 在Windows虚拟机中打包

```batch
REM 在Windows命令行中执行

REM 安装依赖
pip install -r requirements.txt
pip install pyinstaller

REM 打包应用
pyinstaller --onefile --windowed --name "MTF清晰度评估工具" mtf_gui.py

REM 生成的程序在: dist\MTF清晰度评估工具.exe
```

---

## ☁️ 方案4: 云服务器

### 适用场景
- 需要频繁打包
- 不想安装虚拟机
- 需要CI/CD集成

### 步骤

#### 1. 租用Windows云服务器

**阿里云 ECS**
- 选择Windows Server系统
- 最低配置即可（1核2G）
- 按量付费，用完即删

**腾讯云 CVM**
- 同样选择Windows系统
- 新用户有优惠

#### 2. 连接服务器

使用远程桌面连接（RDP）

#### 3. 上传代码并打包

```batch
REM 在服务器上执行
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name "MTF清晰度评估工具" mtf_gui.py
```

#### 4. 下载生成的exe文件

---

## 🚀 快速测试GUI程序

在Mac上先测试GUI是否正常：

```bash
# 安装GUI依赖（tkinter通常已包含在Python中）
python mtf_gui.py
```

如果出现错误，安装tkinter：
```bash
brew install python-tk
```

---

## 📦 打包配置说明

### PyInstaller参数

```bash
pyinstaller \
  --onefile \              # 打包成单个exe文件
  --windowed \             # 不显示控制台窗口
  --name "MTF清晰度评估工具" \  # 程序名称
  --icon=icon.ico \        # 图标（可选）
  mtf_gui.py               # 入口文件
```

### 高级选项

```bash
# 添加图标
--icon=path/to/icon.ico

# 添加数据文件
--add-data "README.md:."

# 隐藏控制台（GUI程序）
--noconsole

# 排除不需要的模块（减小体积）
--exclude-module matplotlib
```

---

## 🔧 常见问题

### Q1: 打包后程序很大（>100MB）

**解决方案：**
```bash
# 使用UPX压缩
pip install pyinstaller[encryption]
pyinstaller --upx-dir=/path/to/upx mtf_gui.py

# 或排除不需要的包
pyinstaller --exclude-module matplotlib --exclude-module pandas mtf_gui.py
```

### Q2: Windows Defender报毒

**原因：** PyInstaller打包的程序有时会被误报

**解决方案：**
1. 添加代码签名证书（需要购买）
2. 向Microsoft提交误报申请
3. 使用其他打包工具（如cx_Freeze、Nuitka）

### Q3: 打包后运行报错

**常见原因：**
- 缺少依赖文件
- 路径问题

**解决方案：**
```python
# 在代码中使用相对路径
import sys
import os

# 获取正确的资源路径
if getattr(sys, 'frozen', False):
    # 打包后的路径
    application_path = sys._MEIPASS
else:
    # 开发时的路径
    application_path = os.path.dirname(os.path.abspath(__file__))
```

### Q4: tkinter界面显示异常

**解决方案：**
```bash
# 明确指定hiddenimports
pyinstaller --hidden-import PIL._tkinter_finder mtf_gui.py
```

---

## 📝 完整打包脚本

我已经创建了 `build_windows.py`，运行它获取完整说明：

```bash
python build_windows.py
```

---

## 🎨 添加图标（可选）

### 1. 准备图标文件

- 格式：`.ico`（Windows）或 `.icns`（macOS）
- 推荐大小：256x256像素

### 2. 在线转换工具

- https://convertio.co/zh/png-ico/
- https://www.icoconverter.com/

### 3. 使用图标打包

```bash
pyinstaller --icon=icon.ico --onefile --windowed mtf_gui.py
```

---

## 📊 方案对比总结

### 推荐优先级

1. **GitHub Actions** ⭐⭐⭐⭐⭐
   - 最适合：开源项目、需要分发
   - 优点：全自动、免费、支持多平台
   
2. **Docker** ⭐⭐⭐⭐
   - 最适合：本地快速打包
   - 优点：不需要Windows环境
   
3. **虚拟机** ⭐⭐⭐
   - 最适合：频繁开发测试
   - 优点：可以直接调试
   
4. **云服务器** ⭐⭐
   - 最适合：临时需求
   - 缺点：需要付费

---

## 🔗 相关资源

- [PyInstaller官方文档](https://pyinstaller.org/)
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [Docker官方文档](https://docs.docker.com/)

---

## 💡 下一步

1. **先测试GUI**: `python mtf_gui.py`
2. **选择打包方案**: 推荐GitHub Actions
3. **测试打包结果**: 在Windows上运行测试

需要帮助？查看 `build_windows.py` 获取详细说明！
