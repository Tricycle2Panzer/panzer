from be import serve
from be.model.order import time_exceed_delete

if __name__ == "__main__":
    serve.be_run(auto_cancel=True)

