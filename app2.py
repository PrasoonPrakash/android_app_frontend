from flask import Flask, request, jsonify, render_template, send_file
#from flask_socketio import SocketIO, emit
import os
#import ffmpeg
import assemblyai as aai
#from config import assemblyai_key
import pickle
import pandas as pd
import numpy as np
# from prompter import OpenAIPrompter
import subprocess
import time
import csv
import psutil
import sys
from werkzeug.utils import secure_filename
from write import *

#sys.path.insert(0,'/home/prasoon/breast_cancer_project/trial1/featureExtraction/feature_extraction/')

from feature_extraction import featEx
from transcription import transcribe

app = Flask(__name__)
#socketio=SocketIO(app)

UPLOAD_FOLDER = '/home/prasoon/breast_cancer_project/trial1/featureExtraction/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#with open("randomForest.pkl","rb") as f:
 #   model=pickle.load(f)

# model="gpt-3.5-turbo-0125"
# prompter = OpenAIPrompter(model, max_tokens=16)

# feat_ids = [
#       "AGE", "MARITAL STATUS", "MARRIAGE_DURATION",
#       "EDUCATION", "OCCUPATION", "FAMILY TYPE", "RELIGION",
#      # Medical
#      # "PAST_SURGERY", # --> Missing
#       "MENSTRUAL_STATUS",
#       "TYPE OF MENOPAUSE(NATURAL/HYSTERECTOMY)", "PHYSICAL ACTIVITY",
#       "ABORTION",
#      "ABORTION_NO.",
# ]

name=None
#ans=None
prob_0=None
prob_1=None
is_transcripted=0
is_translated=0
is_featEx=0
is_pred=0
audio_upload=0

@app.route('/upload', methods=['POST'])
def upload_file():
    global name
    global prob_0
    global prob_1
    global is_transcripted
    global is_translated
    global is_featEx
    global is_pred
    global audio_upload
    #global ans
    is_transcripted=0
    is_translated=0
    is_featEx=0
    is_pred=0
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    #emit_stage_update("Uploading...")
    file = request.files['file']
    #file_name=file.filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file_name=secure_filename(file.filename)
    print("Audio file " +file_name+ " uploaded")
    audio_upload=1
    
    #os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    audio_file_path = os.path.join(UPLOAD_FOLDER, file_name)
    #fcntl.flock(audio_file_path, fcntl.LOCK_EX)
    file.save(audio_file_path)
    name,extension=os.path.splitext(file_name)
    print(audio_file_path)
    #emit_stage_update("Transliterating...")
    hindiPath=generateHindi(audio_file_path,name)
    print(name)
    #print("Transcripts generated")
    if(hindiPath!=" "):
        
        #print("hello")
        #emit_stage_update("Translating...")
        #engPath=generateEnglish(hindiPath,name)
        #print("Translation done")
        
        #check_memory_usage()
        #print("translation done")
        #emit_stage_update("Extracting features...")
        csvPath=featureExtraction(name)
        is_featEx=1
        #print("features extracted")
        #time.sleep(5)
        #emit_stage_update("Predicting risk...")
        """ans=prediction(name)
        #sendMsg("Done!")
        #print("prediction done")
        #time.sleep(5)
        #fcntl.flock(f,fcntl.LOCK_UN)
        if (ans):
            s=f"You are classified in the NO risk category for Breast Cancer. \n \n There is a {prob_1}% possibility that you do not have Breast Cancer. \n \n Please continue regular follow-ups with your physician during your next visit."
        else:
            s=f"Based on your assessment, there is a {prob_0}% estimated risk of Breast Cancer. \n \n To ensure your health and well-being, we will schedule an appointment for you at the earliest possible date."""
        audio_upload=0
        return jsonify({"result":"Audio file uploaded, transcripted and translated. Features have been extracted."})
    else:
        return jsonify({"result":"couldn't process file"})
        
def check_memory_usage():
    process = psutil.Process()
    mem_info = process.memory_info()
    print(f"Memory usage: {mem_info.rss} bytes")

