# py-image-crawling

> **General-purpose Python image crawler** — Selenium-based scraper that downloads images from search engines based on any keyword list. Build custom image datasets for ML training, research, or visual analysis.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?logo=selenium)](https://www.selenium.dev/)

---

## Overview

A general-purpose Python utility that uses Selenium WebDriver to scrape images from search engines. Pass any list of keywords and the crawler downloads dozens of representative photos per keyword into category folders — making it easy to build a labeled image dataset for any domain.

The tool is keyword-agnostic: animals, products, places, faces, objects, paintings, anything indexed by image search engines.

## Use Cases

- 📊 **ML / AI training data collection** — Build labeled image datasets for classification or detection models
- 🔬 **Visual research** — Bulk-collect images for academic analysis
- 🛒 **Product / market analysis** — Scrape product images by category
- 🎨 **Reference libraries** — Build mood boards or visual archives

## Real-world Example

Originally built as the data pipeline for the [kpopface](https://github.com/moony01/kpopface) AI face matcher — given a list of K-Pop idol names, it downloaded hundreds of representative photos per idol to train a Teachable Machine model. The same crawler works just as well with any other keyword set.

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

Downloaded images land in the `dataset/` directory, organized into one folder per keyword.

## License

[MIT License](LICENSE) © 2024–2026 [moony01](https://github.com/moony01)

## Contact

- 👤 [@moony01](https://github.com/moony01)
- 💖 [github.com/sponsors/moony01](https://github.com/sponsors/moony01)
