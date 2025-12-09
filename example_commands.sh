#!/bin/bash
# MTF清晰度评估 - 示例命令

echo "MTF图像清晰度评估工具 - 示例命令"
echo "================================"
echo ""

# 示例1：评估单张图片
echo "示例1：评估单张图片"
echo "python mtf_sharpness.py ./images/new2-8.bmp"
echo ""

# 示例2：批量评估文件夹
echo "示例2：批量评估当前images文件夹"
echo "python mtf_sharpness.py ./images"
echo ""

# 示例3：批量评估并保存结果
echo "示例3：批量评估并保存到results.txt"
echo "python mtf_sharpness.py ./images --output results.txt"
echo ""

# 示例4：使用绝对路径
echo "示例4：使用绝对路径"
echo "python mtf_sharpness.py /Users/你的用户名/图片文件夹 --output report.txt"
echo ""

echo "================================"
echo "提示：直接复制上面的命令到终端运行即可"
