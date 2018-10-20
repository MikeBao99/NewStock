import json
from watson_developer_cloud import ToneAnalyzerV3
import textrazor

def analyzeText(text):
  textrazor.api_key = "b695217cdaeb234d8a4edd867e1ab59b23aa1d050fa063c5f4a3a89a"
  client = textrazor.TextRazor(extractors=["topics"])
  response = client.analyze(text)
  topic = map(lambda x: str(x.label), response.topics()[:8])
  ans = ""
  for topica in topic:
    ans += topica + "</h6> <h6>"
  return ans


colors = {'Anger':'#FFE0E6', 'Confident':'#F1DED3', 'Analytical':'#EBE1FE', 'Fear':'#DCF2F2', 'Tentative':'#FFEEFE', 'Sadness':'#D8ECFA', 'Joy':'#FFF5DF'}

def colorText(text):
  tone_analyzer = ToneAnalyzerV3(
      version ='2017-09-21',
      username ='f163ce1a-be0a-4dd8-93f8-17b1b02cc209',
      password ='OUcpFH7JH8rT'
  )
  content_type = 'application/json'

  tone = tone_analyzer.tone({"text": text},content_type)
  ans = ""
  try:
    for sentence in tone['sentences_tone']:
      if len(sentence['tones']) > 0:
        ans += colorSentence(sentence['text'], sentence['tones'][0]['tone_name'])
      else:
        ans += sentence['text']
      ans+= ' '
  except:
    ans = text
  return ans

sents = ["Anger", "Sadness", "Joy", "Fear", "Analytical", "Confident", "Tentative"]
def sentList(text):
  tone_analyzer = ToneAnalyzerV3(
      version ='2017-09-21',
      username ='f163ce1a-be0a-4dd8-93f8-17b1b02cc209',
      password ='OUcpFH7JH8rT'
  )
  content_type = 'application/json'

  tone = tone_analyzer.tone({"text": text},content_type)
  sentiments = [0,0,0,0,0,0,0]
  try:
    for sentiment in range(len(sents)):
      for senti in tone['document_tone']['tones']:
        if senti['tone_name'] == sents[sentiment]:
          sentiments[sentiment] = senti['score']
  except:
    sentiments = [0,0,0,0,0,0,0]
  return sentiments

def colorSentence(sentence, emotion):
	return('<FONT style=\"BACKGROUND-COLOR: ' + colors[emotion] + '\">' + sentence + "</FONT>")
