# -*- mode: python ; coding: utf-8 -*-
# Windows打包配置文件 - 解决scipy和importlib依赖问题

block_cipher = None

a = Analysis(
    ['mtf_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        # tkinter相关
        'PIL._tkinter_finder',
        '_tkinter',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.filedialog',
        'tkinter.messagebox',
        
        # PIL/Pillow相关（关键！用于图像读取）
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'PIL.BmpImagePlugin',  # BMP格式支持
        'PIL.JpegImagePlugin', # JPEG格式支持
        'PIL.PngImagePlugin',  # PNG格式支持
        'PIL.TiffImagePlugin', # TIFF格式支持
        
        # scipy完整导入
        'scipy',
        'scipy.signal',
        'scipy.signal.windows',
        'scipy.signal._peak_finding',
        'scipy.signal.spectral',
        'scipy.ndimage',
        'scipy.ndimage._ni_support',
        'scipy.sparse',
        'scipy.sparse.csgraph',
        'scipy.sparse.linalg',
        'scipy.special',
        'scipy.special._ufuncs',
        'scipy.interpolate',
        'scipy._lib',
        'scipy._lib.messagestream',
        
        # importlib相关 - 解决主要错误
        'importlib',
        'importlib.resources',
        'importlib.metadata',
        'importlib.abc',
        'importlib_resources',
        'importlib_metadata',
        
        # numpy相关
        'numpy',
        'numpy.core',
        'numpy.core._multiarray_umath',
        'numpy.fft',
        'numpy.random',
        
        # opencv相关（作为备用）
        'cv2',
        'cv2.cv2',
        
        # 其他依赖
        'threading',
        'pathlib',
        'glob',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'pandas', 'torch', 'tensorflow'],  # 排除不需要的大型库
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
    icon=None,
)
