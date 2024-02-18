# VLR Scraper

This repository contains two scripts that scrape the [vlr.gg](https://www.vlr.gg) website for match and player data. The first script, `get_match_urls.py` scrapes the matches page and saves the urls of all the matches to a file. The second script, `get_match_details.py` scrapes the match pages (including player data) from those urls and saves the data to a JSON file in NDJSON format.

## Usage

To use the scripts, first install the required packages with `pip install -r requirements.txt`. Then, run the scripts in the following order:

1. `python get_match_urls.py`
2. `python get_match_details.py`

**Note**: The scripts are configured to use a proxy API. If you want to use it, you need to get one (for example, [BrightData](https://brightdata.com)), follow the instructions to get your proxy credentials, and set the `HTTP` and `HTTPS` environment variables in an `.env` file in the root directory of the project. The `.env` file should look like the example file `.env.example`.

If you don't want to use a proxy, you can configure the scripts to not use one by removing the declaration of the `opener` variable at the top of the `get_match_urls.py` and `get_match_details.py` files and replacing them with `opener = urllib.request.build_opener()`.

## Data

As mentioned earlier, matches are saved in NDJSON format. Keep this in mind when reading the data with something like `pandas`. An example of a single match entry can be found in the [match_example.json](./data/match_example.json) file. The data is saved in the `data` folder.

The script will save data to `scraped_data.json` at intervals of 100 matches and saves each scraped match to `scraped_urls.log`, so if your computer crashes or the script is interrupted, you can restart it and it will pick up where it left off, without scraping the same match twice.

**Note:** The stats are saved for each player for each map (including stats for their performance in each half `t` and `ct`), but each player's combined stats for all maps are not saved, and they can be calculated from the individual maps. This was done to save space and make the data more readable.

Also, the data is not 100% clean, there may be some `\t` and `\n` characters in the data, but those are easily removed with some basic string manipulation once you load the data into a dataframe or similar.

## Contributing

If you want to contribute to the project, feel free to open an issue or a pull request. If you have any questions or comments, you can contact me at [my email](mailto:taavidev@gmail.com).

## License

This project is licensed under the MIT License - please credit me if you use the code or its output in your own project. And gimme stars, I like stars. 🌟
