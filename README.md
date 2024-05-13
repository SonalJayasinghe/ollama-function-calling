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
- Chain of thoughts


## Notes
- This is NOT the perfect solution for large number of functions.
- This is ONLY an experimental project.
- Sometimes this will not provide the answer what we want. 
- Over heating, hight amount of memory swapping can be happen due to running an LLM on your local machine / laptop.
- This project is initiated in Apple MacBook Air (M1) 8GB RAM, the Ollama may not be perform correctly on Windows.