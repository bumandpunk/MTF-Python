#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows应用打包脚本
在Mac上交叉编译Windows .exe文件
"""

import os
import sys
import platform

def create_spec_file():
    """创建PyInstaller配置文件"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['mtf_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MTF清晰度评估工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)
"""
    
    with open('mtf_gui.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✓ 已创建 mtf_gui.spec 配置文件")


def print_instructions():
    """打印打包说明"""
    print("\n" + "="*70)
    print("MTF清晰度评估工具 - Windows打包指南")
    print("="*70)
    
    if platform.system() == 'Darwin':  # macOS
        print("\n【方案1】在Mac上使用Wine打包Windows程序（推荐）")
        print("-"*70)
        print("1. 安装Wine和PyInstaller for Windows:")
        print("   brew install --cask wine-stable")
        print("   pip install pyinstaller")
        print()
        print("2. 使用Docker打包（更可靠）:")
        print("   docker run -v \"$(pwd):/src/\" cdrx/pyinstaller-windows")
        print()
        
        print("\n【方案2】使用GitHub Actions自动打包（最简单）")
        print("-"*70)
        print("1. 将代码上传到GitHub")
        print("2. 使用GitHub Actions自动构建Windows/Mac/Linux版本")
        print("3. 我可以帮你创建.github/workflows配置文件")
        print()
        
        print("\n【方案3】在Windows虚拟机中打包（最直接）")
        print("-"*70)
        print("1. 使用Parallels/VMware安装Windows虚拟机")
        print("2. 在Windows中运行:")
        print("   pip install -r requirements.txt")
        print("   pip install pyinstaller")
        print("   pyinstaller mtf_gui.spec")
        print()
        
        print("\n【方案4】使用云服务器打包")
        print("-"*70)
        print("1. 租用Windows云服务器（阿里云/腾讯云）")
        print("2. 上传代码并在服务器上打包")
        print()
    
    else:  # Windows或Linux
        print("\n当前系统:", platform.system())
        print("\n打包步骤:")
        print("-"*70)
        print("1. 安装PyInstaller:")
        print("   pip install pyinstaller")
        print()
        print("2. 打包应用:")
        print("   pyinstaller mtf_gui.spec")
        print()
        print("3. 生成的程序位于: dist/MTF清晰度评估工具.exe")
        print()
    
    print("="*70)
    print("\n💡 提示: GUI版本已创建，运行查看效果:")
    print("   python mtf_gui.py")
    print("="*70 + "\n")


def main():
    print("正在准备打包配置...")
    create_spec_file()
    print_instructions()
    
    # 询问是否需要创建GitHub Actions配置
    print("\n是否需要创建GitHub Actions自动打包配置? (y/n)")
    # 注意：这里只是说明，实际使用时需要手动确认


if __name__ == '__main__':
    main()
