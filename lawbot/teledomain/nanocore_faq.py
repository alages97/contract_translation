def handleFaq(intent):
	switcher = {
		'clean_process':'The pain relief wraps can be easily cleaned with soap and water and either a paper towel or wash cloth. Air dry. ​\n\nTo keep your pain relief wraps from soaking up odors from the fridge simply fold it so that the (chargeable) side is outward and place it in a Ziploc bag before charging.',
		'use_process':'While a minimum of 2 hours a day is ideal for injuries, the pain relief wraps can be worn anytime, day or night, or can even be worn consistently all day. For those suffering from chronic pain, the products can be used whenever the problem flairs up.\n\nMore extreme cases: Some users even buy 2 of the same products and continue to trade off, one on the body, one charging in the fridge to help manage extreme injuries or healing after surgery.',
		'how_it_works':'Nanotechnology utilizes a patent-pending thermal wax which charges quickly when introduced to a fridge or freezer and then holds a temperature range, optimal for healing and pain relief for an extended period of time, far longer than ice or gel.\n\nThe technology helps to pull heat away from the injured muscles, ligaments and tendons to help accelerate healing and reduce swelling and pain. The active cooling side of the products have an antimicrobial surface, are easy to clean and, unlike ice, the temperature is gentle enough to be worn directly against the skin.',
		'unique_selling_point':'We are believers that you should always start with the pain relief and healing option that is the safest, most natural and least invasive before reaching for drugs or considering more costly or risky treatments.\n\nKeep you pain relief wraps on hand for any onset of pain or unexpected injuries. While they may be used alone or in conjunction with other therapies, there is no harm in starting with natural cooling relief to treat you or your loved ones pain first and foremost, everytime.',
		'technology_history':'The powerful healing properties of optimum temperature therapy? Centuries.\n\nThe scientifically crafted thermal wax utilized in the nanohealth products? Decades. This technology has been used for years in military applications and by first responders Nationwide. It has been sold by doctors offices and in hospitals for years - and now, is finally available to all those in pain, straight from the manufacturer.',
		'refund':'We are here to provide pain relief and happiness to our customers.\n\nIf you are not 100% satisfied with your product(s) you can return them anytime within 30 days of purchase and get your money back, no questions asked.',
		'sleep_related':'Absolutely. The pain relief wraps deliver a natural and optimum temperature that slowly warms along with your body temperature. There is no risk associated with enjoying the therapeutic cooling while you are sleeping.',
		'freeze_process':'When the pockets of your wrap are in a liquid state, simply place it in the fridge (or freezer if you would like it to charge a bit faster.\n After about 20 mins you should see the clear pockets turn from a clear liquid, to a bright white, and reach a solid state.',
		'medical_certification':'Our products are FDA Class 1 Medical Device. They are clinically tested, recommended by doctors and used in the hospitals.',
		'one_charge_use':'Our products are designed to maintain the optimum healing temperature for about 1.5 to 2 hours.',
		'bacteria_free':'The active cooling side of the products have an antimicrobial surface to repel bacteria.',
		'product_line':'We have products for Ankle, Back, Elbow, Foot, Hip, Knee, Lumbar-Sciatica, Menopause Relief, Shoulder and Wrist.',
		'hot_flashes':'Imagine your life without hot flashes. As a self-regulated, FDA 510k Registered product, our Menopause Relief Bolero provides immediate and ongoing relief.\nBy using one hour in the morning and evening, it will help to reduce the intensity and frequency of hot flashes. A completely hormone-free solution.',
		'manufacture':'The products are proudly made in U.S.A.',
		'size':'All the products are one-size-fit all.'
	}
	return switcher.get(intent,"Sorry, not sure what you meant there. Try asking me how pain reliefs works?")