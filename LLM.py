from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from rag_pipeline import Rag_Pipeline
from langchain.chains.question_answering.chain import load_qa_chain

class LLM(Rag_Pipeline):
    def __init__(self, prompt="Hi"):
        load_dotenv()
        super().__init__()
        self.clear_memory = True
        self.model = None
        self.prompt = None
        self.memory = None
        self.template = """
                        You are a helpful financial advisor chatbot working for AssetAI. Use the provided context to answer the user's question accurately. Always consider the user's chat history for better understanding and personalized responses. Do not mention the word 'Zerodha' at any time.
                        Also sometimes prompt may include asking details about part 1 or part 2 from the context, you always have to provide a detailed answer including both.
                        Here is the information you have:

                        Context: 
                        {context}

                        Chat History: 
                        {chat_history}

                        User's Question: 
                        {question}

                        Based on the above information, provide a detailed and accurate answer to the user's question. Remember to stay relevant to the context and maintain professionalism. Your response should be clear, concise, and helpful:
                        """


        # self.template = """  You are a helpful Assistant with extensive knowledge in the stock market and financial advice.
        #                 Users will ask you questions about the Stock Market, and you must use the given context to answer their questions accurately.
        #                 Always answer in breif and ask the user if he wants detailed explaination
        #                 Follow these guidelines:
        #                 1. Always base your answers on the provided context. Do not make up information.
        #                 2. If the context does not contain the answer, use your financial expertise to provide a comprehensive response based on general knowledge.
        #                 3. If you still do not know the answer, simply say, "I don't know based on the provided information."

        #                 You were talking to the human and here is the chat history so far {chat_history}

        #                 **Context:**
        #                 {context}

        #                 **User Question:**
        #                 {question}

        #                 **Answer:**
        #                 """

    # def call_groq(self, given_prompt):
    #     try:
    #         llm = ChatGroq(
    #             temperature=0.7,
    #             model= "llama3-70b-8192"
    #         )
    #         system = "You are a helpful assistant."
    #         human = "{text}"
    #         prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    #         chain = prompt | llm | StrOutputParser()
    #         return chain.invoke({"text": given_prompt})
    #     except Exception as e:
    #         return f"Error: {str(e)}"
        
    def call_google(self, given_prompt):
        user_input = given_prompt
        if self.clear_memory:
            model_id = "gemini-1.5-pro"
            self.model = ChatGoogleGenerativeAI(model = model_id, temprature = 0.7)
            template = self.template
            self.prompt = PromptTemplate(
                template=template,
                input_variables=["chat_history", "context", "question"]
            )
            self.memory = ConversationBufferMemory(memory_key="chat_history", input_key="question")
            self.clear_memory = False
        chain = load_qa_chain(prompt = self.prompt, llm = self.model, memory = self.memory, chain_type = "stuff")
        print(chain.memory.buffer)
        return chain({
                        "input_documents": self.docsearch.similarity_search(user_input),
                        "question": user_input
                    }, 
                        return_only_outputs=True
                    )["output_text"]