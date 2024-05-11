from openai import OpenAI
import instructor
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from rich import print
from functions.functions import get_exercise_list, get_exercise_by_bodypart
import json

#Global variable to store the api response
api_response = []
filtered_api_response = []

# Initialize the client
client = instructor.patch(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    ),
    mode=instructor.Mode.JSON,
)

# Define the schema for the response
class Functions (BaseModel):
    name: str = Field(..., description="Name of the function")
    parameters: List[str] = Field( description="List of parameters of the function")
    
class Call(BaseModel):
    thought: str = Field(..., description="Thought process behind the response")
    moves: List[Functions] = Field(None, description="List of functions used to get the response")

# Make the request for function call
def chat_call(question):
    funct_resp = client.chat.completions.create(
        model="gemma:2b",
        temperature=0.5,
        top_p=0.65,
        max_tokens=100,
        messages=[
            {"role": "system", "content": ''' 
         You are a gym trainer system and you are restricted to talk only about exercises.
         The user will ask about either exercises or exercises based on body parts.
         
         BODY PARTS:
         back
         cardio
         chest
         lower arms
         lower legs
         neck
         shoulders
         upper arms
         upper legs
         waist
         
         For every request, perform zero or one or more of the following MOVES. 
         The MOVES name is case-sensitive and should be as it is. You are not allowed to use any other arbitrary MOVES.
         
         MOVES:
         Get_Exercise_List: Get the list of exercises
         Get_Exercise_By_Bodypart: Get the list of exercises based on body part
         
         
         Respond in the following format:
         {
             "thought": "State the thought process behind the response",
                "moves": [
                    {
                        "name": "Name of the function",
                        "parameters": ["List of parameters of the function"]
                    }
                ]
         }
         
         Examples
         ---
            User: What are the exercises you have?
            {
                "thought": "I need to get the list of exercises",
                "moves": [
                    {
                        "name": "Get_Exercise_List",
                        "parameters": []
                    }
                ]
            }
        ---
            User: What are the exercises for chest?
            {
                "thought": "I need to get the list of exercises for chest",
                "moves": [
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["chest"]
                    }
                ]
            }
        ----
            user: What are the exercises for back?   
            {
                "thought": "I need to get the list of exercises for back",
                "moves": [
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["back"]
                    }
                ]
            }
        ----
            user: What are the exercises for lower arms?
            {
                "thought": "I need to get the list of exercises for lower arms",
                "moves": [
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["lower arms"]
                    }
                ]
            }
        ----
            user: Show me the all the exercises and exercises for chest
            {
                "thought": "I need to get the list of exercises and exercises for chest",
                "moves": [
                    {
                        "name": "Get_Exercise_List",
                        "parameters": []
                    },
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["chest"]
                    }
                ]
            }             
         ----
            user: Show me the all the exercises
            {
                "thought": "I need to get the list of exercises",
                "moves": [
                    {
                        "name": "Get_Exercise_List",
                        "parameters": []
                    }
                ]
            }
        ----
            user: I want to shape my waist
            {
                "thought": "I need to get the list of exercises for waist",
                "moves": [
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["waist"]
                    }
                ]
            }
        ----
            user: I want to build my shoulders
            {
                "thought": "I need to get the list of exercises for shoulders",
                "moves": [
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["shoulders"]
                    }
                ]
            }
        ----
            user: I want to build my upper arms
            {
                "thought": "I need to get the list of exercises for upper arms",
                "moves": [
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["upper arms"]
                    }
                ]
            }
        ---- 
            user: what are the exercises for lower legs, upper legs and cardio
            {
                "thought": "I need to get the list of exercises for lower legs, upper legs and cardio",
                "moves": [
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["lower legs"]
                    },
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["upper legs"]
                    },
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["cardio"]
                    }
                ]
        ----
            user: what are the exercises for stomach
            {
                "thought": "stomach is not in my BODY PARTS list. I should ask the user to ask about the body parts in the list",
                "moves": []
            }  
        ----
            user: what are the exercises for stomach and neck
            {
                "thought": "stomach is not in my BODY PARTS list, neck is in my BODY PARTS list.",
                "moves": [
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["neck"]
                    }
                ]
            } 
        ---
            user: I want find all the exercises
            {
                "thought": "I need to get the list of exercises",
                "moves": [
                    {
                        "name": "Get_Exercise_List",
                        "parameters": []
                    }
                ]
            }
        ----
            user: What are the exercises do you have?
            {
                "thought": "I need to get the list of exercises",
                "moves": [
                    {
                        "name": "Get_Exercise_List",
                        "parameters": []
                    }
                ]
            }                   
        ----
           user: view all the exercises
           {
               "thought": "I need to get the list of exercises",
               "moves": [
                   {
                       "name": "Get_Exercise_List",
                       "parameters": []
                   }
               ]
           }
        ----
              user: show me all the exercises and exercises for chest
              {
                  "thought": "I need to get the list of exercises and exercises for chest",
                  "moves": [
                      {
                          "name": "Get_Exercise_List",
                          "parameters": []
                      },
                      {
                          "name": "Get_Exercise_By_Bodypart",
                          "parameters": ["chest"]
                      }
                  ]
              }
        ---- 
            user: show me all the exercises and exercises for neck
            {
                "thought": "I need to get the list of exercises and exercises for neck",
                "moves": [
                    {
                        "name": "Get_Exercise_List",
                        "parameters": []
                    },
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["neck"]
                    }
                ]
            }         
               
         '''},
            {"role": "user", "content": f"Question: {question}"},
        ],
        response_model=Call,
    )    

    json_response = funct_resp.model_dump_json()
    return json.loads(json_response)
    


# Select the correct function to get the response based on the moves
def selector(json_dict):
    if json_dict["moves"] == []:
        api_response.append({"message": "No moves found. Please ask about exercises or exercises based on body parts"})
    else:    
        for move in json_dict["moves"]:
            if move["name"] == "Get_Exercise_List":
                api_response.append(get_exercise_list())
            elif move["name"] == "Get_Exercise_By_Bodypart":
                api_response.append(get_exercise_by_bodypart(move['parameters'][0]))
            else:
                print("Assistant: Invalid move")

def api_clear_response():
    api_response.clear()
    
# Defined function for regular chat
def chat(question, api_response):
    stream = client.chat.completions.create(
    model="phi3:instruct",
    temperature=0.5,
    top_p=0.65,
    messages=[
        {"role": "system", "content": f'''
          You are a gym trainer and you are restricted to talk only about exercises.
          You will provide the user QUESTION and a array of DATA from database.
          You have to provide suitable natural language answer in shorter way based on QUESTION and DATA.
          Your sound should polite and professional.
         '''},
        {"role": "user", "content": f"QUESTION: {question} DATA: {api_response}  "},
    ],
    stream=True,
)
    for chunk in stream:
        print(chunk.choices[0].delta.content, end="")

def chain():
    question = input("You: ")
    func_resp_dict  = chat_call(question)
    print(func_resp_dict)
    selector(func_resp_dict)
    print(api_response)
    chat(question, api_response)
    
if __name__ == "__main__":
    chain()