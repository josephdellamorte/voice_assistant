import whisper
from multiprocessing import Process
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from gtts import gTTS
import pyaudio
import wave
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
                ("what are the mysteries for friday?","for friday the rosary mysteries are?","what are the rosary mysteries for friday"):"the sorrowful mysteries",
                }
        self.next_response=None

    def score_phrase(self,text):
        return fuzz.partial_ratio(text,self.lower_text)

    def best_response(self):
        best_score=0
        for inquisition_list in self.inquisitions_response_map.keys():
            for question in inquisition_list:
                score=self.score_phrase(question)
                if (score > best_score) and score > 90:
                    best_score=score
                    self.next_response=self.inquisitions_response_map[inquisition_list]
                


    def aprint(self,text,language='en',slow_speed=False):
        '''Given a string the computer reads off the text'''
        myobj = gTTS(text=text, lang=language, slow=slow_speed)
        myobj.save("acoustic_print.mp3")
        os.system("powershell -c (New-Object Media.SoundPlayer './acoustic_print.mp3').PlaySync();")

    def record_first(self,durration):
        '''records to the first file'''
        #kick off decoding of second audio
        self.record_wav("first_audio.wav",durration)
        
    def record_second(self,durration):
        '''records to the second file'''
        #kick off decoding of first record_audio
        #start recording of second audio
        self.record_wav("second_audio.wav",durration)

    def record_third(self,durration):
        '''records to the third file'''
        #kick off decoding of second record_audio
        #start recording of third audio
        self.record_wav("third_audio.wav",durration)

    def record_wav(self,filename,duration):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = duration
        WAVE_OUTPUT_FILENAME = filename

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        print(filename + " recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print(filename + " done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


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
            helper.aprint(self.next_response)
            self.next_response=None

        
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
    helper.process_file("first_audio.wav")
    second_record_process.join()

    for i in range(5):
        third_record_process = Process(target=helper.record_third, args=(record_durration, ))
        third_record_process.start()
        helper.process_file("second_audio.wav")
        third_record_process.join()

        first_record_process = Process(target=helper.record_first, args=(record_durration, ))
        first_record_process.start()
        helper.process_file("third_audio.wav")
        first_record_process.join()

        second_record_process = Process(target=helper.record_second, args=(record_durration, ))
        second_record_process.start()
        helper.process_file("first_audio.wav")
        second_record_process.join()
