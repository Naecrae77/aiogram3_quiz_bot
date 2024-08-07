
# aiogram3_quiz_bot

This repository contains a Telegram bot built using the `aiogram` library (version 3). The bot is designed to conduct quizzes and can be deployed on the Railway platform.

## Features

- **Quiz Functionality**: The bot can conduct quizzes with multiple questions.
- **User Interaction**: Users can start the quiz, answer questions, and receive feedback.
- **Asynchronous**: Utilizes asynchronous programming for efficient handling of multiple users.

## Requirements

- Python 3.7+
- `aiogram` library
- `python-dotenv` for environment variable management

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Naecrae77/aiogram3_quiz_bot.git
    cd aiogram3_quiz_bot
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the root directory of the project.
    - Add your Telegram bot token to the `.env` file:
      ```
      API_KEY=your_telegram_bot_token
      ```

## Usage

1. **Run the bot**:
    ```bash
    python main.py
    ```

2. **Interact with the bot**:
    - Open Telegram and search for your bot.
    - Start a conversation and follow the prompts to participate in the quiz.

## Deployment on Railway

1. **Fork the repository** to your GitHub account.

2. **Create a new project** on [Railway](https://railway.app/).

3. **Connect your GitHub repository** to the Railway project.

4. **Set environment variables** on Railway:
    - Go to the project settings on Railway.
    - Add the `API_KEY` or in my case `keys` environment variable with your Telegram bot token.

5. **Deploy the project**:
    - Railway will automatically detect the project and deploy it.

## Project Structure

```
aiogram3_quiz_bot/
│
├── main.py              # Main bot script
│   ├── __init__.py
|── functions.py        # Module containing handlers and defined functions
|── quiz_data.py        # Module containing quiz questions
├── .env                # Environment variables file
├── requirements.txt    # List of dependencies
├── Procfile            # Directory for Railway to initialize the bot
└── README.md           # Project README file
```
