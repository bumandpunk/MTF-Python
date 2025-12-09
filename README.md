# MTF图像清晰度评估工具

基于ISO 12233标准的MTF（调制传递函数）刃边法实现，用于评估摄像头或光学系统的成像清晰度。

## 📖 算法原理

本工具实现了文章中描述的完整MTF刃边法（Knife-Edge Method）：

```
1. 灰度化处理 (Grayscale Conversion)
   ↓
2. 边缘区域提取 (Edge ROI Detection)
   ↓
3. ESF提取 (Edge Spread Function)
   ↓
4. LSF计算 (Line Spread Function = dESF/dx)
   ↓
5. FFT变换 (Fast Fourier Transform)
   ↓
6. MTF曲线 (Modulation Transfer Function)
   ↓
7. MTF50计算 (清晰度核心指标)
```

### 什么是MTF50？

**MTF50** 是调制传递函数下降到50%时的空间频率（单位：cycles/pixel），是国际标准ISO 12233推荐的图像清晰度评价指标。

- **值越大** = 图像越清晰
- **单位**: cycles/pixel（每像素周期数）
- **应用**: 镜头测试、摄像头质量评估、图像质量控制

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

需要的包：
- `opencv-python` - 图像处理
- `numpy` - 数值计算
- `scipy` - 科学计算（信号处理和FFT）

### 2. 基本使用

#### 评估单张图片

```bash
python mtf_sharpness.py image.bmp
```

输出示例：
```
======================================================================
MTF图像清晰度评估结果（刃边法）
======================================================================
文件名: test_image.bmp
图像尺寸: (1296, 2304)
----------------------------------------------------------------------
MTF50: 0.166074 cycles/pixel  [主要指标]
MTF30: 0.166080 cycles/pixel
MTF10: 0.166087 cycles/pixel
清晰度评分: 33.21/100
清晰度等级: 轻微模糊
======================================================================
```

#### 批量评估文件夹

```bash
python mtf_sharpness.py ./images
```

#### 批量评估并保存结果

```bash
python mtf_sharpness.py ./images --output results.txt
```

## 📊 清晰度评价标准

### MTF50数值范围

| MTF50 (cycles/pixel) | 清晰度等级 | 说明 |
|---------------------|-----------|------|
| > 0.4 | 非常清晰 ⭐⭐⭐⭐⭐ | 优秀的成像质量 |
| 0.3 - 0.4 | 清晰 ⭐⭐⭐⭐ | 良好的成像质量 |
| 0.2 - 0.3 | 较清晰 ⭐⭐⭐ | 可接受的成像质量 |
| 0.1 - 0.2 | 轻微模糊 ⭐⭐ | 成像质量较差 |
| < 0.1 | 模糊 ⭐ | 成像质量不合格 |

### 清晰度评分

程序还会给出0-100分的评分，计算公式：
```
评分 = min(100, MTF50 × 200)
```

- **80-100分**: 优秀
- **60-80分**: 良好
- **40-60分**: 一般
- **20-40分**: 较差
- **0-20分**: 不合格

## 💡 使用场景

### 1. 摄像头质量检测
使用标准测试卡（如ISO 12233刃边测试卡）拍摄图像，评估摄像头的清晰度性能。

```bash
# 测试多个摄像头拍摄的图像
python mtf_sharpness.py ./camera_test_images --output camera_report.txt
```

### 2. 镜头对比评估
对比不同镜头或不同光圈设置下的成像质量。

```bash
# 对比测试
python mtf_sharpness.py ./lens_A_images --output lens_A.txt
python mtf_sharpness.py ./lens_B_images --output lens_B.txt
```

### 3. 图像质量控制
在生产线上批量检测产品图像质量，筛选不合格样品。

```bash
# 批量质检
python mtf_sharpness.py ./production_images --output qc_report.txt
```

## 📁 项目结构

```
.
├── mtf_sharpness.py      # 主程序
├── requirements.txt      # Python依赖
├── README.md            # 使用说明（本文件）
├── images/              # 测试图片文件夹
└── results.txt          # 输出结果文件（运行后生成）
```

## 🔧 进阶用法

### 在Python代码中使用

