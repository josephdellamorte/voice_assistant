import whisper
from multiprocessing import Process
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def record_first(durration):
    #kick off decoding of second audio
    os.system('ffmpeg -y -f avfoundation -i ":0" -t '+str(durration)+' first_audio.mp3 &>/dev/null')

    
def record_second(durration):
    #kick off decoding of first record_audio
    #start recording of second audio
    os.system('ffmpeg -y -f avfoundation -i ":0" -t '+str(durration)+' second_audio.mp3 &>/dev/null')

def record_third(durration):
    #kick off decoding of second record_audio
    #start recording of third audio
    os.system('ffmpeg -y -f avfoundation -i ":0" -t '+str(durration)+' third_audio.mp3 &>/dev/null')

def process_file(file):

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(file)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    '''
    # detect the spoken language
    _, probs = model.detect_language(mel)
    #print(f"Detected language: {max(probs, key=probs.get)}")
    ''' 

    # decode the audio
    options = whisper.DecodingOptions(fp16=False, language=False)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)
    #if "Sarah" in result.text:
    #    print("\a\a\a\a\a\a\a\a\a\a")
    print("'hey part keeper' partial match score:" + str(fuzz.partial_ratio("hey part keeper",result.text)))
    print("'hey park keeper' partial match score:" + str(fuzz.partial_ratio("hey park keeper",result.text)))
    print("'how many minislims do we have?' partial match score:" + str(fuzz.partial_ratio("how many minislims do we have?",result.text)))

    def match_phrase():
        phrases=[ "can you check how many items are in _____",
                 "could you check the stock on the minislims",
                 "how many modems do we have in _____",
                 "what is located in location _____",
                 "what do we have in location ______",
                 "what are the names of the things in location _____",
                 "what is in this box?",
                 "what's the quantity of male microfit pins?",
                 "how many female minifit pins do we have?",
                 "what do you call the part in this bin",
                 "add a part to location _____",
                 "could you add a part to location ______",
                 "could you remove a piece from the tray",
                 "please take ##### out of the male minifit pins stock",
                ]

        '''(nicety,verb,)'''

        
if __name__ == "__main__":

    model = whisper.load_model("small.en")
    record_durration = 13

    first_record_process = Process(target=record_first, args=(record_durration, ))
    first_record_process.start()
    first_record_process.join()
    second_record_process = Process(target=record_second, args=(record_durration, ))
    second_record_process.start()
    process_file("first_audio.mp3")
    second_record_process.join()

    for i in range(5):
        third_record_process = Process(target=record_third, args=(record_durration, ))
        third_record_process.start()
        process_file("second_audio.mp3")
        third_record_process.join()

        first_record_process = Process(target=record_first, args=(record_durration, ))
        first_record_process.start()
        process_file("third_audio.mp3")
        first_record_process.join()

        second_record_process = Process(target=record_second, args=(record_durration, ))
        second_record_process.start()
        process_file("first_audio.mp3")
        second_record_process.join()
