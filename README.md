# Python Image Crawler

> **Selenium-based image crawler** for collecting training data — originally built to scrape K-Pop idol photos for the [kpopface](https://github.com/moony01/kpopface) AI face matcher.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?logo=selenium)](https://www.selenium.dev/)

---

## Overview

A Python utility that uses Selenium WebDriver to scrape images from search engines based on keyword queries. Built as the data pipeline for training the [kpopface](https://github.com/moony01/kpopface) Teachable Machine model — given a list of K-Pop idol names, it downloads dozens of representative photos per name into category folders.

Useful as a starting point for any image-based ML training dataset.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.9 |
| **Browser Automation** | Selenium WebDriver |

## Local Development

```bash
git clone https://github.com/moony01/py-image-crawling.git
cd py-image-crawling

pip install -r requirements.txt

# Edit search keywords in index.py, then run
python index.py
```

Downloaded images land in the `dataset/` directory.

## License

[MIT License](LICENSE) © 2024–2026 [moony01](https://github.com/moony01)

## Contact

- 👤 [@moony01](https://github.com/moony01)
- 💖 [github.com/sponsors/moony01](https://github.com/sponsors/moony01)
