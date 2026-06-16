# Customer Product Review Sentiment Analyzer

Created by Rahul Roy. Project started on June 12, 2026.

Enterprise-inspired local review analyzer for customer product reviews. The app uses the Amazon `Reviews.csv` dataset and provides sentiment prediction, fake/spam risk checks, aspect mining, product analytics, user credibility scoring, and a dashboard/API.

## Dataset

Put the review CSV here:

```text
data/raw/amazon_reviews/Reviews.csv
```

Optional Flipkart dataset is also supported here:

```text
data/raw/flipkart_reviews/Dataset-SA.csv
```

Expected columns:

```text
Id, ProductId, UserId, ProfileName, HelpfulnessNumerator,
HelpfulnessDenominator, Score, Time, Summary, Text
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Prepare Data

```powershell
python scripts/prepare_data.py --max-rows 120000
```

This writes cleaned review data and user/product aggregates to `data/processed/`. If `Dataset-SA.csv` exists in the Flipkart folder, it is merged into the cleaned training data automatically.

## Train

```powershell
python train.py --max-rows 120000
```

This trains a TF-IDF + Logistic Regression sentiment model and saves it in `data/models/sentiment/`.

## Run API and Dashboard

```powershell
python run_api.py
```

Open:

- Dashboard: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

## Useful API Tests

Positive review:

```json
{
  "review_id": "manual-1",
  "product_id": "PROD_1",
  "user_id": "USER_1",
  "rating": 5,
  "summary": "Excellent product",
  "text": "The taste is excellent, delivery was fast, packaging was clean, and I would buy this again."
}
```

Suspicious spam/fake review:

```json
{
  "review_id": "manual-2",
  "product_id": "PROD_2",
  "user_id": "NEW_USER",
  "rating": 5,
  "summary": "Best product ever",
  "text": "Amazing amazing amazing buy now http://promo.example.com free discount offer best best best"
}
```

## Full Fresh-Clone Run

```powershell
cd Customer_product_review_sentiment_analyzer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `Reviews.csv` into `data/raw/amazon_reviews/Reviews.csv`, then run:

```powershell
python scripts/prepare_data.py --max-rows 120000
python train.py --max-rows 120000
python -m pytest -q
python run_api.py
```

## Notes

In this project I intentionally uses a practical lightweight local stack instead of massive transformer models, so it runs on a normal laptop. The modules are structured so heavier models can be swapped in later.
