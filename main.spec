from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import get_package_paths

# Collect all the submodules from PyQt5 and its dependencies
hiddenimports = collect_submodules('PyQt5')
hiddenimports += collect_submodules('sip')

# Collect all the data files from PyQt5 and its dependencies
datas = collect_data_files('PyQt5')
datas += collect_data_files('sip')

# Collect all the additional packages and modules from site-packages
packages, modules = get_package_paths('site-packages')
hiddenimports += packages + modules


# Update the 'pathex' and 'hiddenimports' options in the spec file
# with the paths to your PyQt5 modules
a = Analysis(['main.py', 'activetasktab.py', 'createtask.py', 'dashboard.py', 'mainwindow.py', 'tabdesign.py', 'tasker.py'],
             pathex=packages,
             hiddenimports=hiddenimports,
             datas=datas,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=None)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='mainsub',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)
