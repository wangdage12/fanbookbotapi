from setuptools import setup, find_packages

setup(
    name='fanbookbotapi',
    version='1.2.7',
    packages=find_packages(),
    install_requires=[
        # 这里列出你的依赖包，例如：
        # 'numpy',
        'requests',
        'coloredlogs',
        'websocket-client',
        'pygments',
        'colorama'
    ],
    author='wangdage',
    author_email='fanbookwdg1122@outlook.com',
    description='fanbook bot api',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fanbook-wangdage/fanbookbotapi/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
