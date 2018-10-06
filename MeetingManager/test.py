from watson_developer_cloud import SpeechToTextV1
from os.path import join, dirname
import json

def convert(filename):
	speech_to_text = SpeechToTextV1(
		username='cc286924-dfb4-455f-926d-af445007608c',
		password='IqMUWG3Sj6LK'
	)

	with open(filename,
		           'rb') as audio_file:
		speech_recognition_results = speech_to_text.recognize(
		    audio=audio_file,
		    content_type='audio/mp3',
		    speaker_labels=True,
		    model='en-US_NarrowbandModel'
		).get_result()
	# print(json.dumps(speech_recognition_results, indent=2))
	results = speech_recognition_results["results"]
	speakers = speech_recognition_results["speaker_labels"]
	result_map = []
	speaker_map = {}
	for result in results:
		# print result["alternatives"][0]
		for timestamp in result["alternatives"][0]["timestamps"]:
		    # print timestamp[1], timestamp[2]
		    result_map.append(((timestamp[1],timestamp[2]),timestamp[0]))
	for speaker in speakers:
		speaker_map[(speaker["from"],speaker["to"])] = speaker["speaker"]
	result_map.sort()
	transcript = []
	speaker = speaker_map[result_map[0][0]]
	speech = result_map[0][1]
	# print result_map
	for result in result_map[1:]:
		speaker2 = speaker_map[result[0]]
		speech2 = result[1]
		# print speaker, speech
		# print speaker2, speech2
		if speaker == speaker2:
		    speech += ' ' + speech2
		else:
		    transcript.append((speaker,speech))
		    speaker = speaker2
		    speech = speech2
	transcript.append((speaker,speech))
	text = ""
	onlytext = ""
	for s in transcript:
		text += "Speaker " +  str(s[0]) + " : " + str(s[1]) + "\n"
		onlytext += s[1]
	return text,onlytext

