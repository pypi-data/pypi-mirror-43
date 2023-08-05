# easycon  
A easy-use tool to connect to a remote server. This tool is developed on `paramiko`. 
## Install  
`pip install easycon` 
## Usage 
One can find the instruction by run command `easycon` in terminal directly. 



### Update 2019.03.08  
1. fix bug  
  Fix know bugs for login. This is an old issue relate to stdin. Details see [here](https://github.com/paramiko/paramiko/issues/302). The solution is [here](https://github.com/rogerhil/paramiko/commit/4c7911a98acc751846e248191082f408126c7e8e). 
2. add `put`/`get` to upload/download directory  
3. change the format of the configuration file.
