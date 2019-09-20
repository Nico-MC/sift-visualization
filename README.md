# Visualization App for SIFT


# Get started
- **Use Ubuntu Bash on Windows** (linux subsystem)
- Install python 3.6.7 (with pip)
- Set the environment variables - if not already done - for python & pip (first time skip this)
- Install flask with pip (run 'pip3 install -U Flask')
- Install @quasar/cli globally (1.0.0-rc.2)
  - Make sure its working (just type 'quasar')
- Clone git repository from https://github.com/Nico-MC/sift-visualization

# Starting backend (flask)
- Go to backend directory
- Install pip dependencies ('pip install -r requirements.txt')
- Run 'FLASK_APP=index.py flask run' or 'python index.py'
  - Using Flask produces .pyc files

# Starting frontend (vuejs)
- Go to frontend directory
- Install node modules ('npm install')
- Run 'quasar dev'
- Go to localhost:8080

# Known bugs
- Windows (with Ubuntu bash):
  - Disable firewall or/and antivirus
- Segmentation fault
  - Use 'sudo apt install python3-opencv'

*For questions don't hesitate to contact me: niconoster@t-online.de*
