#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MTF图像清晰度评估工具 - GUI版本
支持Windows/Mac/Linux跨平台
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import glob
from pathlib import Path
from mtf_sharpness import MTFSharpnessEvaluator
import numpy as np


class MTFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MTF图像清晰度评估工具")
        self.root.geometry("900x700")
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        self.results = []
        
    def create_widgets(self):
        # 标题
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title = ttk.Label(
            title_frame, 
            text="MTF图像清晰度评估工具", 
            font=("Arial", 18, "bold")
        )
        title.pack()
        
        subtitle = ttk.Label(
            title_frame,
            text="基于ISO 12233标准 - 刃边法",
            font=("Arial", 10)
        )
        subtitle.pack()
        
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：输入控制
        left_frame = ttk.LabelFrame(main_frame, text="输入选择", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # 单文件选择
        file_frame = ttk.Frame(left_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            file_frame, 
            text="选择单张图片", 
            command=self.select_file,
            width=20
        ).pack(pady=5)
        
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # 文件夹选择
        folder_frame = ttk.Frame(left_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            folder_frame, 
            text="选择文件夹（批量）", 
            command=self.select_folder,
            width=20
        ).pack(pady=5)
        
        # 当前路径显示
        self.path_var = tk.StringVar(value="未选择")
        path_label = ttk.Label(
            left_frame, 
            textvariable=self.path_var,
            wraplength=200,
            justify=tk.LEFT
        )
        path_label.pack(fill=tk.X, pady=10)
        
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # 操作按钮
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = ttk.Button(
            button_frame,
            text="开始评估",
            command=self.start_evaluation,
            state=tk.DISABLED
        )
        self.start_btn.pack(fill=tk.X, pady=5)
        
        self.export_btn = ttk.Button(
            button_frame,
            text="导出结果",
            command=self.export_results,
            state=tk.DISABLED
        )
        self.export_btn.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_frame,
            text="清空结果",
            command=self.clear_results
        ).pack(fill=tk.X, pady=5)
        
        # 进度条
        self.progress = ttk.Progressbar(
            left_frame,
            mode='determinate',
            length=200
        )
        self.progress.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(
            left_frame,
            textvariable=self.status_var,
            font=("Arial", 9)
        )
        status_label.pack()
        
        # 右侧：结果显示
        right_frame = ttk.LabelFrame(main_frame, text="评估结果", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            width=60,
            height=30,
            font=("Courier", 9)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 底部信息栏
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        info_text = ttk.Label(
            info_frame,
            text="支持格式: PNG, JPG, JPEG, BMP, TIFF | MTF50 > 0.3 为清晰",
            font=("Arial", 8),
            foreground="gray"
        )
        info_text.pack()
        
    def select_file(self):
        """选择单个文件"""
        filename = filedialog.askopenfilename(
            title="选择图像文件",
            filetypes=[
                ("图像文件", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.current_path = filename
            self.is_folder = False
            self.path_var.set(f"文件: {os.path.basename(filename)}")
            self.start_btn.config(state=tk.NORMAL)
            
    def select_folder(self):
        """选择文件夹"""
        folder = filedialog.askdirectory(title="选择文件夹")
        if folder:
            self.current_path = folder
            self.is_folder = True
            
            # 统计图片数量
            image_count = self.count_images(folder)
            self.path_var.set(f"文件夹: {os.path.basename(folder)}\n({image_count}张图片)")
            self.start_btn.config(state=tk.NORMAL)
    
    def count_images(self, folder):
        """统计文件夹中的图片数量"""
        extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.tif']
        count = 0
        for ext in extensions:
            count += len(glob.glob(os.path.join(folder, ext)))
            count += len(glob.glob(os.path.join(folder, ext.upper())))
        return count
    
    def start_evaluation(self):
        """开始评估"""
        self.start_btn.config(state=tk.DISABLED)
        self.result_text.delete(1.0, tk.END)
        self.results = []
        
        # 在新线程中运行，避免界面卡顿
        thread = threading.Thread(target=self.run_evaluation)
        thread.daemon = True
        thread.start()
    
    def run_evaluation(self):
        """执行评估（在后台线程）"""
        try:
            if self.is_folder:
                self.evaluate_folder()
            else:
                self.evaluate_file()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"评估失败：{str(e)}"))
        finally:
            self.root.after(0, lambda: self.start_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.status_var.set("完成"))
    
    def evaluate_file(self):
        """评估单个文件"""
        self.update_status("正在评估...")
        self.update_progress(50)
        
        try:
            evaluator = MTFSharpnessEvaluator(self.current_path)
            evaluator.load_image()
            results = evaluator.compute_mtf_sharpness()
            
            filename = os.path.basename(self.current_path)
            mtf50 = results['mtf50']
            score = results['sharpness_score']
            level = evaluator.get_sharpness_level(mtf50)
            
            self.results.append({
                'filename': filename,
                'mtf50': mtf50,
                'score': score,
                'level': level
            })
            
            # 显示结果
            output = f"""
{'='*70}
MTF图像清晰度评估结果
{'='*70}
文件名: {filename}
图像尺寸: {evaluator.gray.shape}
{'─'*70}
MTF50: {mtf50:.6f} cycles/pixel
MTF30: {results['mtf30']:.6f} cycles/pixel
MTF10: {results['mtf10']:.6f} cycles/pixel
清晰度评分: {score:.2f}/100
清晰度等级: {level}
{'='*70}

参考标准:
  > 0.4: 非常清晰
  0.3-0.4: 清晰
  0.2-0.3: 较清晰
  0.1-0.2: 轻微模糊
  < 0.1: 模糊
"""
            self.update_result(output)
            self.update_progress(100)
            self.root.after(0, lambda: self.export_btn.config(state=tk.NORMAL))
            
        except Exception as e:
            self.update_result(f"评估失败: {str(e)}")
    
    def evaluate_folder(self):
        """评估文件夹中的所有图片"""
        # 获取所有图片
        extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.tif']
        image_files = []
        for ext in extensions:
            image_files.extend(glob.glob(os.path.join(self.current_path, ext)))
            image_files.extend(glob.glob(os.path.join(self.current_path, ext.upper())))
        
        if not image_files:
            self.update_result("错误: 文件夹中没有找到图像文件")
            return
        
        total = len(image_files)
        self.update_result(f"{'='*70}\n批量评估开始\n{'='*70}\n")
        self.update_result(f"找到 {total} 张图片\n\n")
        
        # 逐个评估
        for i, img_path in enumerate(image_files, 1):
            try:
                filename = os.path.basename(img_path)
                self.update_status(f"正在评估 {i}/{total}: {filename}")
                
                evaluator = MTFSharpnessEvaluator(img_path)
                evaluator.load_image()
                results = evaluator.compute_mtf_sharpness()
                
                mtf50 = results['mtf50']
                score = results['sharpness_score']
                level = evaluator.get_sharpness_level(mtf50)
                
                self.results.append({
                    'filename': filename,
                    'mtf50': mtf50,
                    'score': score,
                    'level': level
                })
                
                self.update_result(f"✓ {filename}: MTF50={mtf50:.4f} | 评分={score:.2f} | {level}\n")
                self.update_progress(int(i * 100 / total))
                
            except Exception as e:
                self.update_result(f"✗ {filename}: 失败 - {str(e)}\n")
        
        # 显示统计
        self.show_statistics()
        self.root.after(0, lambda: self.export_btn.config(state=tk.NORMAL))
    
    def show_statistics(self):
        """显示统计信息"""
        if not self.results:
            return
        
        mtf50_values = [r['mtf50'] for r in self.results]
        avg_mtf50 = np.mean(mtf50_values)
        max_mtf50 = np.max(mtf50_values)
        min_mtf50 = np.min(mtf50_values)
        
        # 排序
        sorted_results = sorted(self.results, key=lambda x: x['mtf50'], reverse=True)
        
        output = f"""
{'='*70}
统计信息
{'='*70}
成功评估: {len(self.results)} 张
平均MTF50: {avg_mtf50:.4f} cycles/pixel
最高MTF50: {max_mtf50:.4f} cycles/pixel
最低MTF50: {min_mtf50:.4f} cycles/pixel

{'='*70}
清晰度排名 (Top 10)
{'='*70}
{'排名':<6} {'文件名':<30} {'MTF50':<15} {'等级':<10}
{'─'*70}
"""
        self.update_result(output)
        
        for i, r in enumerate(sorted_results[:10], 1):
            line = f"{i:<6} {r['filename']:<30} {r['mtf50']:<15.4f} {r['level']:<10}\n"
            self.update_result(line)
        
        if len(sorted_results) > 10:
            self.update_result(f"\n... 还有 {len(sorted_results) - 10} 张图像\n")
        
        self.update_result(f"{'='*70}\n")
    
    def export_results(self):
        """导出结果到文件"""
        if not self.results:
            messagebox.showwarning("警告", "没有可导出的结果")
            return
        
        filename = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.result_text.get(1.0, tk.END))
                messagebox.showinfo("成功", f"结果已保存到:\n{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def clear_results(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        self.results = []
        self.progress['value'] = 0
        self.status_var.set("就绪")
        self.export_btn.config(state=tk.DISABLED)
    
    def update_result(self, text):
        """更新结果显示"""
        def _update():
            self.result_text.insert(tk.END, text)
            self.result_text.see(tk.END)
        self.root.after(0, _update)
    
    def update_status(self, text):
        """更新状态栏"""
        self.root.after(0, lambda: self.status_var.set(text))
    
    def update_progress(self, value):
        """更新进度条"""
        self.root.after(0, lambda: self.progress.config(value=value))


def main():
    root = tk.Tk()
    app = MTFApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
