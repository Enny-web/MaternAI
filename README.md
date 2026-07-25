# MaternAI

MaternAI is an AI-powered maternal health risk prediction web application built with Streamlit. It combines a machine learning model with a generative AI assistant to provide maternal health risk predictions alongside easy-to-understand explanations.

## Features

- Predicts maternal health risk (Low, Mid, or High Risk)
- Interactive web interface built with Streamlit
- AI-generated explanation of prediction results
- Patient summary table
- Responsive and user-friendly interface
- Educational medical disclaimer

## Technologies Used

- Python
- Streamlit
- XGBoost
- Pandas
- Joblib
- OpenRouter API (LLM)
- OpenAI Python SDK

## Project Structure

```
MaternAI/
│── MaternAI.py
│── maternal_health_model.pkl
│── label_encoder.pkl
│── image.jpg
│── requirements.txt
│── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/MaternAI.git
cd MaternAI
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run MaternAI.py
```

## Usage

1. Enter the patient's clinical measurements.
2. Click **Predict Risk**.
3. View the predicted maternal health risk.
4. Read the AI-generated explanation and recommendations.

## Disclaimer

This application is intended for educational and research purposes only. It does not provide medical diagnoses and should not replace professional medical advice or clinical judgment.

## Author

**Eniola Adetunji**
