from setuptools import setup


dependence = [
    'opencv-python',
    'pyautogui',
    'pyperclip',
    'selenium',
    'easyocr',
    'sympy',
    'lazy_loader',
]

desc = 'pyautobot is a Python library provide functions that do robotic process automation jobs.'

long_desc = '''pyautobot is a Python library provide functions that do robotic process automation jobs.

It combines below librarys to archive the target:

* PyAutoGUI and pyperclip: control clipboard, mouse and keyboard operations.
* Selenium: control Chrome browser.
* OpenCV-Python: provide graphic based operation.
* EasyOCR: provide OCR functions.
'''

version = '1.0.0'

setup(
    name='pyautobot',
    version=version,
    url='https://github.com/blacktear23/pyautobot',
    author='blacktear23',
    author_email='blacktear23@gmail.com',
    description=desc,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license='BSD',
    packages=['pyautobot'],
    scripts=['bin/pyautobot'],
    test_suite='tests',
    install_requires=dependence,
    keywords="automation rpa",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
