#!/usr/bin/env python
# coding: utf-8

import json
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

        json.dump(data=data, fp="../nfl_agents.json", ensure_ascii=True, indent=4)

    except:
        raise


if __name__ == "__main__":
    main()
