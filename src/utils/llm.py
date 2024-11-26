from prompts import (
    RESUME_YAML_SCHEMA,
    LLM_YAML_PARSE_PROMPT,
    RESUME_REVIEW_PROMPT,
    JOB_DESCRIPTION_REVIEW_PROMPT,
    REVIEW_OUTPUT_SCHEMA,
)
from src.utils.yaml import extract_yaml
from openai import OpenAI
import os
import streamlit as st
import json
import requests

from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

OLLAMA_LLM_MODEL = os.environ.get("OLLAMA_LLM_MODEL")

@st.cache_resource
def call_llm(prompt, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def call_llama(prompt, stream=False, model=OLLAMA_LLM_MODEL):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt":prompt,
        "stream":stream
    }
    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={"Content-Type":"application/json"})
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: Status code is: {response.status_code}"


def parse_resume(resume_text):
    parse_prompt = LLM_YAML_PARSE_PROMPT.format(
        resume_schema=RESUME_YAML_SCHEMA, resume_text=resume_text
    )
    #resume_yaml = call_llm(parse_prompt)
    resume_yaml = call_llama(parse_prompt)
    return extract_yaml(resume_yaml)


def review_resume(resume_yaml, job_description=None):
    if job_description:
        review_prompt = JOB_DESCRIPTION_REVIEW_PROMPT.format(
            resume_data=resume_yaml,
            job_description=job_description,
            review_output_schema=REVIEW_OUTPUT_SCHEMA,
        )
    else:
        review_prompt = RESUME_REVIEW_PROMPT.format(
            resume_data=resume_yaml, review_output_schema=REVIEW_OUTPUT_SCHEMA
        )

    #review_response = call_llm(review_prompt)
    review_response = call_llama(review_prompt)
    return extract_yaml(review_response)
