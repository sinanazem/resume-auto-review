from datetime import datetime

import openai
from dotenv import load_dotenv
import os
import numpy as np
from pgvector.psycopg2 import register_vector


def format_value(key, value):
    if isinstance(value, dict):
        return ", ".join(filter(None, value.values()))
    elif isinstance(value, datetime):
        return value.strftime('%b %Y')
    elif isinstance(value, (list, tuple)):
        return ", ".join(map(str, value))
    return str(value)

def schema_to_markdown(data, level=1):
    markdown = ""

    if isinstance(data, dict):
        title = data.get('title', '')
        url = data.get('url', '')
        description = data.get('description', '')

        if title:
            heading = '#' * min(level, 3)  # Limit heading level to 3
            if url:
                markdown += f"{heading} [{title}]({url})\n\n"
            else:
                markdown += f"{heading} {title}\n\n"

        if description:
            markdown += f"{description}\n\n"

        for key, value in data.items():
            if key not in ['title', 'url', 'description']:
                if isinstance(value, (dict, list)):
                    markdown += schema_to_markdown(value, level + 1)
                else:
                    markdown += f"**{key.replace('_', ' ').title()}:** {format_value(key, value)}\n"
        markdown += "\n"

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                markdown += schema_to_markdown(item, level)
            elif isinstance(item, str):
                markdown += f"- {item}\n"
            else:
                markdown += schema_to_markdown(item, level)
        markdown += "\n"

    elif isinstance(data, str):
        if len(data.split()) > 10:  # Assume it's a long text field
            markdown += f"{data}\n\n"
        else:
            markdown += f"{data}\n\n"

    return markdown


openai.api_key = os.getenv("OPENAI_API_KEY")

# def get_embeddings(text):
#    response = openai.Embedding.create(
#        model="text-embedding-ada-002",
#        input = text.replace("\n"," ")
#    )
#    embedding = response['data'][0]['embedding']
#    # Embedding
#     # embeddings = OpenAIEmbeddings()
#     # single_vector = embeddings.embed_query(text)
#     return embedding

from openai import OpenAI
client = OpenAI()

def get_embeddings(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding



#Helper function: Get top 3 most similar documents from the database
def get_top3_similar_docs(query, conn):
    query_embedding = get_embeddings(query)
    embedding_array = np.array(query_embedding)
    # Register pgvector extension
    register_vector(conn)
    cur = conn.cursor()
    # Get the top 3 most similar documents using the KNN <=> operator
    cur.execute("SELECT * FROM embeddings ORDER BY embedding <=> %s LIMIT 9", (embedding_array,))
    top3_docs = cur.fetchall()
    return top3_docs


