# Workout Prediction Backend

A backend service that predicts calories burned during a workout using a machine learning model trained on gym exercise data. Built as a group project by [Name 1], [Name 2], [Name 3], and [Name 4].

## What it does

The service takes in workout and user details (things like age, weight, duration, heart rate) and returns a predicted calorie burn, based on a model trained on gym member exercise data.

## Project structure
├── app/                                   # Backend application code
├── calories prediction model.ipynb        # Notebook used to train/explore the model
├── Calorie model.joblib                   # Saved trained model
├── Final_data.csv                         # Cleaned dataset used for training
├── gym_members_exercise_tracking.csv      # Raw source dataset
└── requirements.txt                       # Python dependencies

## Tech stack

- Python
- [Flask / FastAPI — fill in whichever the `app` folder uses]
- scikit-learn (model training and inference)
- pandas / numpy (data handling)

## Getting started

### Prerequisites

- Python 3.x
- pip

### Setup

```bash
git clone https://github.com/anunandy123/WorkoutPredictionBackend.git
cd WorkoutPredictionBackend
pip install -r requirements.txt
```

### Running the server

```bash
[python app/main.py — replace with actual entry point]
```

The API will be available at `http://localhost:[port]`.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict` | Takes workout details, returns predicted calories burned |

Example request:

```json
{
  "age": 25,
  "weight": 70,
  "duration": 45,
  "heart_rate": 130
}
```

*(Replace this with the actual request/response shape once confirmed.)*

## Model

The prediction model was trained in `calories prediction model.ipynb` on `Final_data.csv`, which was derived from `gym_members_exercise_tracking.csv`. The trained model is saved as `Calorie model.joblib` and loaded by the backend at runtime.

## Team

- Baisakhi Nandi — [role, e.g. model training]
- Syed Md. Farhan E Azam — [role, e.g. API development]
- Soumik Mondal — [role, e.g. data cleaning]
- Anuska Nandy — [role, e.g. deployment/testing]

