from flask import Flask, render_template, request, flash
from github import Github
from dingdong import calculate_code_complexity_score
import tiktoken
import re


import os
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

secret_key = os.urandom(24).hex()
github_token = 'paste github api key'
max_tokens = 4000


app = Flask(__name__)
app.secret_key = secret_key

def calculate_average_complexity_score(output):
    # Extract numbers from the output string using regular expression
    complexity_scores = re.findall(r'\d+', output)

    # Convert the extracted numbers to a list of integers
    scores = list(map(int, complexity_scores))

    # Calculate the sum of complexity scores
    total_sum = sum(scores)

    # Calculate the average complexity score
    average = total_sum / len(scores)

    return average


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def truncate_file(file_path, max_tokens):
    with open(file_path, "r") as file:
        contents = file.read()

    # Truncate the tokens if it exceeds the maximum number of tokens
    truncated_contents = tiktoken.truncate(
        contents,
        max_tokens,
        truncation_strategy="longest_first",
        stride=0,
        num_subtokens_to_remove=0
    )

    return truncated_contents


# Function to perform chunking on a file
def chunk_file(file_path, chunk_size):
    chunks = []
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            chunks.append(data)
    return chunks

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_url = request.form.get('github_url')
        print("User URL:", user_url)
        try:
            g = Github()
            user = g.get_user(user_url)
            repositories = user.get_repos()

            repository_names = [repo.name for repo in repositories]
            print("Repository Names:", repository_names)
            partitioned_files = {}  # Dictionary to store partitioned files for each repository
            repository_scores = {}  # Dictionary to store repository complexity scores and explanations

            for repo_name in repository_names:
                repository = user.get_repo(repo_name)
                contents = repository.get_contents('')

                files = []  # List to store files for the current repository
                chunk = []  # List to store current chunk of files
                chunk_size = 0  # Current chunk size in bytes

                for content in contents:
                    if content.type == 'file':
                        file_size = content.size
                        if chunk_size + file_size > 4000:
                            # If adding the file exceeds the chunk size limit, start a new chunk
                            files.append(chunk)
                            chunk = []
                            chunk_size = 0

                        chunk.append({
                            'name': content.path,
                            'size': file_size
                        })
                        chunk_size += file_size
                        #print("Chunks:", chunk)
                        #print("Chunk size: ", chunk_size)
                    else:
                        print("Skipping content type:", content.type)


                if chunk:
                    files.append(chunk)
                    #print("files: ", files)  # Add the remaining files to the last chunk if any

                partitioned_files[repo_name] = files 
                #print("Part files: ", partitioned_files) # Add the partitioned files to the repository

                for chunk in files:
                    for file in chunk:
                        file_path = file['name'] 
                        file_contents = repository.get_contents(file_path).decoded_content.decode('utf-8')
                        print("File path: ", file_path) # Get the file path

                        num_tokens = num_tokens_from_string(file_contents, "cl100k_base")
                        #print(num_tokens)

                        if num_tokens > max_tokens:
                        # Truncate the tokens if it exceeds the maximum number of tokens
                            file_contents = truncate_file(file_path, max_tokens)
                            #print("Limited file contents:", file_contents)  # Print the limited file contents
                        #else:
                        # If the number of tokens is within the limit, use the original file contents
                            #print("File contents:", file_contents)

                        complexity_score = calculate_code_complexity_score(file_contents)
                        print( complexity_score)
                        #average_score = calculate_average_complexity_score(complexity_score)
                        repository_scores.setdefault(repo_name, []).append({'score': complexity_score})
            
            
                        #average_scores = calculate_average_complexity_score(complexity_score)

            return render_template('result.html', repositories=repository_names, partitioned_files=partitioned_files, repository_scores=repository_scores)
        except Exception as e:
            flash(str(e))
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)

