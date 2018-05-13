from cx_Freeze import setup, Executable
import sys

buildOptions = dict(packages = 
	["idna","urllib","bs4","requests","re","sys","os","img2pdf"], 
	excludes = [])
exe = [Executable("MMC.py")]

setup(
    name='MARUMARU_Collector',
    version = '0.1',
    author = "IML",
    description = 'MARUMARU Web Crawler',
    options = dict(build_exe = buildOptions),
    executables = exe
)

# cxfrees는 몇몇패키지를 미리담줘야함https://github.com/anthony-tuininga/cx_Freeze/issues/228
# windows는 sys.eexcutable
#mac은 __file__ (글로벌 사용가능)