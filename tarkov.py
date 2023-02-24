import requests
import json


def request(item: str) -> dict:
    url = f"https://tarkov-market.com/api/v1/item?q={item}&"
    headers = {
        "x-api-key": "GmHPhQmFIn1UKUNA"
    }
    response = requests.get(url, headers=headers)

    data = json.loads(response.text)

    with open("answer.json", 'w') as file:
        json.dump(data, file, indent=4)

    data_dict = data[0]
    [data_dict.pop(key) for key in ["uid", "bannedOnFlea", "name", "tags", "basePrice", "traderPriceRub", "diff24h",
                                    "diff7days", "img", "imgBig", "bsgId", "link", "isFunctional", "reference"]]
    data_dict["Наличие на барахолке"] = data_dict.pop("haveMarketData")
    data_dict["Название"] = data_dict.pop("shortName")
    data_dict["Цена"] = data_dict.pop("price")
    data_dict["Средняя цена за день"] = data_dict.pop("avg24hPrice")
    data_dict["Средняя цена за неделю"] = data_dict.pop("avg7daysPrice")
    data_dict["Торговец"] = data_dict.pop("traderName")
    data_dict["Цена у торговца"] = data_dict.pop("traderPrice")
    data_dict["Валюта торговца"] = data_dict.pop("traderPriceCur")
    data_dict["Обновлена"] = data_dict.pop("updated")
    data_dict["Слоты"] = data_dict.pop("slots")
    data_dict[" "] = data_dict.pop("icon")
    data_dict["Wiki"] = data_dict.pop("wikiLink")
    return data_dict


if __name__ == '__main__':
    print("Ты хули тут забыл? ")
