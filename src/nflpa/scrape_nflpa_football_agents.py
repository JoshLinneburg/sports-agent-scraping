#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from nflpa_tools import BASE_URL, scrape_main_table, gather_page_urls


def main():
    data = []

    try:

        page_urls = gather_page_urls(
            f"{BASE_URL}/search/agents?page=1", [f"{BASE_URL}/search/agents?page=1"]
        )

        print(f"Found {len(page_urls)} pages of agents to scrape!")

        for page_url in page_urls:
            page_data = scrape_main_table(page_url=page_url)
            data = data + page_data

        with open("../../data/nfl_agents.json", "w") as f:
            json.dump(data, f, ensure_ascii=True, indent=4)

        df = pd.json_normalize(data)
        df.to_csv("../../data/nfl_agents.csv", index=False)

    except:
        raise


if __name__ == "__main__":
    main()
