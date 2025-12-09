# 在Mac上生成Windows应用 - 快速指南

## 🎯 最简单的方法：GitHub Actions（推荐）

### 为什么选择这个方案？
- ✅ **完全自动化** - 推送代码即可自动构建
- ✅ **免费使用** - GitHub公开仓库免费
- ✅ **多平台支持** - 同时生成Windows、Mac、Linux版本
- ✅ **无需Windows环境** - 在Mac上操作即可

---

## 📝 3步完成打包

### 第1步：上传到GitHub

```bash
# 在项目目录执行
cd /Users/zfj/CodeBuddy/20251208110159

# 初始化Git仓库（如果还没有）
git init
git add .
git commit -m "MTF清晰度评估工具"

# 在GitHub上创建新仓库后，添加远程仓库
git remote add origin https://github.com/你的用户名/mtf-tool.git
git push -u origin main
```

### 第2步：触发自动构建

**方式A：推送版本标签（推荐）**
```bash
git tag v1.0.0
git push origin v1.0.0
```

**方式B：手动触发**
1. 打开 https://github.com/你的用户名/mtf-tool
2. 点击 "Actions" 标签
3. 选择 "打包MTF应用程序" 工作流
4. 点击 "Run workflow" 按钮

### 第3步：下载程序

等待5-10分钟后：

1. 在Actions页面找到完成的构建
2. 下载Artifacts：
   - `MTF-Windows.zip` - Windows版本
   - `MTF-macOS.zip` - Mac版本
3. 解压即可使用

---

## 🖥️ 本地测试GUI程序

在打包前，先在Mac上测试：

```bash
# 运行GUI程序
python mtf_gui.py
```

### GUI功能预览
- ✅ 图形化界面，操作简单
- ✅ 支持单张图片或文件夹批量处理
- ✅ 实时显示处理进度
- ✅ 结果可视化展示
- ✅ 一键导出结果报告

---

## 🐳 备选方案：Docker打包

如果不想用GitHub，可以在Mac上直接使用Docker：

```bash
# 确保Docker已安装并运行
# 然后执行：

cd /Users/zfj/CodeBuddy/20251208110159

docker run --rm -v "$(pwd):/src/" cdrx/pyinstaller-windows \
  "pip install opencv-python-headless numpy scipy && \
   pyinstaller --onefile --windowed --name 'MTF清晰度评估工具' mtf_gui.py"

# 生成的exe在: dist/windows/MTF清晰度评估工具.exe
```

---

## 📦 已创建的文件

| 文件 | 说明 |
|------|------|
| `mtf_gui.py` | GUI应用程序主文件 |
| `build_windows.py` | 打包辅助脚本 |
| `mtf_gui.spec` | PyInstaller配置文件 |
| `.github/workflows/build.yml` | GitHub Actions自动构建配置 |
| `BUILD_GUIDE.md` | 详细打包指南 |

---

## ⚡ 快速命令参考

```bash
# 测试GUI
python mtf_gui.py

# 查看打包方案
python build_windows.py

# 使用命令行版本（无GUI）
python mtf_sharpness.py ./images --output results.txt
```

---

## 🎨 GUI界面特点

### 左侧控制面板
- 📂 选择单张图片
- 📁 选择文件夹批量处理
- ▶️ 开始评估按钮
- 💾 导出结果按钮
- 📊 进度条显示

### 右侧结果显示
- 📈 实时显示评估进度
- 📋 详细的MTF50数值
- 🏆 清晰度排名
- 📊 统计信息

---

## 🔧 故障排除

### 问题1：GitHub Actions构建失败

**解决方案：**
1. 检查 `.github/workflows/build.yml` 文件是否存在
2. 确保requirements.txt包含所有依赖
3. 查看Actions页面的错误日志

### 问题2：GUI在Mac上无法运行

**解决方案：**
```bash
# tkinter可能未安装
brew install python-tk@3.9

# 或重新安装Python
brew reinstall python@3.9
```

### 问题3：Docker命令失败

**解决方案：**
```bash
# 确保Docker Desktop正在运行
open -a Docker

# 等待Docker启动后再执行命令
```

---

## 📞 需要帮助？

1. **详细打包指南**: 查看 `BUILD_GUIDE.md`
2. **使用说明**: 查看 `README.md`
3. **快速开始**: 查看 `QUICKSTART.md`

---

## ✨ 总结

**推荐流程：**

1. ✅ 先测试：`python mtf_gui.py`
2. ✅ 上传GitHub：创建仓库并推送代码
3. ✅ 自动构建：推送tag触发Actions
4. ✅ 下载使用：获取生成的Windows程序

**时间估计：** 首次配置约15分钟，后续每次构建5-10分钟

**完全免费！** ✨
