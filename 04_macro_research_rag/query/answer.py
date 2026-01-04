from llm_client import call_llm 
 

def answer(question, context_chunks): 
    context = "\n".join(context_chunks) 
 

messages = [ 
        {"role": "system", "content": "Answer only from context."}, 
        {"role": "user", "content": f""" 
Context: 
{context} 
 

Question: 
{question} 
"""} 
    ] 
    return call_llm(messages)