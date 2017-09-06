::清空之前的测试文件
@echo off
echo 清理测试文件
rmdir /s/q .\htmlcov\
coverage erase
::开始测试
echo 开始测试...
coverage run .\test_redque.py
::生成报告
coverage report -m
choice /M "是否生成html并打开页面"
if %ERRORLEVEL% == 1 (
    ::生成html并打开
    coverage html
    start .\htmlcov\index.html
)
