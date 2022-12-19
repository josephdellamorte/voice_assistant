import whisper
from multiprocessing import Process
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from gtts import gTTS
import sys
import datetime

class voice_assistant():
    def __init__(self):
        self.lower_text='no text yet'
        self.inquisitions_response_map= {
                ("how many days are in a week","there are seven days in a week right?"):"there are seven days in a week unless you are the beatles",
                ("how long does it take to make a christmas tree grow",):"six to eight years",
                ("hey part keeper","hey park keeper",):"I'm sorry, part keeper is down",
                ("how much wood could a wood chuck chuck if a wood chuck could chuck wood?",):"depending on age and size, about a cord and a half",
                ("what is the time",):"I don't know that yet",
                ("what is the year",):"I don't know that yet",
                ("when was iggy born",):"July 28 2022",
                }
        self.next_response=None

    def score_phrase(self,text):
        return fuzz.partial_ratio(text,self.lower_text)

    def best_response(self):
        best_score=0
        for inquisition_list in self.inquisitions_response_map.keys():
            for question in inquisition_list:
                score=self.score_phrase(question)
                print(str(question) + " " + str(score))
                if (score > best_score) and score > 90:
                    best_score=score
                    print('better score '+ str(score))
                    self.next_response=self.inquisitions_response_map[inquisition_list]
                


    def aprint(self,text,language='en',slow_speed=False):
        '''Given a string the computer reads off the text'''
        myobj = gTTS(text=text, lang=language, slow=slow_speed)
        myobj.save("acoustic_print.mp3")
        os.system("afplay acoustic_print.mp3")

    def record_first(self,durration):
        '''records to the first file'''
        #kick off decoding of second audio
        os.system('ffmpeg -y -f avfoundation -i ":0" -t '+str(durration)+' first_audio.mp3 &>/dev/null')

        
    def record_second(self,durration):
        '''records to the second file'''
        #kick off decoding of first record_audio
        #start recording of second audio
        os.system('ffmpeg -y -f avfoundation -i ":0" -t '+str(durration)+' second_audio.mp3 &>/dev/null')

    def record_third(self,durration):
        '''records to the third file'''
        #kick off decoding of second record_audio
        #start recording of third audio
        os.system('ffmpeg -y -f avfoundation -i ":0" -t '+str(durration)+' third_audio.mp3 &>/dev/null')

    def process_file(self,file):
        '''runs the audio recording through the whisper speech recognition library'''

        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(file)
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # decode the audio
        options = whisper.DecodingOptions(fp16=False, language=False)
        self.result = whisper.decode(model, mel, options)

        # print the recognized text
        print(self.result.text)
        self.lower_text=str.lower(self.result.text)
        #print(self.lower_text)
        if verbosity:
            pass
            '''
            print("'hey part keeper' partial match score:" + str(hpk))
            print("'hey park keeper' partial match score:" + str(hppk))
            print("'how many minislims do we have?' partial match score:" + str(hmmsdwh))
            '''
        self.best_response()
        if (self.next_response!=None):
            print('TALKING')
            helper.aprint(self.next_response)
            self.next_response!=None

        
if __name__ == "__main__":

    helper=voice_assistant()
    #check for verbose level 1 and 2
    try:
        if sys.argv[1]== "-v":
            verbosity = 1
            print("verbosity is set to high")
    except:
        verbosity=0
    #load model
    model = whisper.load_model("small.en")
    record_durration = 13

    first_record_process = Process(target=helper.record_first, args=(record_durration, ))
    first_record_process.start()
    first_record_process.join()
    second_record_process = Process(target=helper.record_second, args=(record_durration, ))
    second_record_process.start()
    helper.process_file("first_audio.mp3")
    second_record_process.join()

    for i in range(5):
        third_record_process = Process(target=helper.record_third, args=(record_durration, ))
        third_record_process.start()
        helper.process_file("second_audio.mp3")
        third_record_process.join()

        first_record_process = Process(target=helper.record_first, args=(record_durration, ))
        first_record_process.start()
        helper.process_file("third_audio.mp3")
        first_record_process.join()

        second_record_process = Process(target=helper.record_second, args=(record_durration, ))
        second_record_process.start()
        helper.process_file("first_audio.mp3")
        second_record_process.join()
