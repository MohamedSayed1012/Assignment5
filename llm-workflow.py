import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the model server type (defaults to GROQ)
model_server = os.getenv('MODEL_SERVER', 'GROQ').upper()

if model_server == "GROQ":
    API_KEY = os.getenv('GROQ_API_KEY')
    BASE_URL = os.getenv('GROQ_BASE_URL')
    LLM_MODEL = os.getenv('GROQ_MODEL')
elif model_server == "OPENAI":
    API_KEY = os.getenv('OPENAI_API_KEY')
    BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    LLM_MODEL = os.getenv('OPENAI_MODEL')
else:
    raise ValueError(f"Unsupported MODEL_SERVER: {model_server}")

# Initialize OpenAI (or Groq) client
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Function to call the LLM API
def call_llm(messages, tools=None, tool_choice=None):
    kwargs = {
        "model": LLM_MODEL,
        "messages": messages,
    }
    if tools:
        kwargs["tools"] = tools
    if tool_choice:
        kwargs["tool_choice"] = tool_choice
    try:
        response = client.chat.completions.create(**kwargs)
        return response
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        return None

# Define tool schemas
extract_key_points_schema = {
    "type": "function",
    "function": {
        "name": "extract_key_points",
        "description": "Extract key points from a blog post",
        "parameters": {
            "type": "object",
            "properties": {
                "key_points": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of key points extracted from the blog post"
                }
            },
            "required": ["key_points"]
        }
    }
}

generate_summary_schema = {
    "type": "function",
    "function": {
        "name": "generate_summary",
        "description": "Generate a concise summary",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"}
            },
            "required": ["summary"]
        }
    }
}

# Corrected function to extract key points
def task_extract_key_points(blog_post):
    messages = [
        {"role": "system", "content": "You are an expert at analyzing content and extracting key points from articles."},
        {"role": "user", "content": f"Extract the key points from this blog post:\n\nTitle: {blog_post['title']}\n\nContent: {blog_post['content']}"}
    ]

    response = call_llm(messages, tools=[extract_key_points_schema], tool_choice={"type": "function", "function": {"name": "extract_key_points"}})

    if response and response.choices and hasattr(response.choices[0].message, "tool_calls"):
        tool_call = response.choices[0].message.tool_calls[0]
        result = json.loads(tool_call.function.arguments)
        return result.get("key_points", [])

    return []  # Fallback if tool calling fails

# Corrected function to generate summary
def task_generate_summary(key_points):
    messages = [
        {"role": "system", "content": "You are an expert at summarizing content concisely while preserving key information."},
        {"role": "user", "content": f"Generate a summary based on these key points:\n\n" + "\n".join([f"- {point}" for point in key_points])}
    ]

    response = call_llm(messages, tools=[generate_summary_schema], tool_choice={"type": "function", "function": {"name": "generate_summary"}})

    if response and response.choices and hasattr(response.choices[0].message, "tool_calls"):
        tool_call = response.choices[0].message.tool_calls[0]
        result = json.loads(tool_call.function.arguments)
        return result.get("summary", "")

    return ""  # Fallback if tool calling fails

# Simple pipeline workflow
def run_pipeline_workflow(blog_post):
    key_points = task_extract_key_points(blog_post)
    summary = task_generate_summary(key_points)
    return {
        "key_points": key_points,
        "summary": summary
    }

# Load the sample blog post
def get_sample_blog_post():
    try:
        with open('sample-blog-post.json', 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: sample-blog-post.json file not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in sample-blog-post.json.")
        return None

# Run the workflow
if __name__ == "__main__":
    blog_post = get_sample_blog_post()
    if blog_post:
        print("\n=== Pipeline Workflow ===")
        pipeline_results = run_pipeline_workflow(blog_post)
        print(json.dumps(pipeline_results, indent=2))
