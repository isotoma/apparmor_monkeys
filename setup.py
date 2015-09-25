from setuptools import setup, find_packages


setup(
    name = 'apparmor_monkeys',
    version = '0.0.1',
    description = 'Monkeypatches to minimize the permissions required to run python under AppArmor',
    packages = find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ),
)
