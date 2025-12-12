"""Setup configuration for document gap analyzer."""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='document-gap-analyzer',
    version='1.0.0',
    description='AI-powered document gap analysis tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Confeto',
    packages=find_packages(),
    install_requires=[
        'PyPDF2>=3.0.1',
        'python-docx>=1.1.0',
        'pdfplumber>=0.10.3',
        'pypdf>=3.17.4',
        'openai>=1.12.0',
        'anthropic>=0.18.1',
        'python-dotenv>=1.0.0',
        'click>=8.1.7',
        'rich>=13.7.0',
        'pydantic>=2.5.3',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.3',
            'pytest-cov>=4.1.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'gap-analyzer=src.cli:cli',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
