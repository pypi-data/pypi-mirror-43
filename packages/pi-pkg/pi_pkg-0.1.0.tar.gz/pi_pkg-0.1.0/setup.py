import setuptools

with open('README.md', encoding='utf_8') as fh:
    readme = fh.read()

setuptools.setup(
    name='pi_pkg',
    author="zhangjiong",
    author_email="49005718@qq.com",
    version='0.1.0',
    description='计算pi的小程序',
    long_description=readme,
    long_description_content_type='text/markdown; charset=UTF-8',
    url='https://github.com/pypa/sampleproject',
    license='MIT',
    install_requires=[''],
    entry_points={'console_scripts': ['wordcloud_cli=wordcloud.__main__:main']},
    packages=setuptools.find_packages(),

)