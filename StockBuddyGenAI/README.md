# StockBuddyGenAI


## Installation and Usage
1. Make sure you have Poetry installed. If not, you can install it via pip:
```pip install poetry```

2. Once Poetry is installed, navigate to your project directory and run:
```poetry install```
This will install all the dependencies specified in `pyproject.toml` file.

3. To run the project:
```poetry run python app.py```

## Prerequisites
Make sure you have the following prerequisites:

- **Database Files**: This project requires `NSE_Yahoo_9_FEB_24.sqlite` and `prompt_cache.db` to be present in the `src/Data` directory of the project. 
- **.env**: Keep the .env file inside `src/GenAI/FunctionCalling/models/.env` it contains the API keys for all the models.

**For linux follow these**:

1. first to the project folder

2. Navigate to the Data directory: ```cd src/Data```

3. Download 'NSE_Yahoo_9_FEB_24.sqlite' using curl: ```curl -L -o NSE_Yahoo_9_FEB_24.sqlite "https://drive.google.com/file/d/1CK-dPtd6hpikAAPIqD0pTo8h2Db2dCio/view?usp=sharing"```

4. Download 'NSE_Yahoo_9_FEB_24.sqlite' using curl: ```curl -L -o prompt_cache.db "https://drive.google.com/file/d/1zCoanAG-SvmZED5CS5kmqNQNfep0bIIW/view?usp=sharing"```

5. Navigate to the directory containing the .env file: ```cd ../GenAI/FunctionCalling/models```

**For windows powershell**: ```Invoke-WebRequest -Uri "file_link" -OutFile file_name```