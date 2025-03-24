# LLM Workflow

A Python implementation for extracting key points and generating summaries from blog posts using Large Language Models, with support for multiple LLM providers (OpenAI and Groq).

## Overview

This project demonstrates how to use LLM APIs for text analysis and summarization through a structured workflow. The system extracts key points from a blog post and then generates a concise summary based on those key points using function calling capabilities of modern LLMs.

## Setup Instructions

### Prerequisites

- Python 3.8+
- OpenAI or Groq API access

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/llm-workflow.git
   cd llm-workflow
   ```

2. Install required packages:
   ```bash
   pip install openai python-dotenv
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   # Choose your model server (GROQ or OPENAI)
   MODEL_SERVER=GROQ
   
   # Groq configuration
   GROQ_API_KEY=your_groq_api_key
   GROQ_BASE_URL=https://api.groq.com/openai/v1
   GROQ_MODEL=llama3-70b-8192
   
   # OpenAI configuration
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-4o
   ```

### Running the Application

Run the main script:
```bash
python llm-workflow.py
```

The script will:
1. Load a sample blog post from `sample-blog-post.json`
2. Extract key points from the blog post
3. Generate a summary based on those key points
4. Display the results

## Implementation Details

### Core Components

- **Environment Configuration**: Dynamic configuration based on the selected model provider (OpenAI or Groq)
- **LLM API Integration**: Unified client interface for multiple LLM providers
- **Function Calling**: Structured output generation using the LLM's function calling capabilities
- **Workflow Pipeline**: Sequential processing from blog post to key points to summary

### Key Functions

- `call_llm()`: Makes API calls to the selected LLM provider
- `task_extract_key_points()`: Extracts key points from a blog post
- `task_generate_summary()`: Generates a concise summary from key points
- `run_pipeline_workflow()`: Orchestrates the full workflow

## Example Output

When running the workflow on the sample healthcare AI blog post, you'll get output similar to:

```json
{
  "key_points": [
    "AI is revolutionizing healthcare in diagnosis, treatment development, and patient care delivery",
    "Machine learning algorithms can analyze medical images with high accuracy, often detecting abnormalities that human radiologists might miss",
    "AI-driven imaging technologies are used for breast cancer detection, lung diseases, neurological disorders, and cardiovascular conditions",
    "AI helps standardize medical diagnoses and enables remote interpretation through teleradiology",
    "Predictive analytics using AI can identify patterns and risk factors for disease outbreaks, patient readmissions, and complications",
    "AI-powered predictive models assess individual risk factors for conditions like diabetes and heart disease",
    "AI played a crucial role in tracking COVID-19 outbreaks by analyzing various data sources",
    "AI accelerates drug discovery and development by analyzing biological data and predicting compound interactions",
    "AI can model molecular interactions, simulate drug efficacy, and predict side effects before human trials",
    "AI has helped discover new antibiotics to fight resistant bacteria",
    "Personalized medicine is enhanced through AI analysis of genetic information",
    "AI-powered precision medicine helps develop cancer treatments tailored to genetic profiles",
    "Virtual health assistants and chatbots improve patient engagement and provide medical guidance",
    "AI reduces administrative burdens for healthcare providers",
    "Challenges include data privacy, algorithm bias, regulatory approval, and integration with existing systems",
    "The future of healthcare will likely involve AI systems and human providers working together"
  ],
  "summary": "AI is transforming healthcare through advanced diagnostics, predictive analytics, and drug development. In diagnostic imaging, AI detects abnormalities with remarkable accuracy, standardizes diagnoses, and enables remote interpretation. Predictive analytics identifies disease risks and outbreak patterns, while accelerating pharmaceutical research by modeling molecular interactions and predicting drug efficacy. AI also powers personalized medicine through genetic analysis and virtual health assistants that improve patient engagement. Despite challenges like data privacy and algorithm bias, the future of healthcare will likely involve collaborative human-AI approaches that enhance efficiency, accuracy, and accessibility of medical care."
}
```

## Analysis of Effectiveness

The pipeline workflow design proves effective for several reasons:

1. **Modularity**: Breaking down the process into discrete tasks allows for easier maintenance and updates.

2. **Step-by-step processing**: Extracting key points first creates a more focused and accurate summary, as the LLM can concentrate on distilling information rather than processing the entire article at once.

3. **Consistent output structure**: Using function calling ensures that outputs conform to expected formats, making the results more reliable and easier to integrate with other systems.

4. **Flexibility**: The workflow design supports multiple LLM providers, allowing users to choose based on cost, performance, or availability.

5. **Error handling**: The implementation includes basic error handling to gracefully manage API failures or data issues.

This approach is particularly well-suited for processing longer documents where direct summarization might lose important details or nuance.

## Future Improvements

Potential enhancements could include:

- Adding more tasks to the workflow (e.g., sentiment analysis, topic extraction)
- Implementing parallel processing for greater efficiency
- Adding a feedback loop where summary quality is evaluated
- Creating a web interface for easier interaction
- Supporting batch processing of multiple documents


## Challenges & How They Were Solved

1. API Errors & Invalid Responses

Problem: API calls sometimes returned empty or malformed responses.

Solution: Implemented error handling and fallback responses.

2. AttributeError: 'ChatCompletionMessage' object has no attribute 'get'

Problem: Incorrectly accessing tool_calls as a dictionary.

Solution: Used hasattr(response.choices[0].message, "tool_calls") to check for tool usage.

3. Encoding Issues with .env File

Problem: .env file had invalid encoding, causing UnicodeDecodeError.

Solution: Ensured the .env file was saved in UTF-8 (without BOM) format.

4. Execution Order Issues in DAG Workflow

Problem: Some dependent tasks executed before required inputs were available.

Solution: Adjusted task dependencies to ensure proper execution order.
