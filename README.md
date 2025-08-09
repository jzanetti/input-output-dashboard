# Deploy the input-output dashboard

1. Log in to PythonAnywhere and open a **Bash** console.
2. Clone your repository:

```bash
cd ~
git clone https://github.com/jzanetti/input-output-dashboard
cd input-output-dashboard
```

## Create & activate a virtualenv, install deps

Choose a Python version that matches the one you selected in the Web tab (e.g. `3.13`).

```bash
# create virtualenv (PythonAnywhere convention under ~/.virtualenvs)
python3.13 -m venv ~/.virtualenvs/dashenv
source ~/.virtualenvs/dashenv/bin/activate
pip install --upgrade pip
cd ~/input-output-dashboard
pip install -r requirements.txt
```

## Configure the Web app on PythonAnywhere

1. On PythonAnywhere, go to the **Web** tab and click **Add a new web app** (or edit an existing one).
2. Choose **Manual configuration** and pick the **same Python version** used in your virtualenv (e.g. 3.10).
3. Set the **Source code** and **working directory** to your project folder: `/home/<yourusername>/<repo>` (this is normally auto-detected).
4. Enter the virtualenv path under **Virtualenv**: `/home/<yourusername>/.virtualenvs/dashenv`.


## Edit the WSGI configuration file

Click the WSGI file link on the Web tab (it opens an editor). Replace or update the file to include your project path and import the Flask `server` from your `app.py`.

**Example WSGI file** (replace `<username>` and `<repo>`):

```python
import sys
import os

project_home = '/home/<username>/<repo>'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
from app import server as application
```

## Reload & test
1. On the PythonAnywhere **Web** tab click **Reload**.
2. Visit `https://jzanetti1985.pythonanywhere.com`.
3. If it fails, open the **Error log** link on the Web tab — that file contains Python tracebacks which are essential for debugging.

### Reference:
- `HHI`: https://pmc.ncbi.nlm.nih.gov/articles/PMC9760014/?utm_source=chatgpt.com