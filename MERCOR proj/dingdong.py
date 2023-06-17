import openai


openai.api_key = "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"  # Replace with your actual API key



def generate_completion(code_contents):
    messages = [
        {"role": "system", "content": "You are a code complexity score calculator, Just give me a number 1-10. and give very short explanation for the number, in the format Complexity score: and next line Explanation: "},
        {"role": "user", "content": code_contents},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        max_tokens=16000,
        messages=messages,
    )

    return response.choices[0].message["content"]

def calculate_code_complexity_score(code_contents):
    
    completion = generate_completion(code_contents)
    return completion



    
    

