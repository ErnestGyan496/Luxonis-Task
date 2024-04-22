import requests
import pandas as pd
import psycopg2
from psycopg2 import extras


def extractData():
    Flat_Name = []
    Flat_Location = []
    Flat_Price = []
    Flat_image_urls = []

    for i in range(1, 26):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cookie": 'szncmpone=1; udid=0W4zNRgusOj6YIibv45Zz4AQWj5AQkXN@1712326518161@1712326518161; per_page=20; cmpreferrer=https://www.sreality.cz/en/search/for-sale/apartments?_escaped_fragment_=; euconsent-v2=CP8mHYAP8mHYAD3ACBENAwEsAP_gAEPgAATIJVwQgAAwAKAAsACAAFQALgAZAA6ACAAFAAKgAWgAyABoADmAIgAigBHACSAEwAJwAVQAtgBfgDCAMUAgACEgEQARQAjoBOAE6AL4AaQA4gB3ADxAH6AQgAkwBOACegFIAKyAWYAuoBgQDTgG0APkAjUBHQCaQE2gJ0AVIAtQBbgC8wGMgMkAZcA0oBqYDugHfgQHAhcBGYCTQEqwQugRQAKAAsACoAFwAQAAyABoAEQAI4ATAAqgBiAD8AISARABEgCOAE4AMsAZoA7gB-gEIAIsAXUA2gCbQFSALUAW4AvMBggDJAGXANTAhcAA.YAAAAAAAAAAA; __gfp_64b=vYKwC7UrE3i4PVKdiHJVWU9Y9D1n_3BsEpEk1QsffgL.W7|1712326523; __cw_snc=1; sid=id=4594942427005925625|t=1704378169.655|te=1713154354.893|c=093734C347BD552B5974D2C155B200EF; cookie-wall-enabled=1; szncsr=1713156831; lastsrch="{\\"category_main_cb\\": \\"1\\"\\054 \\"per_page\\": \\"20\\"\\054 \\"tms\\": \\"1713156863975\\"\\054 \\"category_type_cb\\": \\"1\\"\\054 \\"page\\": \\"2\\"}"; lps=eyJfZnJlc2giOmZhbHNlLCJfcGVybWFuZW50Ijp0cnVlfQ.ZhyzBw.tHW9vXxcuZbOSHbDUYSO-maaciI',
            "referer": "https://www.sreality.cz/en/search/for-sale/apartments",
            "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }

        params = {
            "category_main_cb": "1",
            "category_type_cb": "1",
            "page": str(i),
            "per_page": "20",
            "tms": "1713187085062",
        }

        response = requests.get(
            "https://www.sreality.cz/api/en/v2/estates", headers=headers, params=params
        )
        print("The request response is ", {response.status_code})

        # results_json = response.json()

        for key, flat in enumerate(results_json["_embedded"]["estates"]):
            flat = []

            try:
                Flat_Name.append(
                    results_json["_embedded"]["estates"][key]["name"].replace(
                        "For sale apartment", ""
                    )
                )
            except:
                Flat_Name.append("")

            try:
                Flat_Location.append(
                    results_json["_embedded"]["estates"][key]["locality"]
                )
            except:
                Flat_Location.append("")

            try:
                Flat_Price.append(results_json["_embedded"]["estates"][key]["price"])
            except:
                Flat_Price.append("")

            try:
                Flat_image_urls.append(
                    results_json["_embedded"]["estates"][key]["_links"]["images"][0]
                )
            except:
                Flat_image_urls.append("")

            image_url = [link["href"] for link in Flat_image_urls]

    data = {
        "Flat_Name": Flat_Name,
        "Flat_Location": Flat_Location,
        "Flat_Price": Flat_Price,
        "Flat_image_url": image_url,
    }
    df = pd.DataFrame(data)
    df.to_csv("output1.csv", index=False)


def readData(data_):
    data = pd.read_csv(data_)
    data.reset_index(drop=True, inplace=True)
    # data=data.drop('Unnamed: 0', axis=1)
    print(data)


# Connection to the postgre Database
def getConnection():
    conn = psycopg2.connect(
        database="SRflats",
        user="postgres",
        password="Jan0247722623@",
        host="localhost",
        port="5432",
    )
    cur = conn.cursor()
    conn.autocommit = True
    return conn, cur


def create_flat_details(cursor):
    cursor.execute(
        """
                DROP TABLE IF EXISTS SReality_flats CASCADE; CREATE 
                UNLOGGED TABLE SReality_flats(
                    Flat_Name    TEXT,
                    Flat_Location    TEXT,
                    Flat_Price   NUMERIC,
                    Flat_image_url TEXT
                );
                
                """
    )


def schema_creation(conn, cursor):
    create_flat_details(cursor)


def send_csv_to_psql(connection, csv, table_):
    sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ',' "
    with open(csv, "r") as file:
        table = table_
        with connection.cursor() as cur:
            cur.execute("TRUNCATE TABLE " + table + ";")
            cur.copy_expert(sql=sql % table, file=file)
    connection.commit()


if __name__ == "__main__":
    df = "output1.csv"
    extractData()
    readData(df)
    conn, cursor = getConnection()
    schema_creation(conn, cursor)
    send_csv_to_psql(conn, "output1.csv", "SReality_flats")
    # conn.close()
