import os
def sample():
    basedir = os.path.abspath(os.path.dirname(__file__))
    run = "python " + os.path.join(basedir,"app.py")
    os.system(run)
sample()
