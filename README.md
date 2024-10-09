# Stream Community Products

Crawl product listings from the streamcommunity.com website.


### How to build the the repo in docker and run it

Build the image using below command:

```
docker build -t stream-crawler:latest .
```

Then, simply run the container with:

```
docker run -p 8000:8000 stream-crawler:latest
```

### Check the endpoints and test them

After you have built and run your docker, go to http://127.0.0.1:8000/docs to check the swagger interface and test the endpoints. For example, you can run the `GET` endpoint with number of pages you want to crawl and and you will get list of products in json format for specified pages.

## How to build and run this repo in dev environment using uvicorn:

One time setup:
```
Go to project directory and run below commands -

conda create -n stream-crawler-venv
conda activate stream-crawler-venv
conda install -c conda-forge uvicorn
conda install pip
pip install pytest
pip install -r requirements.txt
export PYTHONPATH=/root/../../stream-marketplace-crawler <- Path to the project directory
conda deactivate
```

Run the project in dev environment -
```
cd project_dir/app
conda activate stream-crawler-venv
uvicorn main:app --reload --port 8020
Access the Endpoints at http://127.0.0.1:8020/docs
conda deactivate
```

## Testing

### Unit tests

Run below command from the root folder to run the test cases:

```
pytest -rA .
```

## Test Results

Sample Curl Request
```
curl -X 'GET' \
  'http://127.0.0.1:8000/get_products?page_limit=2' \
  -H 'accept: application/json'
```
Sample Response
```
{
  "product_list": [
    {
      "name": "Plinknana",
      "app_name": "Banana",
      "buy_price": "$0.04",
      "sell_price": "$0.05",
      "sell_offers": 79083,
      "marketable": true
    },
    {
      "name": "Dreams & Nightmares Case",
      "app_name": "Counter-Strike 2",
      "buy_price": "$1.38",
      "sell_price": "$1.44",
      "sell_offers": 40724,
      "marketable": true
    },
    {
      "name": "Kilowatt Case",
      "app_name": "Counter-Strike 2",
      "buy_price": "$0.86",
      "sell_price": "$0.89",
      "sell_offers": 109987,
      "marketable": true
    },
    {
      "name": "Gamma 2 Case",
      "app_name": "Counter-Strike 2",
      "buy_price": "$2.97",
      "sell_price": "$3.10",
      "sell_offers": 18084,
      "marketable": true
    },
    .........
  ]
}
```