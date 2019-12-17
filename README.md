# FS Webscrapper

## Table of Contents
* [What is it?](#what-is-it)
  - [Features](#features)
* [Usage](#usage)
  - [Development setup](#development-setup)
  - [Deployment](#deployment)
* [Architecture](#architecture)
  - [API](#api)

## What is it?
FS webscrapper is scrapper developed with the aim of retrieving information related to services and functionalities about NOS. It integrates a chat bot developed with the aim of improving the customer assistance provided by ISPs, NOS in this case, by aggregating most of their customer services in a single endpoint.

### Features
The API provided by this service allows:
* Retrieve service lines
* Retrieve avaiable phones
* Retrieve all 'WTF' tariffs available
* Retrieve all packages
* Retrieve 'NOS' store address


## Usage
#### Development Setup
* Install project dependencies:
`pip install -r requirements.txt --user`
* Run *Flask* project:
`python3 fs_scrapper.py`

### Deployment
* Build Docker image
`docker build -t fs_scrapper:latest .`
* Run Docker container
`docker run -p 5002:5002 -it fs_scrapper:latest`


## Architecture

### API
<details>
<summary>Retrieve service lines</summary>

```http
GET /fs_scrapper/linhas_apoio?assunto=<>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `assunto` | `string` | Optional. Specific matter |

Returns a list of json objects.

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve phones based on brand, if they are new, in promotion/discount, top most searched, come with an offer, can be payed by installment, can be payed with points and/or in a specified price range</summary>

```http
GET /fs_scrapper/phone_model/<model>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `brand` | `string` | Optional. Phone brand or model |
| `new` | `string` | Optional. Indication that are wanted new phones |
| `promo` | `string` | Optional. Indication that are wanted phones with a promotion/discount |
| `top` | `string` | Optional. Indication that are wanted the top most searched phones |
| `ofer` | `string` | Optional. Indication that are wanted phones that come with an offer |
| `prest` | `string` | Optional. Indication that are wanted phones which have installment payment available |
| `points` | `string` | Optional. Indication that are wanted phones which have points payment available |
| `min` | `float` | Optional. Lowest value of price |
| `max` | `float` | Optional. Highest value of price |

***Note**: All parameters are optional, but if phones are wanted in a price range both min and max are needed.

Returns a list of json objects.

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve 'WTF' tariffs available</summary>

```http
GET /fs_scrapper/all_wtf
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | Optional. Tariff name |

Returns a list of json objects.

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve the stores available at specified region or coordinates</summary>

```http
GET /fs_scrapper/stores_zone/<zone>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `zone` | `string` | Optional. Zone query |
| `lat` | `float` | Optional. Latitude value |
| `lon` | `float` | Optional. Longitude value |

***Note**: Parameters are optional, but a zone or lat and lon are needed. When values are given to lat and lon the returned stores are in a maximum distance of 20 km.

Returns a list of json objects.

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve packages based on name, type, service and/or a specified price range</summary>

```http
GET /fs_scrapper/packages
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `type` | `string` | Optional. Type of package wanted (satelite or fiber) |
| `service` | `string` | Optional. Service wanted |
| `min` | `float` | Optional. Lower value of price |
| `max` | `float` | Optional. Highest value of price |
| `name` | `string` | Optional. Package name |

***Note**: All parameters are optional, but if phones are wanted in a price range both min and max are needed.

Returns a list of json objects.

------
</details>
