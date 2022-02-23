from utils import functions
from traceback import print_exc

if __name__ == "__main__":
    cmd = None
    job_list = functions.start_all_jobs()
    while cmd != '/stop':
        cmd = input('> ')
        if not cmd.startswith('/'):
            try:
                eval(cmd)
            except Exception:
                print_exc()
    functions.stop_all_jobs(job_list)