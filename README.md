# consensus
A brief info of the state of the consensus

<details>
  <summary>Requirements:</summary>
  
  *  Ubuntu 20.04 
  *  python3.8 
  *  pip3 
  *  pipenv
  *  For the correct work of the application you should configure RPC :26657 and REST :1317 endpoints. For example:  
  http://8.8.8.8:26657 and http://8.8.8.8:1317
  
  
</details>

<details>
  <summary>Installing:</summary>
  
  #### Technically, the installation itself is cloning the repo, setting dependencies, and providing 2 variables

```sh
$ cd && git clone https://github.com/Northa/consensus.git && cd consensus
$ sudo apt install python3-pip
$ pip3 install pipenv
$ pipenv sync

```  
  
  Next open consensus.py in editor and replace REST/RPC variables with an appropriate values.  
  Example:  
  ```REST = 'http://1.1.1.1:1317'```  
  ```RPC = "http://1.1.1.1:26657"```
  
  Once configured you can run the app by following:
  
  ```$ pipenv run python3 consensus.py ```
</details>

<details>
  <summary>Tesed chains:</summary>  
  
  - Evmos evmosdryrun_9009-1  
  - Evmos evmos_9000-4  
  - Umee  
  - Archway  
  - Cosmic Horizon  
  - Kyve  
  
  
  
</details>


![Example](https://github.com/Northa/consensus/blob/main/scr/Screenshot%20from%202022-04-27%2008-53-01.jpg?raw=true "EX")
