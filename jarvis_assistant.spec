from PyInstaller.utils.hooks import collect_dynamic_libs
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['jarvis_assistant.py'],
    pathex=[],
    binaries = collect_dynamic_libs('pvporcupine'),
    datas=[
        ('E:\\Vaazha\\jarvis.ppn', '.'),
        ('E:\\Vaazha\\porcupine_params.pv', '.'),
        ('E:\\Vaazha\\libpv_porcupine.dll', '.'),
        ('E:\\Vaazha\\vosk-model-en-us-daanzu-20200328', 'vosk-model-en-us-daanzu-20200328'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='jarvis_assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='jarvis_assistant'
)
