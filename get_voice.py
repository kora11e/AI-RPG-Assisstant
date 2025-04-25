import speech_recognition as sr, pyttsx3 as sx3, wave

r = sr.Recognizer()
mic = sr.Microphone()

def speakText(command:str) -> None:
    engine = sx3.init()
    engine.say(command)
    engine.runAndWait()

print('the program is listening')

def capture_voice() -> None:

    while(1):
        print('listening...')
        try:
            with mic:
                
                #mów głośno bo ten debil od googla nie słyszy
                r.adjust_for_ambient_noise(mic)

                #zmienić timeout na późniejszym etapie
                audio2 = r.listen(mic, timeout=4.0)

                myText = r.recognize_google(audio2)
                myText = myText.lower()
                
                print("Recorded text: ", myText)
                #speakText(myText)

        except sr.RequestError as e:
            print(f"COuld not request result {e}")

        except sr.UnknownValueError:
            print("unknown error occurred")