import re
from oocana import Context
from langchain_core.runnables import RunnablePassthrough

def main(inputs: dict, context: Context):
  source_id: int = 0

  def format_docs(docs):
    nonlocal source_id
    texts: list[str] = []
    for doc in docs:
      content = re.sub(r"\s+", " ", doc.page_content)
      texts.append(f"Source: {source_id}\n{content}")
      source_id += 1

    return "\n\n".join(texts)

  retriever = inputs["retriever"]
  prompt_params = {
    "context": retriever | format_docs, 
    "input": RunnablePassthrough()
  }
  return { "prompt_params": prompt_params }