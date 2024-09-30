import os
from oocana import Context

def main(inputs: dict, context: Context):
  question = inputs["question"]
  answer = inputs["answer"]
  sources = inputs["sources"]
  lines: list[str] = [
    "<h1>Question</h1>",
    f"<p>{question}</p>",
    "<h1>Answer</h1>",
    "<p>"
  ]
  citations_dict: dict[tuple[str, int], tuple[int, str, int, str]] = {}
  next_anchor: int = 1

  for anwser_sentence in answer.anwser_sentences:
    sentence: str = anwser_sentence.sentence
    citations: list[int] = anwser_sentence.citations
    lines.append(sentence)

    for source_id in citations:
      if source_id >= len(sources):
        continue
      source = sources[source_id]
      metadata = source["metadata"]
      content = source["content"]
      page = metadata["page"]
      path = metadata["path"]
      key = (path, page)
      if key in citations_dict:
        anchor = citations_dict[key][0]
      else:
        anchor = next_anchor
        citations_dict[key] = (anchor, path, page, content)
        next_anchor += 1

      lines.append(f"<a href='#{anchor}'>[{anchor}]</a>")

  lines.append("</p>")
  citations_values = list(citations_dict.values())
  citations_values.sort(key=lambda x: x[0])

  if len(citations_values) > 0:
    lines.append("<h1>Citations</h1>")
    for anchor, path, page, content in citations_values:
      file_name = os.path.basename(path)
      lines.append("<h3>")
      lines.append(f"<label id='{anchor}'>[{anchor}]</label>")
      lines.append(f"{file_name}, page {page}")
      lines.append("</h3>")
      lines.append(f"<blockquote>{content}</blockquote>")

  body = "\n".join(lines)
  html = f"""
  <html>
    <head>
      <title>RAG question</title>
    </head>
    <body>{body}</body>
  </html>
  """

  return { "html": html }
