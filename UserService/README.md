# RadioLocal Service
This service gets JWT token and saves stations inside a MongoDB

## Running on local computer (recomended)
This was tested on Python 3.10
rename ``.env.example`` to ``.env`` and add ur MySQL Connection details
then run
```python
pip install -r requirements.txt
python3 src/main.py
```
## Running with docker
```bash
docker compose up --build
```
