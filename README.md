## Github-Automated-Analysis

This repository contains the code for the GitHub Analysis website, which utilizes the GitHub API and GPT-3.5 for analyzing code complexity. This README file provides instructions for running the code locally and an overview of how the code works.

### Installation

To run the GitHub Analysis website, you need to install the following dependencies:

- Python 3.x
- Flask
- PyGithub
- tiktoken
- OpenAI GPT-3.5 API (you will need an API key)

You can install these dependencies by running the following command:

```shell
pip install flask pygithub tiktoken openai
```

### Running the Code Locally

To run the GitHub Analysis website locally, follow these steps:

1. Clone this repository to your local machine.
2. Set up your OpenAI GPT-3.5 API key by following the OpenAI API documentation.
3. Open the `app.py` file and replace the `github_token` variable with your own GitHub API token.
4. Run the following command to start the Flask server:

```shell
python app.py
```

5. Open your web browser and visit `http://localhost:5000` to access the GitHub Analysis website.

### Files and Functionality

The GitHub Analysis website allows users to enter a GitHub repository URL and analyze the complexity of the code files in that repository. Here's an overview of how the code works:

- The `app.py` file contains the Flask application that handles the web interface and API requests. It uses the `Github` class from the `pygithub` library to interact with the GitHub API and retrieve repository information.
- The `result.html` file is the HTML template used to display the analysis results.
- The `dingdong.py` file contains the function `calculate_code_complexity_score`, which uses the OpenAI GPT-3.5 API to calculate the complexity score of code snippets.
- Memory management is performed by chunking large files into smaller chunks with a maximum size of 4000 tokens. The `chunk_file` function in `app.py` handles the chunking process.
- The code snippets are sent to the GPT-3.5 model using prompt engineering techniques to generate complexity scores for each code snippet.
- The complexity scores are then displayed on the web interface along with relevant repository, file, and file size information.

### Contact

If you have any questions or need further assistance, please feel free to reach out to me. I'm more than happy to help!

Sobika Sree Ramesh
sobikasreeramesh@gmail.com
