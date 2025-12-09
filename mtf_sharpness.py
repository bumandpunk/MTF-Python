#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MTF图像清晰度评估工具 - 刃边法（Knife-Edge Method）
基于调制传递函数(Modulation Transfer Function)原理实现
严格按照ISO 12233标准的MTF测试方法
"""

import cv2
import numpy as np
import argparse
import os
import glob
from pathlib import Path
from scipy import signal, ndimage
from numpy.fft import fft, fftfreq


class MTFSharpnessEvaluator:
    """MTF清晰度评估器 - 刃边法实现"""
    
    def __init__(self, image_path):
        """
        初始化评估器
        
        Args:
            image_path: 图像文件路径
        """
        self.image_path = image_path
        self.image = None
        self.gray = None
        self.mtf_curve = None
        self.mtf50 = None
        self.frequencies = None
        
    def load_image(self):
        """加载并预处理图像"""
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"图像文件不存在: {self.image_path}")
        
        # 读取图像
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise ValueError(f"无法读取图像: {self.image_path}")
        
        # 转换为灰度图
        if len(self.image.shape) == 3:
            self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            self.gray = self.image.copy()
        
        return self.gray
    
    def detect_edges(self):
        """
        检测图像中的边缘（刃边）
        
        Returns:
            list: 检测到的边缘区域列表 [(x1, y1, x2, y2, angle), ...]
        """
        # 使用Canny边缘检测
        edges = cv2.Canny(self.gray, 50, 150, apertureSize=3)
        
        # 使用霍夫变换检测直线
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                                minLineLength=100, maxLineGap=10)
        
        edge_regions = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # 计算线段角度
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                # 只选择接近水平或垂直的边缘（斜边在3-10度范围内更好）
                if abs(angle) > 80 or abs(angle) < 10 or (abs(angle) > 170):
                    edge_regions.append((x1, y1, x2, y2, angle))
        
        return edge_regions
    
    def extract_edge_roi(self, margin=50):
        """
        提取边缘感兴趣区域（ROI）
        自动检测图像中最明显的边缘区域
        
        Args:
            margin: 边缘周围的边距
            
        Returns:
            numpy.ndarray: 边缘ROI区域
        """
        # 计算图像梯度找到最强的边缘
        grad_x = cv2.Sobel(self.gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(self.gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_mag = np.sqrt(grad_x**2 + grad_y**2)
        
        # 找到梯度最大的区域
        threshold = np.percentile(gradient_mag, 95)
        edge_mask = gradient_mag > threshold
        
        # 找到边缘区域的边界框
        coords = np.column_stack(np.where(edge_mask))
        if len(coords) == 0:
            # 如果没有找到边缘，使用整个图像
            return self.gray
        
        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)
        
        # 添加边距
        y_min = max(0, y_min - margin)
        y_max = min(self.gray.shape[0], y_max + margin)
        x_min = max(0, x_min - margin)
        x_max = min(self.gray.shape[1], x_max + margin)
        
        roi = self.gray[y_min:y_max, x_min:x_max]
        return roi
    
    def compute_esf(self, roi=None):
        """
        计算边缘扩散函数（Edge Spread Function, ESF）
        
        Args:
            roi: 边缘ROI区域，如果为None则使用整个图像
            
        Returns:
            numpy.ndarray: ESF曲线
        """
        if roi is None:
            roi = self.gray
        
        # 检测边缘方向（水平或垂直）
        grad_x = np.abs(cv2.Sobel(roi, cv2.CV_64F, 1, 0, ksize=3)).mean()
        grad_y = np.abs(cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=3)).mean()
        
        # 沿着梯度最大的方向投影
        if grad_x > grad_y:
            # 垂直边缘，沿x方向投影
            esf = np.mean(roi, axis=0)
        else:
            # 水平边缘，沿y方向投影
            esf = np.mean(roi, axis=1)
        
        # 亚像素插值，提高采样密度
        x_original = np.arange(len(esf))
        x_interpolated = np.linspace(0, len(esf)-1, len(esf)*4)
        esf_interpolated = np.interp(x_interpolated, x_original, esf)
        
        return esf_interpolated
    
    def compute_lsf(self, esf):
        """
        计算线扩散函数（Line Spread Function, LSF）
        LSF = dESF/dx (ESF的一阶导数)
        
        Args:
            esf: 边缘扩散函数
            
        Returns:
            numpy.ndarray: LSF曲线
        """
        # 使用中心差分法计算导数
        lsf = np.gradient(esf)
        
        # 使用高斯滤波平滑LSF，减少噪声
        lsf_smoothed = ndimage.gaussian_filter1d(lsf, sigma=2)
        
        return lsf_smoothed
    
    def compute_mtf_from_lsf(self, lsf):
        """
        从LSF计算MTF曲线
        MTF = |FFT(LSF)| / |FFT(LSF)[0]|
        
        Args:
            lsf: 线扩散函数
            
        Returns:
            tuple: (frequencies, mtf_values)
        """
        # 对LSF进行FFT
        lsf_fft = fft(lsf)
        
        # 计算MTF（取模值并归一化）
        mtf = np.abs(lsf_fft)
        mtf = mtf / (mtf[0] + 1e-10)  # 归一化，使MTF(0) = 1
        
        # 只取正频率部分
        n = len(lsf)
        mtf = mtf[:n//2]
        
        # 计算对应的频率
        frequencies = fftfreq(n, d=1.0)[:n//2]
        
        return frequencies, mtf
    
    def compute_mtf50(self, frequencies, mtf):
        """
        计算MTF50值（MTF下降到0.5时的空间频率）
        这是衡量图像清晰度的关键指标
        
        Args:
            frequencies: 频率数组
            mtf: MTF值数组
            
        Returns:
            float: MTF50值（cycles/pixel）
        """
        # 找到MTF首次下降到0.5以下的位置
        idx = np.where(mtf < 0.5)[0]
        
        if len(idx) == 0:
            # 如果MTF始终大于0.5，返回最大频率
            return frequencies[-1]
        
        idx50 = idx[0]
        
        if idx50 == 0:
            return frequencies[0]
        
        # 线性插值获得精确的MTF50频率
        f1, f2 = frequencies[idx50-1], frequencies[idx50]
        m1, m2 = mtf[idx50-1], mtf[idx50]
        
        # 线性插值: f = f1 + (0.5 - m1) * (f2 - f1) / (m2 - m1)
        if abs(m2 - m1) > 1e-10:
            mtf50 = f1 + (0.5 - m1) * (f2 - f1) / (m2 - m1)
        else:
            mtf50 = f1
        
        return mtf50
    
    def compute_mtf_sharpness(self):
        """
        完整的MTF刃边法清晰度评估
        按照ISO 12233标准实现：ESF → LSF → FFT → MTF → MTF50
        
        Returns:
            dict: 包含MTF50、平均MTF等指标的字典
        """
        # 1. 提取边缘ROI
        roi = self.extract_edge_roi()
        
        # 2. 计算ESF
        esf = self.compute_esf(roi)
        
        # 3. 计算LSF（ESF的导数）
        lsf = self.compute_lsf(esf)
        
        # 4. 通过FFT计算MTF
        frequencies, mtf = self.compute_mtf_from_lsf(lsf)
        
        # 5. 计算MTF50
        mtf50 = self.compute_mtf50(frequencies, mtf)
        
        # 保存结果
        self.mtf_curve = mtf
        self.frequencies = frequencies
        self.mtf50 = mtf50
        
        # 计算其他有用的指标
        mtf30 = self.compute_mtf_at_value(frequencies, mtf, 0.3)
        mtf10 = self.compute_mtf_at_value(frequencies, mtf, 0.1)
        
        # 计算MTF曲线下面积（Area Under Curve）作为综合指标
        mtf_auc = np.trapezoid(mtf, frequencies)
        
        # 归一化MTF50到0-100范围（用于评分）
        # 通常MTF50在0.1-0.5范围内，映射到0-100
        sharpness_score = min(100, mtf50 * 200)
        
        results = {
            'mtf50': mtf50,
            'mtf30': mtf30,
            'mtf10': mtf10,
            'mtf_auc': mtf_auc,
            'sharpness_score': sharpness_score,
            'frequencies': frequencies,
            'mtf_curve': mtf
        }
        
        return results
    
    def compute_mtf_at_value(self, frequencies, mtf, value):
        """
        计算MTF下降到指定值时的频率
        
        Args:
            frequencies: 频率数组
            mtf: MTF值数组
            value: 目标MTF值（例如0.3, 0.1）
            
        Returns:
            float: 对应的频率值
        """
        idx = np.where(mtf < value)[0]
        if len(idx) == 0:
            return frequencies[-1]
        
        idx_val = idx[0]
        if idx_val == 0:
            return frequencies[0]
        
        # 线性插值
        f1, f2 = frequencies[idx_val-1], frequencies[idx_val]
        m1, m2 = mtf[idx_val-1], mtf[idx_val]
        
        if abs(m2 - m1) > 1e-10:
            freq = f1 + (value - m1) * (f2 - f1) / (m2 - m1)
        else:
            freq = f1
        
        return freq
    
    def get_sharpness_level(self, mtf50):
        """
        根据MTF50值判断图像质量等级
        
        Args:
            mtf50: MTF50数值（cycles/pixel）
            
        Returns:
            str: 清晰度等级描述
        """
        # MTF50的典型范围：0.1-0.5 cycles/pixel
        if mtf50 > 0.4:
            return "非常清晰"
        elif mtf50 > 0.3:
            return "清晰"
        elif mtf50 > 0.2:
            return "较清晰"
        elif mtf50 > 0.1:
            return "轻微模糊"
        else:
            return "模糊"


def process_single_image(image_path, verbose=True):
    """
    处理单张图像
    
    Args:
        image_path: 图像路径
        verbose: 是否打印详细信息
        
    Returns:
        tuple: (filename, mtf50_value, sharpness_score, level)
    """
    try:
        evaluator = MTFSharpnessEvaluator(image_path)
        evaluator.load_image()
        
        # 使用MTF刃边法计算清晰度
        results = evaluator.compute_mtf_sharpness()
        mtf50 = results['mtf50']
        sharpness_score = results['sharpness_score']
        level = evaluator.get_sharpness_level(mtf50)
        
        filename = os.path.basename(image_path)
        
        if verbose:
            print(f"✓ {filename}: MTF50={mtf50:.4f} | 评分={sharpness_score:.2f} | {level}")
        
        return filename, mtf50, sharpness_score, level
        
    except Exception as e:
        if verbose:
            print(f"✗ {os.path.basename(image_path)}: 处理失败 - {e}")
        return os.path.basename(image_path), None, None, "错误"


def process_folder(folder_path, output_file=None):
    """
    批量处理文件夹中的所有图像
    
    Args:
        folder_path: 文件夹路径
        output_file: 输出结果文件路径（可选）
    """
    # 支持的图像格式
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.tif']
    
    # 获取所有图像文件
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))
        image_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    
    if not image_files:
        print(f"\n错误: 文件夹 '{folder_path}' 中没有找到图像文件")
        print(f"支持的格式: {', '.join(image_extensions)}")
        return
    
    print("\n" + "="*90)
    print(f"MTF图像清晰度批量评估（刃边法 - ISO 12233标准）")
    print("="*90)
    print(f"文件夹: {folder_path}")
    print(f"找到图像: {len(image_files)} 张")
    print("-"*90)
    
    # 处理所有图像
    results = []
    for img_path in image_files:
        filename, mtf50, score, level = process_single_image(img_path, verbose=True)
        if mtf50 is not None:
            results.append({
                'filename': filename,
                'path': img_path,
                'mtf50': mtf50,
                'score': score,
                'level': level
            })
    
    if not results:
        print("\n没有成功处理任何图像")
        return
    
    # 按MTF50排序（值越大越清晰）
    results.sort(key=lambda x: x['mtf50'], reverse=True)
    
    # 统计信息
    print("\n" + "="*90)
    print("统计信息")
    print("="*90)
    
    mtf50_values = [r['mtf50'] for r in results]
    score_values = [r['score'] for r in results]
    avg_mtf50 = np.mean(mtf50_values)
    max_mtf50 = np.max(mtf50_values)
    min_mtf50 = np.min(mtf50_values)
    avg_score = np.mean(score_values)
    
    print(f"成功处理: {len(results)}/{len(image_files)} 张")
    print(f"平均MTF50: {avg_mtf50:.4f} cycles/pixel")
    print(f"最高MTF50: {max_mtf50:.4f} cycles/pixel")
    print(f"最低MTF50: {min_mtf50:.4f} cycles/pixel")
    print(f"平均评分: {avg_score:.2f}/100")
    
    # 清晰度等级分布
    level_count = {}
    for r in results:
        level = r['level']
        level_count[level] = level_count.get(level, 0) + 1
    
    print("\n清晰度等级分布:")
    for level in ['非常清晰', '清晰', '较清晰', '轻微模糊', '模糊']:
        if level in level_count:
            print(f"  {level}: {level_count[level]} 张")
    
    # 显示排名
    print("\n" + "="*90)
    print("清晰度排名 (Top 10)")
    print("="*90)
    print(f"{'排名':<6} {'文件名':<35} {'MTF50':<15} {'评分':<10} {'等级':<10}")
    print("-"*90)
    
    for i, result in enumerate(results[:10], 1):
        print(f"{i:<6} {result['filename']:<35} {result['mtf50']:<15.4f} {result['score']:<10.2f} {result['level']:<10}")
    
    if len(results) > 10:
        print(f"\n... 还有 {len(results) - 10} 张图像")
    
    # 保存结果到文件
    if output_file:
        save_results_to_file(results, output_file)
        print(f"\n✓ 结果已保存到: {output_file}")
    
    print("="*90 + "\n")
    
    return results


def save_results_to_file(results, output_file):
    """
    保存结果到文本文件
    
    Args:
        results: 结果列表
        output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("MTF图像清晰度评估结果（刃边法 - ISO 12233标准）\n")
        f.write("="*100 + "\n\n")
        
        f.write(f"{'排名':<6} {'文件名':<50} {'MTF50':<20} {'评分':<12} {'等级':<10}\n")
        f.write("-"*100 + "\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"{i:<6} {result['filename']:<50} {result['mtf50']:<20.6f} {result['score']:<12.2f} {result['level']:<10}\n")
        
        f.write("\n" + "="*100 + "\n")
        f.write("\n关于MTF50:\n")
        f.write("  MTF50是调制传递函数下降到50%时的空间频率，单位为 cycles/pixel\n")
        f.write("  它是国际标准ISO 12233推荐的图像清晰度评价指标\n")
        f.write("  MTF50值越大，表示图像能够还原更高频率的细节，清晰度越高\n\n")
        f.write("清晰度参考标准:\n")
        f.write("  > 0.4 cycles/pixel: 非常清晰\n")
        f.write("  0.3-0.4 cycles/pixel: 清晰\n")
        f.write("  0.2-0.3 cycles/pixel: 较清晰\n")
        f.write("  0.1-0.2 cycles/pixel: 轻微模糊\n")
        f.write("  < 0.1 cycles/pixel: 模糊\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='MTF图像清晰度评估工具 - 刃边法（ISO 12233标准）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
算法说明:
  本程序实现了基于ISO 12233标准的MTF刃边法:
  1. ESF (Edge Spread Function) - 边缘扩散函数提取
  2. LSF (Line Spread Function) - 线扩散函数计算 (LSF = dESF/dx)
  3. FFT变换 - 对LSF进行傅里叶变换
  4. MTF曲线 - 调制传递函数 (MTF = |FFT(LSF)|)
  5. MTF50 - MTF下降到0.5时的空间频率（清晰度核心指标）

使用示例:
  # 评估单张图像
  python mtf_sharpness.py image.png
  
  # 批量评估文件夹中的所有图像
  python mtf_sharpness.py /path/to/folder
  
  # 批量评估并保存结果到文件
  python mtf_sharpness.py /path/to/folder --output results.txt
        """
    )
    
    parser.add_argument('path', help='图像文件路径或文件夹路径')
    parser.add_argument('--output', '-o', help='输出结果文件路径（仅用于文件夹批量处理）')
    
    args = parser.parse_args()
    
    try:
        path = args.path
        
        # 判断是文件还是文件夹
        if os.path.isfile(path):
            # 处理单张图像
            print("\n处理单张图像...")
            evaluator = MTFSharpnessEvaluator(path)
            evaluator.load_image()
            results = evaluator.compute_mtf_sharpness()
            
            filename = os.path.basename(path)
            mtf50 = results['mtf50']
            mtf30 = results['mtf30']
            mtf10 = results['mtf10']
            score = results['sharpness_score']
            level = evaluator.get_sharpness_level(mtf50)
            
            print("\n" + "="*70)
            print("MTF图像清晰度评估结果（刃边法）")
            print("="*70)
            print(f"文件名: {filename}")
            print(f"图像尺寸: {evaluator.gray.shape}")
            print("-"*70)
            print(f"MTF50: {mtf50:.6f} cycles/pixel  [主要指标]")
            print(f"MTF30: {mtf30:.6f} cycles/pixel")
            print(f"MTF10: {mtf10:.6f} cycles/pixel")
            print(f"清晰度评分: {score:.2f}/100")
            print(f"清晰度等级: {level}")
            print("="*70)
            print("\n说明:")
            print("  MTF50是ISO 12233标准推荐的清晰度评价指标")
            print("  表示MTF下降到0.5时的空间频率（cycles/pixel）")
            print("  值越大表示图像越清晰")
            print("\n参考标准:")
            print("  > 0.4: 非常清晰")
            print("  0.3-0.4: 清晰")
            print("  0.2-0.3: 较清晰")
            print("  0.1-0.2: 轻微模糊")
            print("  < 0.1: 模糊")
            print("="*70 + "\n")
            
        elif os.path.isdir(path):
            # 处理文件夹
            process_folder(path, args.output)
        else:
            print(f"\n错误: 路径不存在: {path}\n")
            return 1
    
    except Exception as e:
        print(f"\n错误: {e}\n")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