```python
from mtf_sharpness import MTFSharpnessEvaluator

# 创建评估器
evaluator = MTFSharpnessEvaluator("test_image.bmp")

# 加载图像
evaluator.load_image()

# 计算MTF清晰度
results = evaluator.compute_mtf_sharpness()

# 获取结果
print(f"MTF50: {results['mtf50']:.6f} cycles/pixel")
print(f"清晰度评分: {results['sharpness_score']:.2f}/100")
print(f"等级: {evaluator.get_sharpness_level(results['mtf50'])}")

# 访问MTF曲线数据
frequencies = results['frequencies']
mtf_curve = results['mtf_curve']

# 可以用matplotlib绘制MTF曲线
import matplotlib.pyplot as plt
plt.plot(frequencies, mtf_curve)
plt.xlabel('Spatial Frequency (cycles/pixel)')
plt.ylabel('MTF')
plt.title('MTF Curve')
plt.grid(True)
plt.show()
```

### 批量处理示例

```python
import glob
from mtf_sharpness import MTFSharpnessEvaluator

# 获取所有图像
image_files = glob.glob("./images/*.bmp")

results = []
for img_path in image_files:
    evaluator = MTFSharpnessEvaluator(img_path)
    evaluator.load_image()
    result = evaluator.compute_mtf_sharpness()
    
    results.append({
        'filename': img_path,
        'mtf50': result['mtf50'],
        'score': result['sharpness_score']
    })

# 按MTF50排序
results.sort(key=lambda x: x['mtf50'], reverse=True)

# 输出最清晰的前5张
print("Top 5 最清晰图像:")
for i, r in enumerate(results[:5], 1):
    print(f"{i}. {r['filename']}: MTF50={r['mtf50']:.4f}")
```

## 📸 测试卡要求

为获得最佳评估效果，建议使用：

1. **标准ISO 12233测试卡**
   - 包含黑白斜边（刃边）
   - 对比度清晰的边界
   - 建议斜边角度：5-10度

2. **拍摄要求**
   - 正面拍摄，避免倾斜
   - 确保测试卡充满画面
   - 准确对焦
   - 光照均匀，避免反光

3. **图像格式**
   - 支持：PNG, JPG, JPEG, BMP, TIFF
   - 建议使用无损格式（BMP, PNG）
   - 灰度或彩色图像均可

## 🔬 技术细节

### 算法步骤详解

1. **ESF提取**: 沿边缘垂直方向投影，获得灰度变化曲线
2. **LSF计算**: 对ESF求一阶导数，并使用高斯滤波平滑
3. **FFT变换**: 对LSF进行快速傅里叶变换到频域
4. **MTF归一化**: 取复数模值并归一化，使MTF(0)=1
5. **MTF50插值**: 线性插值找到MTF=0.5时的精确频率

### 关键参数

- **亚像素插值倍数**: 4倍（提高采样密度）
- **高斯平滑sigma**: 2.0（降噪）
- **边缘检测阈值**: 95百分位数（自动适应）

## ❓ 常见问题

### Q: 为什么我的图片MTF50很低？

A: 可能的原因：
1. 图像确实模糊（对焦不准、镜头质量差）
2. 不是标准测试卡图像（算法针对清晰边缘优化）
3. 图像压缩损失（使用JPEG等有损格式）
4. 光照不均或噪声过大

### Q: 批量评估时部分图片失败怎么办？

A: 程序会自动跳过失败的图片并继续处理。检查：
1. 图片文件是否损坏
2. 图片格式是否支持
3. 图片是否过小（建议至少200x200像素）

### Q: MTF50的典型值是多少？

A: 取决于设备和场景：
- **专业相机**: 0.3-0.5 cycles/pixel
- **手机摄像头**: 0.2-0.4 cycles/pixel
- **工业相机**: 0.25-0.45 cycles/pixel
- **监控摄像头**: 0.15-0.3 cycles/pixel

### Q: 可以用于视频评估吗？

A: 可以。先提取视频帧，然后逐帧评估：
```bash
# 使用ffmpeg提取关键帧
ffmpeg -i video.mp4 -vf "select=not(mod(n\,30))" -vsync vfr frames/frame_%04d.png

# 评估所有帧
python mtf_sharpness.py ./frames --output video_sharpness.txt
```

## 📚 参考资料

- ISO 12233: Photography — Electronic still picture imaging — Resolution and spatial frequency responses
- [CSDN文章: 基于opencv的MTF算法开发](https://blog.csdn.net/zsl091125/article/details/123597827)
- [MTF测量理论与实践](https://www.imatest.com/docs/sfr/)

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

---

**提示**: 如需绘制MTF曲线图，可安装matplotlib：
```bash
pip install matplotlib
```
