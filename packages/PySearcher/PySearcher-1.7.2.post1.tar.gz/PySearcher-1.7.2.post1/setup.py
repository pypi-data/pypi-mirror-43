import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='PySearcher',
    version='1.7.2.post1',
    description='Python Search Engine',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='code search tools',
    install_requires=[],
    packages=setuptools.find_packages(),
    author='Tyrone Zhao',
    author_email='tyrone-zhao@qq.com',
    url='https://github.com/Tyrone-Zhao/PySearcher',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable'
        'Development Status :: 5 - Production/Stable',  # 当前开发进度等级（测试版，正式版等）
        'Intended Audience :: Developers',  # 模块适用人群
        'Topic :: Software Development :: Code Generators',  # 给模块加话题标签
        'License :: OSI Approved :: MIT License',  # 模块的license

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={  # 项目相关的额外链接
        'Blog': 'https://blog.csdn.net/weixin_41845533',
    },
)

# cd GitHub/PySearcher_upload && rm -rf dist/* && python3 setup.py sdist bdist_wheel
# twine upload dist/*
# pip3 install -i https://pypi.org/project/ --user --upgrade pysearcher