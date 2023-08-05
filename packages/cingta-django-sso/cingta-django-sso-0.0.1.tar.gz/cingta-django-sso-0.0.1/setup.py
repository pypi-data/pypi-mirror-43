#coding=utf-8
from setuptools import setup, find_packages

setup(
	name = "cingta-django-sso",
	version = "0.0.1",
	description = "cingta simple sso",
	author = "Vvegetables",
	author_email = "hardwork_fight@163.com",
	license = "Public domain",
	url = "https://github.com/Vvegetables/cingta-django-sso",
	packages = find_packages(),
	platforms = ["all"],
	install_requires = [
		"Django >= 1.11.0, < 2.0",
		"PyMysql >= 0.9.2",
		"webservices >= 0.7",
	],
	include_package_data=True,    # 启用清单文件MANIFEST.in
	exclude_package_date={'':['.gitignore']} #去除部分不想要的文件
)