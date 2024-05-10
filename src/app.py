from openai import OpenAI
import instructor
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from rich import print

client = instructor.patch(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    ),
    mode=instructor.Mode.JSON,
)

class Functions (BaseModel):
    name: str = Field(..., description="Name of the function")
    parameters: List[str] = Field( description="List of parameters of the function")
    
class Call(BaseModel):
    thought: str = Field(..., description="Thought process behind the response")
    moves: Functions = Field(None, description="List of functions used to get the response")


funct_resp = client.chat.completions.create(
    model="phi3:instruct",
    temperature=0.5,
    top_p=0.65,
    max_tokens=100,
    messages=[
    ],
    response_model=Call,
)    



print(funct_resp.model_dump_json(indent=2))


# stream = client.chat.completions.create(
#     model="phi3:instruct",
#     temperature=0.5,
#     top_p=0.65,
#     max_tokens=100,
#     messages=[
#         {"role": "system", "content": "What do you think about apple tree ufaeuhfiuhf"},
#     ],
#     stream=True,
# )
# for chunk in stream:
#     print(chunk.choices[0].delta.content, end="")