import time
import unittest
from src.GenAI.FunctionCalling.models.Test import Test_all_model_main as tamm
from src.GenAI.FunctionCalling.models.Test import Test_followup_questions as tfq

if __name__ == '__main__':
    
    start_time = time.time()
    unittest.main(module=tfq)
    end_time = time.time()

    runtime_seconds = end_time - start_time
    minutes = int(runtime_seconds // 60)
    seconds = int(runtime_seconds % 60)
    print("Runtime:", minutes, "minutes", seconds, "seconds")





    # start_time = time.time()
    # unittest.main(module=tamm)
    # end_time = time.time()

    # runtime_seconds = end_time - start_time
    # minutes = int(runtime_seconds // 60)
    # seconds = int(runtime_seconds % 60)
    # print("Runtime:", minutes, "minutes", seconds, "seconds")