# 快速开始指南

## 1️⃣ 安装（只需一次）

```bash
pip install -r requirements.txt
```

## 2️⃣ 使用

### 测试单张图片
```bash
python mtf_sharpness.py 图片.bmp
```

### 测试整个文件夹
```bash
python mtf_sharpness.py ./images
```

### 保存结果到文件
```bash
python mtf_sharpness.py ./images --output 结果.txt
```

## 3️⃣ 看懂结果

### MTF50数值含义

| 数值 | 清晰度 |
|------|-------|
| > 0.4 | 非常清晰 ⭐⭐⭐⭐⭐ |
| 0.3-0.4 | 清晰 ⭐⭐⭐⭐ |
| 0.2-0.3 | 较清晰 ⭐⭐⭐ |
| 0.1-0.2 | 轻微模糊 ⭐⭐ |
| < 0.1 | 模糊 ⭐ |

### 示例输出
```
文件名: test.bmp
MTF50: 0.166074 cycles/pixel  ← 这个值越大越清晰
清晰度评分: 33.21/100        ← 0-100分
清晰度等级: 轻微模糊          ← 直观评级
```

## 4️⃣ 常见用法

```bash
# 当前文件夹的images目录
python mtf_sharpness.py ./images --output results.txt

# 绝对路径
python mtf_sharpness.py /Users/你的用户名/图片文件夹

# 只看一张图
python mtf_sharpness.py ./images/test.bmp
```

## ❓ 遇到问题？

查看完整文档：`README.md`
