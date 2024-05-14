# Ollama Function Calling 1.0.0 (Experimental)

This experimental project contain a way of implementing **Multiple Function Calling** for locally running Large Language Models.
For this, Google's Gemma 2B model is used through Ollama.

## Importent
For the demostration purpose, this project contain a sample chat application (without memory functionality) for artbitary gym called SLEEPING GYM & FITNESS CENTER.

## Requirements
### Packages
   `pip install openai pydantic instructor requests rich python-dotenv`

   ### Ollama
   You can download Ollama application from [here](https://ollama.com/download).

   Then open the terminal and run `ollama pull gemma:2b`\
   The file size be around 1.7GB

   After pulling the Gemma 2B, you can run \
   `ollama list` - to view all the downloaded models \
   `ollama run gemma:2b` - to confirm model is running correctly.

   ### API Endpoint
   Visit to [Rapid API](https://rapidapi.com/hub) and make an account.\
   Then subscribe to [ExerciseDB](https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb/) for free.

   ### Environment Variables
   Create a .env as the .env.example


## Prompt Engineering Techniques
- Few Shot Prompting
- Zero Shot Prompting

## Diagram of The Project
![alt Structure that i followed](https://od.lk/s/NV8xOTMxODk2NjRf/Screenshot%202024-05-13%20at%2023.05.43.png)

## Notes
- This is NOT the perfect solution for large number of functions.
- This is ONLY an experimental project
- Sometimes this will not provide the answer what we want. (Errors can be occured) 
- Over heating, high amount of memory swapping can be happen due to running a LLM on your local machine / laptop.
- This project is initiated on Apple MacBook Air (M1) 8GB RAM, sometimes the Ollama may not be perform correctly on Windows.