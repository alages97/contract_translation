# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'greeting' domain
"""
from ..root import app

@app.handle(domain='greeting', intent='greet')
def greet(request, responder):
    responder.reply('Hi, I am Amaris chatbot. Ask me anything about Nanocore.') 


@app.handle(domain='greeting', intent='exit')
def exit(request, responder):
    responder.reply('Bye!')
