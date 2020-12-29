#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs

BASE_URL = "https://nflpa.com"


def scrape_agent_page(agent_page_url):
    try:

        print(f"Scraping additional data for {agent_page_url}...")

        response = requests.get(url=f"{BASE_URL}{agent_page_url}")

        if response.status_code < 400:
            agent_html = bs(response.text, features="html.parser")
        else:
            response.raise_for_status()
            raise

        top_half_html = agent_html.findAll("div", class_="profile__content")[0]
        bot_half_html = agent_html.findAll("div", class_="profile__content")[1]

        try:
            certified = top_half_html.find(
                "div", class_="flex items-center"
            ).text.strip()
        except AttributeError:
            certified = None

        try:
            detailed_address = (
                top_half_html.find("ul", "profile__icon-list mt-4")
                .findAll("li")[0]
                .text.replace("  ", "")
                .replace("\n\n", " ")
                .replace("\n", " ")
                .strip()
            )
        except (AttributeError, IndexError):
            detailed_address = None

        try:
            phone_nbr = (
                top_half_html.find("ul", "profile__icon-list mt-4")
                .findAll("li")[1]
                .text.replace("  ", "")
                .replace("\n\n", " ")
                .replace("\n", " ")
                .strip(),
            )
        except (AttributeError, IndexError):
            phone_nbr = None

        try:
            services = [
                item.text.strip()
                for item in bot_half_html.find(
                    "div", class_="profile__section"
                ).findAll("li")
            ]
        except AttributeError:
            services = None

        try:
            other_contact = [
                item.find("a")["href"]
                for item in bot_half_html.find(
                    "ul", class_="profile__icon-list"
                ).findAll("li")
            ]
        except AttributeError:
            other_contact = None

        try:
            education = [
                item.text.replace("  ", "")
                .replace("\n\n", " ")
                .replace("\n", " ")
                .strip()
                for item in bot_half_html.findAll("div", class_="flex")
            ]
        except AttributeError:
            education = None

        extras_obj = {
            "certified": certified,
            "detailed_address": detailed_address,
            "phone_nbr": phone_nbr,
            "services": services,
            "other_contact": other_contact,
            "education": education,
        }

        return extras_obj

    except:
        raise


def scrape_table_row(table_row):
    cols = table_row.findAll("td")

    row_obj = {
        "name": cols[0].text.strip(),
        "company": cols[1].text.strip(),
        "company_address": cols[2].text.strip(),
        "url": cols[0].find("a")["href"],
        "additional_data": scrape_agent_page(cols[0].find("a")["href"]),
    }

    return row_obj


def scrape_main_table(page_url):
    print(f"Finding agents on {page_url}...")

    try:
        response = requests.get(url=page_url)

        if response.status_code < 400:
            first_page_html = bs(response.text, features="html.parser")
        else:
            response.raise_for_status()
            raise

        html_table = first_page_html.find(
            "table", class_="search-results results-table"
        )

        data = []

        print(f"Found {len(html_table.findAll('tr')[1:])} agents to scrape!")

        for row in html_table.findAll("tr")[1:]:
            row_data = scrape_table_row(row)

            data.append(row_data)

        return data

    except:
        raise


def gather_page_urls(page_url, page_url_list):
    try:

        response = requests.get(url=page_url)

        if response.status_code < 400:
            page_html = bs(response.text, features="html.parser")
        else:
            response.raise_for_status()
            raise

        for url in page_html.find("div", class_="pagination__pages").findAll("a"):
            if (
                url["href"] != "https://nflpa.com/search/agents"
                and url["href"] not in page_url_list
            ):
                page_url_list.append(url["href"])
                gather_page_urls(page_url=url["href"], page_url_list=page_url_list)

        return page_url_list

    except:
        raise
