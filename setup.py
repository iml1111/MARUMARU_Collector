from cx_Freeze import setup, Executable
import sys

buildOptions = dict(packages = 
	["idna","urllib","bs4","requests","re","sys","os","img2pdf"], 
	excludes = [])
exe = [Executable("MMC.py")]

setup(
    name='MARUMARU_Collector',
    version = '0.3',
    author = "IML",
    description = 'MARUMARU Web Crawler',
    options = dict(build_exe = buildOptions),
    executables = exe
)
