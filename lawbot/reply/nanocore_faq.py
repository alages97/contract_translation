# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'greeting' domain
"""
from ..root import app

# @app.handle(intent='place_order')
# def place_order(request, responder):
#     """
#     When the user wants to place the order, call an external API to process the transaction and
#     acknowledge the order completion status to the user.

#     For this demo app, we just display a fixed response to indicate that an order has been placed.
#     """
#     responder.reply("We accept the following secure payment options: MasterCard, Visa, American Express and DISCOVER card")

@app.handle(domain='nanocore_faq', intent='clean_process')
def how_to_clean(request, responder):
    responder.reply("The pain relief wraps can be easily cleaned with soap and water and either a paper towel or wash cloth. Air dry. ​\n\nTo keep your pain relief wraps from soaking up odors from the fridge simply fold it so that the 'chargeable' side is outward and place it in a Ziploc bag before charging.")

@app.handle(domain='nanocore_faq', intent='use_process')
def how_to_use(request, responder):
    responder.reply("While a minimum of 2 hours a day is ideal for injuries, the pain relief wraps can be worn anytime, day or night, or can even be worn consistently all day. For those suffering from chronic pain, the products can be used whenever the problem flairs up.\n\nMore extreme cases: Some users even buy 2 of the same products and continue to trade off, one on the body, one charging in the fridge to help manage extreme injuries or healing after surgery.")

@app.handle(domain='nanocore_faq', intent='how_it_works')
def how_it_works(request, responder):
    responder.reply("Nanotechnology utilizes a patent-pending thermal wax which charges quickly when introduced to a fridge or freezer and then holds a temperature range, optimal for healing and pain relief for an extended period of time, far longer than ice or gel.\n\nThe technology helps to pull heat away from the injured muscles, ligaments and tendons to help accelerate healing and reduce swelling and pain. The active cooling side of the products have an antimicrobial surface, are easy to clean and, unlike ice, the temperature is gentle enough to be worn directly against the skin.")

@app.handle(domain='nanocore_faq', intent='unique_selling_point')
def usp_reply(request, responder):
    responder.reply("We are believers that you should always start with the pain relief and healing option that is the safest, most natural and least invasive before reaching for drugs or considering more costly or risky treatments.\n\nKeep you pain relief wraps on hand for any onset of pain or unexpected injuries. While they may be used alone or in conjunction with other therapies, there is no harm in starting with natural cooling relief to treat you or your loved ones pain first and foremost, everytime.")

@app.handle(domain='nanocore_faq', intent='technology_history')
def tech_history(request, responder):
    responder.reply("The powerful healing properties of optimum temperature therapy? Centuries.\n\nThe scientifically crafted thermal wax utilized in the nanohealth products? Decades. This technology has been used for years in military applications and by first responders Nationwide. It has been sold by doctors offices and in hospitals for years - and now, is finally available to all those in pain, straight from the manufacturer.")

@app.handle(domain='nanocore_faq',intent='refund')
def refund(request, responder):
    responder.reply("We are here to provide pain relief and happiness to our customers.\n\nIf you are not 100% satisfied with your product(s) you can return them anytime within 30 days of purchase and get your money back, no questions asked.")

@app.handle(domain='nanocore_faq', intent='sleep_related')
def sleep_related(request, responder):
    responder.reply("Absolutely. The pain relief wraps deliver a natural and optimum temperature that slowly warms along with your body temperature. There is no risk associated with enjoying the therapeutic cooling while you are sleeping.")

@app.handle(domain='nanocore_faq', intent='freeze_process')
def freeze_related(request, responder):
    responder.reply("When the pockets of your wrap are in a liquid state, simply place it in the fridge (or freezer if you'd like it to charge a bit faster).\n After about 20 mins you should see the clear pockets turn from a clear liquid, to a bright white, and reach a solid state.")

@app.handle(domain='nanocore_faq', intent='medical_certification')
def medical_related(request, responder):
    responder.reply("Our products are FDA Class 1 Medical Device. They are clinically tested, recommended by doctors and used in the hospitals.")

@app.handle(domain='nanocore_faq', intent='one_charge_use')
def one_charge(request, responder):
    responder.reply("Our products are designed to maintain the optimum healing temperature for about 1.5 to 2 hours.")

@app.handle(domain='nanocore_faq', intent='bacteria_free')
def bacteria_free(request, responder):
    responder.reply("The active cooling side of the products have an antimicrobial surface to repel bacteria.")

@app.handle(domain='nanocore_faq', intent='product_line')
def product_line(request, responder):
    responder.reply("We have products for Ankle, Back, Elbow, Foot, Hip, Knee, Lumbar-Sciatica, Menopause Relief, Shoulder and Wrist.")

@app.handle(domain='nanocore_faq', intent='hot_flashes')
def hot_flashes(request, responder):
    responder.reply("Imagine your life without hot flashes. As a self-regulated, FDA 510k Registered product, our Menopause Relief Bolero provides immediate and ongoing relief.\nBy using one hour in the morning and evening, it will help to reduce the intensity and frequency of hot flashes. A completely hormone-free solution.")

@app.handle(domain='nanocore_faq', intent='manufacture')
def manufacture(request, responder):
    responder.reply("The products are proudly made in U.S.A.")

@app.handle(domain='nanocore_faq', intent='size')
def size(request, responder):
    responder.reply("All the products are one-size-fit all.")

@app.handle(default=True)
def default(request, responder):
    responder.reply("Sorry, not sure what you meant there. Try asking me how pain reliefs works?")
    #responder.reply("Sorry, not sure what you meant there. Leave us your email and we will be in contact with you as soon as possible.")
    