def generateHindi(audio_file_path,name):
    global is_transcripted
    if(name=="Pt.code_637_case"):
        print("yess")
        return "/home/prasoon/breast_cancer_project/trial1/featureExtraction/hindiTranscripts/Pt.code_637_case_hindi.txt"
    else:
        try:
            transcript = transcribe(audio_file_path)

            # #aai.settings.api_key = "42906185b53b4fb180376d15b40d8f06"
            # aai.settings.api_key = "e7965528d42e418fa3e74b523b235ee2"
            # audio_url = audio_file_path
            # print(audio_url)
            # config = aai.TranscriptionConfig(language_code='hi')
            # print(config)
            # transcriber = aai.Transcriber(config=config)
            # print(transcriber)
            # transcript = transcriber.transcribe(audio_url)

            print(transcript)
            hindiPath="/home/prasoon/breast_cancer_project/trial1/featureExtraction/hindiTranscripts/"+name+"_hindi.txt"
            print(hindiPath)
            #print(name)
            f1=open(hindiPath,'w')
            #prediction = model.predict(audio_url)
            #text=transcript.text
            f1.write(transcript)
            #print(text)
            #print("uploaded")
            is_transcripted=1
            return hindiPath
        except:
            return " "

"""def generateEnglish(hindiPath,name):
    global is_translated
    if(name=="Pt.code_637_case"):
        engPath="/home/prasoon/breast_cancer_project/trial1/featureExtraction/translatedFiles/Pt.code_637_case_english.txt"
        with open(engPath, 'r') as file:
            contents = file.read()
        print("yessss")
        return contents
    else:
        os.chdir("../IndicTrans2/")
        engPath="/home/prasoon/breast_cancer_project/trial1/featureExtraction/translatedFiles/"+name+"_english.txt"
        process=subprocess.Popen(["python","translate_har_aiims.py", hindiPath,engPath])
        
        timeout=45
        
        #start_time=time.time()
        #while not os.path.exists(engPath) or os.path.getsize(engPath) == 0:
        #    if time.time() - start_time > timeout:
        #        print("Timeout: File was not created or is empty")
        #        break
        #time.sleep(timeout)  # Wait for 1 second before checking again
        process.wait()
        # If the file exists and is not empty, read it
        if os.path.exists(engPath) and os.path.getsize(engPath) > 0:
            with open(engPath, 'r') as file:
                contents = file.read()
            print(contents)
            is_translated=1
            return engPath
        else:
            return "Failed to read the output file"
        print("111"+os.getcwd())
        # Ensure the subprocess has finished
        
        #os.chdir("../featureExtraction")
        #return engPath"""

def featureExtraction(name):
    global is_translated
    global is_featEx
    if(name=="Pt.code_637_case"):
        #print("yyyy")
        csvPath="/home/prasoon/breast_cancer_project/trial1/featureExtraction/csvFiles/demo2.csv"
        return csvPath
    else:
        #os.chdir("../featureExtraction")
        #print("222"+os.getcwd())
        csvPath="/home/prasoon/breast_cancer_project/trial1/featureExtraction/csvFiles/"+name+"_data.csv"
        #engPath="translatedFiles/"+name+"_english.txt"

        obj = featEx(name)
        obj.extractFeatures()
        is_translated=1
        is_featEx=1
        # process=subprocess.run(["python","run3new.py",name])
        #time.sleep(5)
        print("Features extracted")
        #process.wait()
        return csvPath
     
def prediction(name):
    if(name=="Pt.code_637_case"):
        #print("zzzzz")
        sendMsg("DONNEEEE!!!!!!!!")
        return 0
    else:
        global prob_0
        global prob_1
        #print("333"+os.getcwd())
        os.chdir("model")
        process=subprocess.run(["python","prepare.py",name])
        time.sleep(5)
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
        df=pd.read_csv("/home/prasoon/breast_cancer_project/trial1/featureExtraction/updatedCsvFiles/"+name+"_updated.csv")
        
            #x=df.drop(columns=["DIAGNOSIS_Notdone"])
            #y=df["DIAGNOSIS_Notdone"]
        y_pred=model.predict(df)
        
        probability_scores = model.predict_proba(df)
        
        probability_scores=[j for elem in probability_scores for j in elem]
        for i in range(len(probability_scores)):
            if i==0:
                prob_0=probability_scores[i]
                prob_0 = round((prob_0*100),2)
                #prob=prob_0
                    #print( prob_1)
            else:
                prob_1 = probability_scores[i]
                prob_1= round((prob_1*100),2)
                #prob=prob_1
                    # print(prob_2)
        
        
        os.chdir("..")
        print("Prediction done")
        #sendMsg("DONNEEEE!!!!!!!!")
        return y_pred
            
