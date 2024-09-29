from LLM import LLM
import gradio as gr
from scrapper import Scraper

scrap = Scraper()

class Parser(LLM):
    def __init__(self):
        super().__init__()
        self.chat_history = []
        self.dropdown = None
        self.modules = [
        ("Introduction To Stock Markets", "https://zerodha.com/varsity/module/introduction-to-stock-markets/"),
        ("Technical Analysis", "https://zerodha.com/varsity/module/technical-analysis/"),
        ("Fundamental Analysis", "https://zerodha.com/varsity/module/fundamental-analysis/"),
        ("Futures Trading", "https://zerodha.com/varsity/module/futures-trading/"),
        ("Options Theory for Professional Trading", "https://zerodha.com/varsity/module/option-theory/"),
        ("Option Strategies", "https://zerodha.com/varsity/module/option-strategies/"),
        ("Markets and Taxation", "https://zerodha.com/varsity/module/markets-and-taxation/"),
        ("Currency, Commodity, and Government Securities", "https://zerodha.com/varsity/module/commodities-currency-government-securities/"),
        ("Risk Management and Trading Psychology", "https://zerodha.com/varsity/module/risk-management/"),
        ("Sector Analysis", "https://zerodha.com/varsity/module/sector-analysis/")
    ]

    def gen_output(self, prompt):
        self.chat_history.append([prompt, self.call_google(prompt)])
        return self.chat_history
    
    def update_text(self, selection):
        return f"Explain {selection} in detail"
    
    def create_accordion(self, title, url):
        with gr.Accordion(title, open=False):
            self.dropdown = gr.Dropdown(scrap.name_from_links(scrap.scraper(url)), show_label=False, info = "Select any topic to learn")

    def clear(self):
        self.clear_memory = True
        self.chat_history = []

   