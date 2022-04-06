#!/bin/bash
cp executable.py.bak executable.py
rm executable
rm finalExecutable
rm -rf dist
rm -rf build
rm -f executable.spec 
rm -f executable
rm -rf __pycache__
pyarmor obfuscate --output dist/obf --restrict=0 --exact executable.py
mv dist/obf/executable.py .
pyinstaller --noconfirm --onefile --console --add-data "./dist/obf:."  "./executable.py"
rm -rf build/
rm -f executable.spec 
rm -rf __pycache__/
cp dist/executable .
rm -rf dist/
upx -9 executable -o StrongMan
