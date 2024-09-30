import re
from oocana import Context
from langchain_core.runnables import RunnablePassthrough

def main(inputs: dict, context: Context):
  def format_docs(docs):
    texts: list[str] = []
    for doc in docs:
      content = re.sub(r"\s+", " ", doc.page_content)
      texts.append(content)
    return "\n\n".join(texts)

  retriever = inputs["retriever"]
  prompt_params = {
    "context": retriever | format_docs, 
    "input": RunnablePassthrough()
  }
  return { "prompt_params": prompt_params }