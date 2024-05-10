## Prerequisites

Before you start, ensure you have the following set up in your development environment:

### Python Installation

- **Python Version**: Make sure Python is installed on your machine. Python 3.6 or newer is recommended.

### Create a Virtual Environment

For **Windows** users:

```bash
python -m venv venv
venv\Scripts\activate
```

For **macOS and Linux** users:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Necessary Libraries

Install Gradio, dotenv, and the OpenAI Python client using pip:

```bash
pip install gradio python-dotenv openai
```

### Setting Up Your Environment Variables

In your project's root directory, create a file named `.env`. Inside this file, you will add your OpenAI API key to
ensure secure access. Insert the following line in your `.env` file:

```plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

### Running the Chatbot
```bash
python app.py
```

## Blog

https://medium.com/@rohan-karan/build-chatbot-arena-using-gradio-a-step-by-step-guide-to-multi-model-chatbots-9d855f4ad650