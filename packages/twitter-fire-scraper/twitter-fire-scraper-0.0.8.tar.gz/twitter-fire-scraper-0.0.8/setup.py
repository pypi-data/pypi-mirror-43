import setuptools

with open("../README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="twitter-fire-scraper",
    version="0.0.8",

    author="Henry Post",
    author_email="HenryFBP@gmail.com",

    description="A tool to scrape data about fires from Twitter.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/raaraa/IPRO497-Analytics-Team/tree/master/coding/twitter-fire-scraper",

    package_data = {
        b'twitter-fire-scraper': [
            'data/*.yml',
            'templates/*.html'
        ]
    },

    packages=setuptools.find_packages(),
    install_requires=[
        "click",
        "itsdangerous",
        "nltk",
        "oauthlib",
        "requests",
        "requests-oauthlib",
        "six",
        "textblob",
        "tweepy",
        "Flask",
        "Jinja2",
        "MarkupSafe",
        "Werkzeug",
        "tmdbsimple",
        "colorama",
        "pymongo",
        "typing",
        "pyyaml",
    ],

    classifiers=[
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
