from app import app

import subprocess
app.run(host="0.0.0.0", port=8080, debug=True)
# subprocess.Popen(['sh','script.sh'])



# async def run_script():

#     subprocess.call(['./script.sh']) # 

# run_script()