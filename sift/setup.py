from setuptools import setup

package_name = 'sift'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/sift.launch.py']),  
        ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='SIFT feature detection and matching tutorial package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sift_dataset = sift.sift_dataset:main',
        ],
    },
)

