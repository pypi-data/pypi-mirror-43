from setuptools import setup

setup(
    name='yapayzekadj',
    version='0.0.1',
    packages=['djangoyz', 'appdjango', 'appdjango.migrations'],
    url='https://github.com/oguz687/djangoyz',
    license='MIT',
    author='oguzhan',
    author_email='oguzhan_687@hotmail.com',
    description='makine öğrenimi django entegrasyonu',
    package_data={"djangoyz": ["static/","templates/"]},

)
