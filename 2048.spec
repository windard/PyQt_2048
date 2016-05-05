# -*- mode: python -*-

block_cipher = None


a = Analysis(['2048.py'],
             pathex=['/home/windard/github/PyQt_2048'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='2048',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='2048.ico')
