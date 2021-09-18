#AWS Project 2
Author: Charlie Gong
email: hgong25@asu.edu

Before running this project, please make sure the requirements are installed:
1. aws iam configured
2. python requirements installed

```
aws configure
pip3 install -r requirements.txt
```

Resource Info:
- Input Bucket name: asu-project2-input-ghh
- Output Bucket name: asu-project2-output-ghh

**This project only consider the scalability,**
**HA design is not included in this project**

web instance startup
```
python3 web.py
```

app instance startup
```
python3 app.py
```