@app.route('/hindi', methods=["GET"])
def hindi():
    global name
    global is_transcripted
    
    hindiText=" "
    #csvPath="csvFiles/"+name+"_data.csv"
    if is_transcripted==1:
        hindiPath="hindiTranscripts/"+name+"_hindi.txt"
        with open(hindiPath,'r') as f:
            hindiText=f.read()
    else:
        hindiText="Please wait. Transcription is in process."
    return jsonify({"transcript": hindiText}), 200
    
@app.route('/english',methods=["GET"])
def english():
    global name
    global is_translated
    
    engText=" "
    if is_translated==1:
        engPath="translatedFiles/"+name+"_english.txt"
        with open(engPath,'r') as f:
            engText=f.read()
    else:
        engText="Please wait. Translation is in process."
    return jsonify({"translation": engText}), 200

@app.route('/name',methods=["GET"])
def features():
    global name
    return jsonify({"name": name}), 200
    
@app.route("/data",methods=["GET"])
def data():
    global name
    csvPath="csvFiles/"+name+"_data.csv"
    df=pd.read_csv(csvPath)
    dicti=df.to_dict()
    return jsonify(dicti)
    
@app.route("/download_csv", methods=['GET'])
def download_csv():
    csv_file_path = os.path.join('csvNoOneHot/'+name+'_data_nooneshot.csv')  # Replace with the actual path

    # Serve the file directly
    return send_file(csv_file_path,
                     as_attachment=True,
                     download_name=name+'_data_nooneshot.csv',  # This is the name that will be used when downloading
                     mimetype='text/csv')
                     
@app.route("/uploadCsvAndPredict", methods=['POST'])
def uploadCsvAndPredict():
    print("HELLLOOOO")
    if 'file' not in request.files:
        print("ERROR!!")
        return jsonify({"error": "No file part"}), 400
    #emit_stage_update("Uploading...")
    file = request.files['file']
    #file_name=file.filename
    if file.filename == '':
        print("No selected file")
        return jsonify({"error": "No selected file"}), 400
    print("HIII")
    file_name=secure_filename(file.filename)
    #print("Audio file" +file_name+ "uploaded")
    #os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    csv_file_path = os.path.join("/home/prasoon/breast_cancer_project/trial1/featureExtraction/csvNoOneHot/", file_name)
    #fcntl.flock(audio_file_path, fcntl.LOCK_EX)
    file.save(csv_file_path)
    print("CSV file "+file_name+" uploaded")
    df=pd.read_csv(csv_file_path)
    dicty=df.to_dict()
    write_dict=one_hot(dicty)
    print("ONE HOT DONE")
    dff=pd.DataFrame([write_dict])
    
    if "Unnamed:0" in dff.columns:
        dff.drop(columns=["Unnamed:0"],inplace=True)
        
    dff.to_csv("/home/prasoon/breast_cancer_project/trial1/featureExtraction/csvFiles/"+name+"_data.csv", index=False)
    
    ans=prediction(name)
        #sendMsg("Done!")
        #print("prediction done")
        #time.sleep(5)
        #fcntl.flock(f,fcntl.LOCK_UN)
    if (ans):
        s=f"You are classified in the NO risk category for Breast Cancer. \n \n There is a {prob_1}% possibility that you do not have Breast Cancer. \n \n Please continue regular follow-ups with your physician during your next visit."
    else:
        s=f"Based on your assessment, there is a {prob_0}% estimated risk of Breast Cancer. \n \n To ensure your health and well-being, we will schedule an appointment for you at the earliest possible date."
    
    return jsonify({"prediction":s})
      
            
"""@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

#@socketio.on("my event")
def sendMsg(msg):
    socketio.emit("my_response", {"data":msg})"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
