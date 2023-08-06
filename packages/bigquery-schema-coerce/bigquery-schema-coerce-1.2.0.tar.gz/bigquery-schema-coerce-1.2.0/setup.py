from setuptools import setup, find_packages


setup(
    name="bigquery-schema-coerce",
    version="1.2.0",
    description=(
        "Force python dictionary to type convert and project onto the given schema"
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="bigquery-schema-coerce",
    author="Jon Robison",
    author_email="narfman0@gmail.com",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["google-cloud-bigquery", "python-dateutil"],
    test_suite="tests",
)
