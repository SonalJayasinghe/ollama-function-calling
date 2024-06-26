from openai import OpenAI
import sys
import instructor
from typing import List
from pydantic import BaseModel, Field
from rich import print
from rich.console import Console
from rich.padding import Padding
import json
from functions.functions import get_exercise_by_bodypart, get_exercise_list

#Initialize the console
console = Console()

# Initialize the client from OpenAI
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="gemma"
    ),
    mode=instructor.Mode.JSON,
)

# Select the function based on the move
def selector(json_dict):
    ''' Select the function based on the move from the JSON schema from the user question'''
    api_response = []
    
    for move in json_dict["moves"]:
        if move["name"] == "Get_Exercise_List":
            api_response.append([{ 'type': "get all exercises", 'message': get_exercise_list()}])
        elif move["name"] == "Get_Exercise_By_Bodypart":
            for i in range(len(move['parameters'])):
             api_response.append([{ 'type': f"get exercise for {move['parameters'][i]}", 'message': get_exercise_by_bodypart(move['parameters'][i])}])
        else:
            for i in range(len(move['parameters'])):
                api_response.append([{ 'type': f"No Moves for {move['parameters'][i]}", 'message': { "statusCode" : "400"}}])
    return api_response       

# Convert the API response to natural language
def api_response_to_nl(api_response):
    ''' Convert the API response to natural language'''
    response_text = ""
    for response in api_response:
        i = 1
        response_text += f"-----{response[0]['type']}-----\n"
        for item in response[0]['message']:
            if(item == 'statusCode'):
                response_text += "Sorry!, there is no exercise for requested bodypart. \n"
                break
            response_text += f"{i}. Exercise Name: {item['name']}, Body Part: {item['bodyPart']}, Target Mucle: {item['target']}, Secondary Target Mucles: {item['secondaryMuscles']} \n"
            i += 1
        response_text += "\n\n"
    return response_text

# Define the JSON schema for the response
class Functions (BaseModel):
    name: str = Field(..., description="Name of the function")
    parameters: List[str] = Field( description="List of parameters of the function")
    
class Call(BaseModel):
    thought: str = Field(..., description="Thought process behind the response")
    moves: List[Functions] = Field(None, description="List of functions used to get the response")

# Convert the user question to JSON schema
def chat_call(question):
    ''' Convert the user question to JSON schema using Gemma 2B model'''
    funct_resp = client.chat.completions.create(
        model="gemma:2b",
        temperature=0.1,
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
         
         BODY PARTS should be one of these. If the user asks about any other body part, you should ask the user to ask about the body parts in the list.
         
         For every request, perform zero or one or more of the following MOVES. 
         The MOVES name is case-sensitive and should be as it is. You are not allowed to use any other arbitrary MOVES.
         
         MOVES:
         Get_Exercise_List: Get the list of exercises
         Get_Exercise_By_Bodypart: Get the list of exercises based on body part
         No_Moves: If the user asks about any other body part, you should ask the user to ask about the body parts in the list.
         
         
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
         
         Examples:
         
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
            user: what are the exercises for neck and cardio?
            {
                "thought": "I need to get the list of exercises for neck and cardio",
                "moves": [
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["neck", "cardio"]
                    }
                ]
            }
            
            
            
        ----
            user: show me all the exercises and then provide me specific exercises for upper legs and shoulders
            {
                "thought": "I need to get the list of exercises and then provide specific exercises for upper legs and shoulders",
                "moves": [
                    {
                        "name": "Get_Exercise_List",
                        "parameters": []
                    },
                    {
                        "name": "Get_Exercise_By_Bodypart",
                        "parameters": ["upper legs", "shoulders"]
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
                        "parameters": ["lower legs", "upper legs", "cardio"]
                    }
                ]
            }
            
        ----
            user: what are the exercises for stomach
            {
                "thought": "stomach is not in my BODY PARTS list. I should ask the user to ask about the body parts in the list",
                "moves": [
                    {
                        "name": "No_Moves",
                        "parameters": ["stomach"]
                    }
                ]
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
            {"role": "user", "content": f"user: {question}"},
        ],
        response_model=Call,
    )    

    json_response = funct_resp.model_dump_json()
    return json.loads(json_response)
    
# Defined function for regular chat
def chat(question, context):
    ''' Chat with the user using Gemma 2B model'''
    stream = client.chat.completions.create(
    model="gemma:2b",
    temperature=0.3,
    messages=[
        {"role": "system", "content": f'''
          You are a helpful assistant that works for SLEEPING GYM & FINTNESS CENTER, and you are restricted to talk only about exercises on the GYM. 
          You have user QUESTION and CONTEXT. You can use the CONTEXT to answer the QUESTION.
          You should provide a helpful answer to the user's QUESTION based on the CONTEXT.
          You should describe the exercises in detail provide in CONTEXT.
          
          Text Formating Instructions:
           1. If your answer contain a list, it should numbered list.
           2. If the question contain multiple parts, you should answer all the parts and you shoud separate the answers with a line.
          
         '''},
        
        {
            "role": "user",
            "content": f'''        
            QUESTION: {question}
            CONTEXT: {context}  ''',
        }
    ],
    stream=True,
    response_model=None
)
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K") 
    print("\nAssistant: ", end="")
    for chunk in stream:
        Padding( print(chunk.choices[0].delta.content, end=""), pad=(2, 4))


#Start the chat!
console.print("\n\n------------------ SLEEPING GYM & FITNESS CENTER ------------------", style="bold blue")

while True:
    question = input("You: ")
    
    # Exit the chat
    if(question == "exit"):
        console.print("Assistant: Goodbye! See you at Gym :)", style="bold green")
        break
    
    # Get the JSON schema for the question
    console.print("Thinking...", style="bold green")
    func_resp_dict  = chat_call(question)
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    
    # Call the APIs
    console.print("APIs are calling...", style="bold green")
    api_response = selector(func_resp_dict)
    api_response_nl = api_response_to_nl(api_response)
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    
    # Chat with the user
    console.print("Thinking...", style="bold green")
    chat(question, api_response_nl)
    print("\n")