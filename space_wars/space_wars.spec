# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\benga\\OneDrive\\Desktop\\python_scripts\\space_wars\\src\\space_wars.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/benga/OneDrive/Desktop/python_scripts/space_wars/fonts', 'fonts'), ('C:/Users/benga/OneDrive/Desktop/python_scripts/space_wars/sounds', 'sounds'), ('C:/Users/benga/OneDrive/Desktop/python_scripts/space_wars/images', 'images')],
    hiddenimports=['pygame', 'pathlib', 'random', 'sys', 'time', 'os'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='space_wars',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\benga\\OneDrive\\Desktop\\python_scripts\\space_wars\\images\\space_wars.ico'],
)
