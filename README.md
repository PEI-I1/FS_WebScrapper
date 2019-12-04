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
`export FLASK_APP=fs_scrapper.py && flask run`

### Deployment
* Build Docker image
`docker build -t fs_scrapper:latest .`
* Run Docker container
`docker run -it --rm --network host fs_scrapper:latest`


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
<summary>Retrieve the specified model</summary>

```http
GET /fs_scrapper/phone_model/<model>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `model` | `string` | Required. Phone model |

------
</details>

<!---------------------------------------------------->
<details>
<summary>Retrieve all phones of specified brand</summary>

```http
GET /fs_scrapper/brand_phones/<brand>
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `brand` | `string` | Required. Phone brand |

------

</details>

<!---------------------------------------------------->

<details>
<summary>Retrive the top most shearched/viewed phones</summary>

```http
GET /fs_scrapper/top_phones
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all phones who are currently under a discount/promotion</summary>

```http
GET /fs_scrapper/promo_phones
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve the most recents phones</summary>

```http
GET /fs_scrapper/new_phones
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all the phones in which it comes with an offer</summary>

```http
GET /fs_scrapper/ofer_phones
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all phones which have installment payment available</summary>

```http
GET /fs_scrapper/prest_phones
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all phones which have points payment available</summary>

```http
GET /fs_scrapper/points_phones
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all phones which are in specified threshold of price</summary>

```http
GET /fs_scrapper/phones_price/<float:min>/<float:max>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `min` | `float` | Required. Lower value of price. |
| `max` | `float` | Required. Highest value of price. |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all phones of specified brand which are in specified threshold of price</summary>

```http
GET /fs_scrapper/phones_brand_price/<brand>/<float:min>/<float:max>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `brand` | `string` | Required. Phone brand |
| `min` | `float` | Required. Lower value of price. |
| `max` | `float` | Required. Highest value of price. |
------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all phones of specified brand which are currentelly under a discount/promotion</summary>

```http
GET /fs_scrapper/phones_brand_promo/<brand>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `brand` | `string` | Required. Phone brand |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all phones between a specified threshold of price which are currently under a discount/promotion</summary>

```http
GET /fs_scrapper/phones_promo_price/<float:min>/<float:max>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `min` | `float` | Required. Lower value of price. |
| `max` | `float` | Required. Highest value of price. |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve the most recents phones of specified brand</summary>

```http
GET /fs_scrapper/new_phones_brand/<brand>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `brand` | `string` | Required. Phone brand |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all 'WTF' tariffs available</summary>

```http
GET /fs_scrapper/all_wtf
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve information of specified tariff</summary>

```http
GET /fs_scrapper/wtf_name/<name>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | Required. Tariff name. |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve the stores available at specified region</summary>

```http
GET /fs_scrapper/stores_zone/<zone>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `zone` | `string` | Required. Zone query. |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrive information õf specified store with its address</summary>

```http
GET /fs_scrapper/store_address/<address>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `address` | `string` | Required. Store address. |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve package of certain type and specific name</summary>

```http
GET /fs_scrapper/specific_package/<tipo>/<nome>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `tipo` | `string` | Required. Type of package wanted. |
| `nome` | `string` | Required. Package name. |
------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all packages available</summary>

```http
GET /fs_scrapper/packages
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all packages of type 'Fibra'</summary>

```http
GET /fs_scrapper/fiber_packages
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all packages of type 'Satélite'</summary>

```http
GET /fs_scrapper/satelite_packages
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieve all packages with specified service</summary>

```http
GET /fs_scrapper/packages_service/<servico>
```

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieves all available packages that are within a specified price threshold</summary>

```http
GET /fs_scrapper/packages_price/<float:min>/<float:max>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `min` | `float` | Required. Lower value of price. |
| `max` | `float` | Required. Highest value of price. |
------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieves packages of a specific service that are within a specified price threshold</summary>

```http
GET /fs_scrapper/packages_service_price/<service>/<float:min>/<float:max>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `service` | `string` | Required. Service wanted. |
| `min` | `float` | Required. Lower value of price. |
| `max` | `float` | Required. Highest value of price. |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieves packages of type 'Fibra' that are within a specified price threshold</summary>

```http
GET /fs_scrapper/fiber_packages_price/<float:min>/<float:max>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `min` | `float` | Required. Lower value of price. |
| `max` | `float` | Required. Highest value of price. |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieves packages of type 'Satélite' that are within a specified price threshold</summary>

```http
GET /fs_scrapper/satelite_packages_price/<float:min>/<float:max>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `min` | `float` | Required. Lower value of price. |
| `max` | `float` | Required. Highest value of price. |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieves packages of type 'Fibra' that have the specified service</summary>

```http
GET /fs_scrapper/fiber_packages_service/<servico>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `servico` | `string` | Required. Service wanted. |

------
</details>

<!---------------------------------------------------->

<details>
<summary>Retrieves packages of type 'Fibra' that have the specified service</summary>

```http
GET /fs_scrapper/satelite_packages_service/<servico>
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `servico` | `string` | Required. Service wanted. |

------
</details>
