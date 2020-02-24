import re
import setuptools


with open("README.rst", "r") as file_stream:
    readme = file_stream.read()

with open("requirements.txt", "r") as file_stream:
    install_requires = file_stream.read().splitlines()

with open("jackbox/__init__.py", "r") as file_stream:
    version = re.search(r"^__version__ = [\"]([^\"]*)[\"]", file_stream.read(), re.MULTILINE).group(1)

if version.endswith(("a", "b", "rc")):
    try:
        import subprocess

        process = subprocess.Popen(["git", "rev-list", "--count", "HEAD"], stdout=subprocess.PIPE)
        out, _ = process.communicate()
        if out:
            version += out.decode("utf-8").strip()

        process = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"], stdout=subprocess.PIPE)
        out, _ = process.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()
    except (Exception) as e:
        pass

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
    "Typing :: Typed",
]

extras_require = {
    "docs": [
        "sphinx",
        "sphinxcontrib_trio",
    ],
}

project_urls = {
    "Documentation": "https://jackboxpy.readthedocs.io/en/latest/",
    "Issue Tracker": "https://github.com/ShineyDev/jackbox.py/issues/",
    "Source": "https://github.com/ShineyDev/jackbox.py/",
}

setuptools.setup(author="ShineyDev",
                 classifiers=classifiers,
                 description="An asynchronous Python framework for interacting with Jackbox Games.",
                 extras_require=extras_require,
                 install_requires=install_requires,
                 license="Apache Software License",
                 long_description=readme,
                 long_description_content_type="text/x-rst",
                 name="jackbox.py",
                 packages=["jackbox", "jackbox.enums", "jackbox.helpers", "jackbox.objects", "jackbox.objects.blobs"],
                 project_urls=project_urls,
                 python_requires=">=3.5.2",
                 url="https://github.com/ShineyDev/jackbox.py",
                 version=version)
