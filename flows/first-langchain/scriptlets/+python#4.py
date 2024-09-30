from __future__ import annotations

from oocana import Context
from pydantic import Field, BaseModel

class CitedAnswer(BaseModel):
  """anwser the user question based only on the given sources."""

  anwser_sentences: list[AnswerSentence] = Field(
    ...,
  )

class AnswerSentence(BaseModel):
  sentence: str = Field(
    ...,
  )
  citations: list[int] = Field(
    ...,
    description=" ".join([
      "the interger IDs of the SPECIFIC sources with justify the sentences.",
      "choose the most appropriate source and ignore sources that are irrelevant to the",
      "sentence. if there are no sources, to be an empty list."
    ])
  )

def main(inputs: dict, context: Context):
  return { "output": CitedAnswer }
