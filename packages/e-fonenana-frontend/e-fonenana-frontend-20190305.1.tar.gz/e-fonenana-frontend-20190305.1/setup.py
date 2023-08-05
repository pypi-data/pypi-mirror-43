from setuptools import setup, find_packages

setup(
    name="e-fonenana-frontend",
    version="20190305.1",
    description="The E-Fonenana frontend",
    url="https://gitlab.com/teamdown/smart-home/frontend",
    author="The E-Fonenana Authors",
    author_email="nyandrianinamamy@gmail.com",
    license="Apache License 2.0",
    packages=find_packages(
        include=[
            "hass_frontend",
            "hass_frontend_es5",
            "hass_frontend.*",
            "hass_frontend_es5.*",
        ]
    ),
    install_requires=["user-agents==1.1.0"],
    include_package_data=True,
    zip_safe=False,
    download_url="https://github.com/teamdown/e-fonenana-frontend/archive/20190305.1.tar.gz",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Other Audience",
        "Topic :: Other/Nonlisted Topic",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
