import random
import os
from absl import logging, flags, app
from multiprocessing import Queue, Manager
from pathos import multiprocessing
import traceback
import time
which_gpus = [0, 1, 2, 3]
max_worker_num = len(which_gpus) * 2
COMMANDS = [
    "python3 main.py " 
]
batch_sizes = [64]#[16, 32, 64]
maskps = [
    #0.1,
    0.5,
    #0.9
]
#me_types = ["softimp"]#["iterative_svd",]# "nucnorm", "softimp"]
me_types = ["svt"]#["iterative_svd",]# "nucnorm", "softimp"]
envs = ["AlienNoFrameskip-v4", "AtlantisNoFrameskip-v4", "CrazyClimberNoFrameskip-v4", "IceHockeyNoFrameskip-v4"]#"ZaxxonNoFrameskip-v4"]#["BreakoutNoFrameskip-v4", "FrostbiteNoFrameskip-v4"]
#envs = ["FrostbiteNoFrameskip-v4"]
svrls = ["--svrl"] #""]
env_name_map = {
    "AlienNoFrameskip-v4":"alien",
    "AtlantisNoFrameskip-v4":"atlantis",
    "CrazyClimberNoFrameskip-v4":"crazy_climber",
    "IceHockeyNoFrameskip-v4":"ice_hockey",
    "BreakoutNoFrameskip-v4":"breakout", 
    "FrostbiteNoFrameskip-v4":"frostbite",
    "ZaxxonNoFrameskip-v4":"zaxxon",
}
timestamp_map = {
    "AlienNoFrameskip-v4":15000000,
    "AtlantisNoFrameskip-v4":30000000,
    "CrazyClimberNoFrameskip-v4":15000000,
    "IceHockeyNoFrameskip-v4":15000000,
    "BreakoutNoFrameskip-v4":15000000, 
    "FrostbiteNoFrameskip-v4":10000000,
    "ZaxxonNoFrameskip-v4":15000000, 
}
def _init_device_queue(max_worker_num):
    m = Manager()
    device_queue = m.Queue()
    for i in range(max_worker_num):
        idx = i % len(which_gpus)
        gpu = which_gpus[idx]
        device_queue.put(gpu)
    return device_queue

def run():
    """Run trainings with all possible parameter combinations in
    the configured space.
    """

    process_pool = multiprocessing.Pool(
        processes=max_worker_num, maxtasksperchild=1)
    device_queue = _init_device_queue(max_worker_num)

    for env in envs:
        for me_type in me_types:
            for maskp in maskps:
                for batch_size in batch_sizes:
                    for svrl in svrls:
                        for command in COMMANDS:
                            if svrl == "--svrl":
                                svrl_string = "svrl"
                            else:
                                svrl_string = ""
                            command += f'--env {env} {svrl} --me_type {me_type} --maskp {maskp} --batch-size {batch_size} --num_timesteps {timestamp_map[env]} {env_name_map[env]}_dqn_{svrl_string}_{me_type}_{maskp}_{batch_size}' 
                            #print(command)
                            process_pool.apply_async(
                                func=_worker,
                                args=[command, device_queue],
                                error_callback=lambda e: logging.error(e))
    process_pool.close()
    process_pool.join()

def _worker(command, device_queue):
    # sleep for random seconds to avoid crowded launching
    try:
        time.sleep(random.uniform(0, 10))

        device = device_queue.get()

        logging.set_verbosity(logging.INFO)

        logging.info("command %s" % command)
        os.system("CUDA_VISIBLE_DEVICES=%d " % device + command)

        device_queue.put(device)
    except Exception as e:
        logging.info(traceback.format_exc())
        raise e
run()

