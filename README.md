# consensus
A brief info of the state of the consensus

<details>
  <summary>Quick start:</summary>

```sh
cd && git clone https://github.com/Northa/consensus.git && cd consensus
python3 consensus.py
```  
Autorefresh not yet implemented as a workaround you can use bash trick:  
```while true; do; sleep 3 && python3 ./consensus.py;done```
</details>

<details>
  <summary>Requirements:</summary>
  
  *  Ubuntu 20.04+ 
  *  python3.8+
  *  For the correct work of the application you should configure RPC :26657 and REST :1317 endpoints.  
  For example:  
  ```REST = 'http://1.1.1.1:1317'```
  ```RPC = "http://1.1.1.1:26657"```
  
  
</details>

<details>
  <summary>Installing:</summary>
  
  #### Technically, the installation itself is cloning the repo and providing 2 variables

```sh
$ cd && git clone https://github.com/Northa/consensus.git && cd consensus
```  
  
  Next open consensus.py in editor and replace REST/RPC variables with an appropriate values.  
  Example:  
  ```REST = 'http://1.1.1.1:1317'```  
  ```RPC = "http://1.1.1.1:26657"```
  
  Once configured you can run the app by following:
  
  ```$ python3 consensus.py ```
</details>

<details>
  <summary>Tested chains:</summary>  
  
  - Evmos mainnet
  - Evmos testnet
  - Umee  
  - Archway  
  - Cosmic Horizon  
  - Kyve  
  - Kichain
  - Konstellation
  - Stargaze
  - AssetMantle
  - Pylons
  - Deweb
  
</details>



![Example](./screenshots/scr_last.png)
