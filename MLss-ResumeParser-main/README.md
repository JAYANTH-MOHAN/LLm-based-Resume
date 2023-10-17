# MLss-ResumeParser
Generartive AI Powered Resume Parser

<table>
<thead>
  <tr>
    <th>Module</th>
    <th>Sub-Module</th>
    <th>Inputs</th>
    <th>Supports</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="3">ResumeParser v1.0.0</td>
    <td>pre-processor</td>
    <td> file  </td>
    <td>pdf, doc, docx, jpg, png, jpeg</td>
  </tr>
  
  <tr>
    <td>transcriber</td>
    <td>pre-processor o/p</td>
    <td>file</td>
  </tr>
  <tr>
    <td>post-processor</td>
    <td>transcriber o/p</td>
    <td>text in multiline</td>
  </tr>

</tbody>
</table>

# Manual Installation
## Clone the repo
```commandline
git clone this Repo
cd MLss-ResumeParser
```

## python 3.8
```apex
sudo apt-get update
sudo apt-get install --reinstall libreoffice libreoffice-core
sudo apt-get install poppler-utils
sudo apt-get install python3.8
sudo apt-get install python3.8-dev
wget https://bootstrap.pypa.io/get-pip.py
python3.8 get-pip.py
rm -r get-pip.py
nano .bashrc
export PATH="/home/ubuntu/.local/bin:$PATH"
source .bashrc
pip3.8 install -U pip
mkdir $HOME/environments
pip3.8 install -U virtualenv
virtualenv ~/environments/resume-parser
source ~/environments/resume-parser/bin/activate
pip install -r requirements.txt
```

## Starting the service
```commandline
cd ..
# root directory should be "MLss-ResumeParser"
uvicorn --host=0.0.0.0 --port=8001 ResumeParser.main:app
```


## Starting the service in background with script file
```commandline
cd MLss-ResumeParser
chmod +x start_service.sh
./start_service.sh
```

# For auto start function

```commandline
sudo cp MLss-ResumeParser/ResumeParser.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ResumeParser.service
sudo systemctl start ResumeParser.service 
sudo systemctl status ResumeParser.service
```
