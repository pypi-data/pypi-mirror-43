from setuptools import setup

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
exec(open('rasa/version.py').read())

# Get the long description from the README file
with open("README.md", "r") as fh:
    long_description = fh.read()

tests_requires = [
    "pytest~=3.0",
    "pytest-pycodestyle~=1.3",
    "pytest-cov~=2.0",
]

install_requires = [
    "rasa-core>=0.14.0a1",
    "rasa-nlu[tensorflow]>=0.15.0a2",
    "rasa-core-sdk~=0.13.0a1",
    "questionary~=1.0",
]

setup(
    name="rasa",
    entry_points={
        'console_scripts': ['rasa=rasa.__main__:main'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        # supported python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
    ],
    version=__version__,
    install_requires=install_requires,
    tests_require=tests_requires,
    description="Rasa Stack - A package which includes Rasa Core and Rasa NLU",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rasa Technologies GmbH",
    author_email="hi@rasa.com",
    maintainer="Tom Bocklisch",
    maintainer_email="tom@rasa.com",
    license="Apache 2.0",
    keywords="nlp machine-learning machine-learning-library bot bots "
             "botkit rasa conversational-agents conversational-ai chatbot"
             "chatbot-framework bot-framework",
    url="https://rasa.com",
    project_urls={
        "Bug Reports": "https://github.com/rasahq/rasa_stack/issues",
        "Source": "https://github.com/rasahq/rasa_stack",
    },
)

print("\nWelcome to Rasa!")
print("If any questions please visit documentation "
      "page https://rasa.com/docs/")
print("or join the community discussions on https://forum.rasa.com")
