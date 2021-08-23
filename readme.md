
# Machine Fault Recognition using Wafer 

This project is about predicting a production line machine fault status using Wafer data. 

For this purpose, historical data is validated, segregated into clusters and then seperate machine learning models are built for each cluster. 

During prediction, each wafer is classified into an appropriate cluster and using the model for that cluster, its status is predicted.

**Services Used:**

Version Control: DVC

Source Control: this git repository

Cloud Service: Heroku

Using one click the models are automatically built and upon commit to git, they are automatically deployed to Heroku platform.








## API Reference

```http
  https://machine-fault-recog-mbaig.herokuapp.com/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `folderPath` | `string` | **Required** |

#### Post JSON Request

```http
  POST https://machine-fault-recog-mbaig.herokuapp.com/predict
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `folderPath` | `string` | **Required** |


#### Gives prediction about machine status

Runs under two modes:
1. Takes custom folder path provided by user and generates predictions in a .csv file, sharing the output location.
2. Uses the inbuilt prediction folder, genereate the .csv and share the path.

  
## Demo

https://media.giphy.com/media/wnOjxfRSbrMS3xLU4u/source.mov?cid=790b761144220111132ad55c6b8daecf487224476ebee8b8&rid=source.mov&ct=g

  
## Deployment

To deploy this project, please follow the below steps in the same order 

create environment

```bash
  conda create -n <envname> python=3.6 -y
```

activate the environment

```bash
  conda activate <envname>
```

install the requirements file

```bash
  pip install -r requirements.txt
```

download the data from

```http
    https://drive.google.com/drive/folders/10dAftFpAvOTUgpAU2I-b9SFzaBmFwB70?usp=sharing
```

create a working directory to hold this project and use the below git commands 
to push work directory contents to your git repo

```bash
    git init
    git add . && git commit -m "first commit"
    git remote add origin https://github.com/.......git
    git branch -M main
    git push origin main
```

build your own package commands

```bash
    python setup.py sdist bdist_wheel 
```

## Execution Preparation and Steps:
1. Data for training and prediction is coming from Amazon S3 bucket. Make your own S3 bucket and hold the data
    a. Training Data - bucket: wafer-data and folder/object: historical-data/
    b. Prediction Data - bucket: wafer-data and folder/object: current-data/
2. All the training modules can be run with a single command $ dvc repro
3. It will segregate train data into clusters and create custom model for each cluster. The models will sit in 
   s3 bucket: wafer-models and reports would go to bucket: wafer-reports
4. s3 buckets need to be created manually by user along with an s3 full access permissions. 
   These keys need to be updated as follows:
   Windows - Update the file "C:\Users\<UserName>\.aws\credentials" 
   Heroku - $ heroku config:set AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=yyy AWS_DEFAULT_REGION=zzz -a <dyno-name>
5. Prediction can be invoked from the url https://machine-fault-recog-mbaig.herokuapp.com/ or via postman service
   as mentioned above





  
## Authors

- [@Mansoor Baig](https://github.com/MansoorAB)

  
## Appendix

DVC https://dvc.org/

  