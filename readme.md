
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

Insert gif or link to demo

  
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
    gdrive link goes here
```

create a working directory to hold the project
use the below git commands to push work directory contents to your git repo

```bash
    git init
    git add . && git commit -m "first commit"
    git remote add origin https://github.com/.......git
    git branch -M main
    git push origin main
```




  
## Authors

- [@Mansoor Baig](https://github.com/MansoorAB)

  
## Appendix

DVC https://dvc.org/

  