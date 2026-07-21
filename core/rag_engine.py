import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from core.vector_store import build_vector_store,load_vector_store,get_retriever

def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3
    )

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])
 
def build_rag_chain(transcript):
    vector_store=build_vector_store(transcript)

    retriever=get_retriever(vector_store,k=4)

    llm=get_llm()

    prompt=ChatPromptTemplate.from_messages(
          [(
            "system",
            """You are an expert meeting assistant. Answer the user's question
based ONLY on the meeting transcript context provided below.

If the answer is not found in the context, say:
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}""",
        ),
        ("human", "{question}"),
    ]
    )

    full_rag_chain = (
        prompt | llm | StrOutputParser()
    )

    grader_llm = get_llm()
    # lowering temperature for grader (deterministic)
    grader_llm.temperature = 0

    grader_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are a strict QA grader. You are given a USER QUESTION, a retrieved CONTEXT from a meeting transcript, and a proposed ANSWER.
Your task is to determine if the proposed ANSWER can be found, inferred, or supported by the CONTEXT provided.

Respond ONLY with 'GRADED: YES' if the answer is grounded in the context, or 'GRADED: NO' if it is not grounded in the context (it is hallucinatory or based on external knowledge).
Do not provide any explanation of your grade. Just the grade itself as 'GRADED: YES' or 'GRADED: NO'.
""",
        ),
        ("human", "USER QUESTION: {question}\n\nRETRIEVED CONTEXT:\n{context}\n\nPROPOSED ANSWER:\n{answer}"),
    ])

    grader_chain = (grader_prompt | grader_llm | StrOutputParser())

    def get_context_and_query_docs(input_dict):
        docs = retriever.invoke(input_dict["question"])
        docs_text = format_docs(docs)
        return {"docs": docs_text}


    def final_grader(input_dict):
        answer = input_dict["answer"]
        question = input_dict["question"]
        context = input_dict["context"]
        grade = grader_chain.invoke({"question":question,"context":context,"answer":answer})

        if "YES" in grade:
            print("GRADED: YES - returning answer")
            return answer
        else:
            print(f"GRADED: NO - Grade was {grade}")
            return "Based purely on the video context provided, I cannot confidently answer the question. Please rephrase or specify what you are looking for."

    full_final_chain = (
        {
            "context" : retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        }
        | RunnablePassthrough.assign(answer=full_rag_chain)
        | RunnableLambda(final_grader)
    )

    return full_final_chain


def load_rag_chain():
    vector_store = load_vector_store()
    retriver = get_retriever()

    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert meeting assistant. Answer the user's question 
based ONLY on the meeting transcript context provided below.

If the answer is not found in the context, say: 
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}""",
        ),
        ("human", "{question}"),
    ])

    rag_chain = (
        {
            "context":  retriver| RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask_question(rag_chain, question:str) -> str:
    print(f"Question : {question}")
    answer = rag_chain.invoke(question)
    print(f"answer :{answer}")
    return answer


    