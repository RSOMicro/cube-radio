# RadioLocal Service
This service gets JWT token and saves stations inside a MongoDB

## Running on local computer (recomended)
This was tested on Python 3.10
rename ``.env.example`` to ``.env`` and add ur MongoDB Connection script
then run
```python
pip install -r requirements.txt
python3 src/main.py
```
## Running with docker
TODO
```bash
docker build -t radio-local .
docker run -p 8080:8080 --env-file .env radio-local
```