import re
from oocana import Context
from langchain_core.runnables import RunnablePassthrough

def main(inputs: dict, context: Context):
  sources: list[dict] = []

  def format_docs(docs):
    texts: list[str] = []
    for doc in docs:
      content = re.sub(r"\s+", " ", doc.page_content)
      source_id = len(sources)
      sources.append({
        "metadata": doc.metadata,
        "content": content,
      })
      texts.append(f"Source: {source_id}\n{content}")

    return "\n\n".join(texts)

  retriever = inputs["retriever"]
  prompt_params = {
    "context": retriever | format_docs, 
    "input": RunnablePassthrough()
  }
  return { 
    "prompt_params": prompt_params,
    "sources": sources,
  }