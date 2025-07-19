# Telegram Bot API Spec Extended

This repository automatically generates and maintains an extended version of the official Telegram Bot API specification. The extended specification includes additional information that is not present in the official spec, such as rate limits, premium features, and other details that are useful for developers.

## How it works

The project uses a set of Python scripts to scrape data from various sources, process it, and generate the extended specification. The main scripts are:

- `scraper.py`: This script scrapes data from the official Telegram Bot API documentation and other sources.
- `update_extensions.py`: This script processes the scraped data, uses an AI component to structure it, and generates the `extensions.json` file.
- `merge.py`: This script merges the `extensions.json` file with the official `api.json` file to create the `spec-extended.json` file.

## How to use it

To generate the extended specification, you can run the following command:

```bash
python3 update_extensions.py && python3 merge.py
```

This will generate the `spec-extended.json` and `spec-extended.min.json` files in the root of the repository.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.
