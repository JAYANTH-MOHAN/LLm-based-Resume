#!/bin/bash


cd "$HOME"
source /home/ubuntu/environments/resume-parser/bin/activate
cd "/home/ubuntu/MLss-ResumeParser/"
echo $PWD
nohup uvicorn --host=0.0.0.0 --port=8001 ResumeParser.main:app > "/home/ubuntu/MLss-ResumeParser/parser_service.log" &

nohup streamlit run logs_visualizer.py > "/home/ubuntu/MLss-ResumeParser/dashboard_service.log" &
echo "Program is running in the background."

