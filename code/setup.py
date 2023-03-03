import sys
import os
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
version = "1.1"
code = "{8b1ffaf6-b046-11ed-afa1-0242ac120002}"

bdist_msi_options = {
    "upgrade_code": code,
}


build_exe_options = {"packages": ["tkinter"],
                     "include_files": ["img", "icon.ico", "option"]}

executables = [
    Executable(
        script="translate.py",
        copyright="Copyright (C) 2023 Igor Ratajczak",
        base=base,
        icon="icon.ico",
        shortcut_name="PolGla Tłumacz",
        shortcut_dir="ProgramMenuFolder"
    )]

setup(
    name="PolGla Tłumacz",
    author="Igor Ratajczak",
    version=version,
    description="Tłumacz, który przetłumaczy polski na głagolice i odwrotnie.",
    executables=executables,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
)
#  "upgrade_code": "{8b1ffaf6-b046-11ed-afa1-0242ac120002}"
