from openai import OpenAI
import instructor

client = instructor.patch(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    ),
    mode=instructor.Mode.JSON,
)

stream = client.chat.completions.create(
    model="phi3:instruct",
    temperature=0.5,
    top_p=0.65,
    max_tokens=100,
    messages=[
        {"role": "system", "content": "What do you think about apple tree?"},
    ],
    stream=True,
)    

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
