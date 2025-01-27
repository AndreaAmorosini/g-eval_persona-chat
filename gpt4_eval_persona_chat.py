from openai import AzureOpenAI
import json
from tqdm import tqdm
import time

client = AzureOpenAI(
    azure_endpoint="endpoint",
    api_version="2024-10-21",
    api_key="API_KEY",
)


# Load dataset
def load_dataset(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


# Format a prompt for GPT-4 evaluation
def format_prompt(context, response):
    return f"""
    You will be given a conversation between two individuals. You will then be given one potential
    response for the next turn in the conversation. 
    
    Your task is to rate the overall quality of the response.
    Please make sure you read and understand these instructions carefully. Please keep this
    document open while reviewing, and refer to it as needed.
    
    **Evaluation Criteria:**
    
    Overall Quality (1-3): Is the overall quality of the response satisfactory?
    
    - **Score 1 (Unsatisfactory):** The response is not aligned with the conversation's tone, context, or intent. It may contain irrelevant or incoherent content, leading to confusion or a breakdown in the flow of the conversation.
    - **Score 2 (Satisfactory):** The response is mostly appropriate, maintaining a reasonable level of coherence and relevance to the conversation. It may have minor issues, such as slightly awkward phrasing, missing some context, or lacking in engagement, but it still contributes to the flow.
    - **Score 3 (Excellent):** The response is highly relevant, engaging, and maintains a natural flow in the conversation. It addresses the topic clearly and concisely while enhancing the overall interaction. There are no significant issues with tone or content.
    
    **Evaluation Steps:**
    1. Read the conversation and the response carefully.
    2. Rate the response on a scale of 1-3 for overall quality, according to the criteria above.
    3. Provide a brief explanation for your rating, referring to specific aspects of the response and
       the conversation.
    
    **Conversation:**
    {context.strip()}
    
    **Response:**
    {response.strip()}
    
    **Evaluation Form:**
    - Overall Quality:
    """


# Call Azure OpenAI to evaluate a response
def evaluate_response(prompt):
    ignore = 0
    try:
        response = client.chat.completions.create(
            model="gpt-4-32k",  # Replace with your GPT-4 deployment name
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that evaluates dialogue quality.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=100,
            top_p=1,
            frequency_penalty = 0,
            presence_penalty = 0,
            stop=None,
            n = 20
        )
        time.sleep(0.5)
        
        all_responses = [response.choices[i].message.content for i in range(len(response.choices))]
        return all_responses

        # return response.choices[0].message.content
    except Exception as e:
        print(e)
        if "limit" in str(e):
            time.sleep(2)
        else:
            ignore += 1
            print("ignored", ignore)


# Process dataset
def process_dataset(dataset):
    results = []
    with tqdm(total=len(dataset), desc="Processing Dataset") as pbar_main:
        for entry in dataset:
            context = entry["context"]
            responses = entry["responses"]
            with tqdm(total=len(responses), desc="Processing Responses", leave=False) as pbar_sub:
                for response_data in responses:
                    response = response_data["response"]
                    model = response_data["model"]
                    prompt = format_prompt(context, response)
                    evaluations = evaluate_response(prompt)
                    results.append(
                        {
                            "context": context,
                            "response": response,
                            "model": model,
                            "evaluation": evaluations,
                        }
                    )
                    pbar_sub.update(1)
                    # time.sleep(0.5)
            pbar_main.update(1)
    return results


# Save results to JSON
def save_results(results, output_file):
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

def aggregate_results(results):
    aggregated = {}
    for result in results:
        context = result["context"]
        if context not in aggregated:
            aggregated[context] = []
        aggregated[context].append({
            "response": result["response"],
            "model": result["model"],
            "evaluation": result["evaluation"],
        })
    return aggregated


# Main script
if __name__ == "__main__":
    # dataset_file = "pc_usr_data.json"  # Path to your dataset
    dataset_file = "test_data.json"
    output_file = "evaluations.json"  # Output file for evaluations

    print("Loading dataset...")
    dataset = load_dataset(dataset_file)

    print("Processing dataset...")
    evaluations = process_dataset(dataset)

    print("Aggregating results...")
    aggregated_results = aggregate_results(evaluations)

    print("Saving results...")
    save_results(aggregated_results, output_file)

    print(f"Evaluations saved to {output_file}")
