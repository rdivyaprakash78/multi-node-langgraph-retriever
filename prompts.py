prompts ={
    "wiki answer retriever prompt" :

    """
    Based on the user's request : {user_query}, a wikipedia search has been performed and the top 
    results are here : {wiki_result}. Based on the result answer the user's request. Stick to the 
    most relevant and consice answer. At the end of your response add the phrase : "from wiki"
    """,
    
    "decision maker prompt" :

    """
    Given the user request : {user_input}, Identify that wheather the user is asking a question 
    thats needs to perform a wikipidea search or is it a time related question or is it a general 
    query. 
    
    A wikipedia search is performed when the user is asking information about famous personality, birth,  
    place, thing, event, etc.

    A question is considered to be a time related question if the user asks about the current time,
    date etc. Sample questions : What date is 7 days from now. What time is 6 and a half hours from now
    
    A general question is the one that does not comes under wiki search question and time related question.
    
    Your job is to identify the type of question the user has askes. Your response should be: 
    "wikipedia" or "time" or "general" and nothing else.
    """,

    "python code execution prompt" :

    """
    The user will make a time related request to you. Example requets are: what is the time now,
    what day is today, what is the date 10 days from now etc.

    Based on the user's request : {user_input}, generate a python print statement that will print 
    their required result.

    Your response should be a python code snippet that ends with a print statement that satisfies 
    the user request.

    Your response should be an executable python code. DOnt add anything else in addition.
    """,

    "python result interpreter prompt" :

    """
    The user has made a made a time related request : {user_input}.
    The bot understood the request and generated a result : {pyhton_result}.
    Formulate a response to thet user based on the generated result in a clear and concise manner.
    """
}