import gradio as gr
from prompt_parser import Parser
# # !pip install unstructured[pdf]
# # !pip install pypdf
# !pip install rapidocr-onnxruntime
# # !pip install --upgrade pip setuptools wheel
# !pip install -U pkgutil

agent = Parser()

with gr.Blocks(fill_height = True) as app:
    with gr.Tab("Asset AI"):
        gr.Markdown('''## 💸 Asset AI : Your Financial Advisor
                        - 🧑‍💻 Whether you are a newbie or a seasoned investor, I am here to provide you with the best financial advice and insights. 
                        - 🧠 Ask me anything about the stock market, investments, and financial planning.
                        - 🚧 Under Construction
                        - 📢 Next Update will include live stock scraping and interpretations
                        ''')
        with gr.Row():
            with gr.Column(scale = 25):
                with gr.Group():
                    chatbox = gr.Chatbot(label = "🔭 Advisor Panel", show_copy_button = True, height=480)
                    textbox = gr.Textbox(show_label = False, placeholder = "👉 Enter your query")

                    textbox.submit(
                        fn = agent.gen_output,
                        inputs = textbox,
                        outputs = chatbox
                    )
                    submit_button = gr.Button("Submit")
                    submit_button.click(
                        fn = agent.gen_output,
                        inputs = textbox,
                        outputs = chatbox
                    )

                clear = gr.ClearButton([textbox, chatbox],value = "Clear Memory and Start New Chat")
                clear.click(fn= agent.clear)

    
            with gr.Column(scale = 10):
                with gr.Accordion("📖 Learning Roadmap", open = True):
                    gr.Markdown("### 📝 The Selected Topic Will Be Copied To TextBox")
                    for title, url in agent.modules:
                        with gr.Row():
                            agent.create_accordion(title, url)
                        agent.dropdown.change(fn=agent.update_text, inputs=agent.dropdown, outputs=textbox)
        
app.launch()