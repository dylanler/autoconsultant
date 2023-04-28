# Auto Consultant

Auto Consultant is an app that returns a competitor analysis, business plan, and location recommendation for your product. It combines the power of Gradio, Google Maps API, and OpenAI's GPT-3.5-turbo model to provide you with valuable insights and recommendations.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Requirements
- Python 3.6 or higher
- Gradio
- OpenAI
- requests

## Installation

1. Install the required Python packages:

```bash
pip install gradio openai requests
```

2. Save the provided code in a file named auto_consultant.py.

## Usage

1. Set the following environment variables:

```bash
export OPENAI_API_KEY="your_openai_api_key"
export GOOGLE_MAPS_API="your_google_maps_api_key"
```

2. Run the app:

```bash
python auto_consultant.py
```

3. Open a web browser and navigate to the URL displayed in the terminal (e.g., http://127.0.0.1:7860/).

4. Enter the product you want to sell and the location you are considering in the textboxes provided.

5. The app will return a competitor analysis, business plan, and location recommendation based on your input.

## Configuration

To modify the default settings, you can update the following variables in the auto_consultant.py file:

- OPENAI_API_KEY: Your OpenAI API key (provided as an environment variable)
- GOOGLE_MAPS_API: Your Google Maps API key (provided as an environment variable)
- radius: The search radius for finding competitors (default: 10000 meters, i.e., 10 km)

