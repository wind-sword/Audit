# -*- mode: python ; coding: utf-8 -*-

# 此文件为打包配置文件

block_cipher = None


a = Analysis(['main.py'],
             pathex=['E:\\GitHub repository\\Audit'],
             binaries=[],
             datas=[('db','db'),('project_word','project_word'),('resource_dir','resource_dir'),('zgfh_word','zgfh_word')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='审计整改管理系统1.0',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='icon.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='审计整改管理系统1.0')
