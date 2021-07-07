from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class GetAnswer(Action):
	def __init__(self):
		self.faq_data = pd.read_csv('./data/FAQ.csv')

	def name(self):
		return 'action_get_answer'
		
	def run(self, dispatcher, tracker, domain):
		query = tracker.latest_message.text
		questions = self.faq_data['question'].values.tolist()
		answer = self.faq_data['answers'].values.tolist()
		Ratios = process.extract(query, questions)
		print(Ratios)

		mathed_question, score = process.extractOne(query, questions, scorer=fuzz.token_set_ratio)

		if score > 50:
		    matched_row = self.faq_data.loc[self.faq_data['question'] == mathed_question,]
		    answer = matched_row['answers'].values[0]
		    response = "Here's something I found, \n Answer: {} \n".format(answer)

		else:
			response = "Sorry I couldn't find anything relevant to your query!"
						
		dispatcher.utter_message(response)