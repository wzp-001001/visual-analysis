
## 使用步骤

1. 服务端：Run the server-side Flask app in one terminal window:
2. 
初次执行并启动：
```sh
   $ cd server
   $ python3 -m venv env
   $ source env/bin/activate
   $ pip install -r requirements.txt
   $ flask run --port=5001 --debug
```
每次启动
   ```sh
   $ cd server
   $ python3 -m venv env
   $ source env/bin/activate
   $ flask run --port=5001 --debug
   ```
 访问 [http://localhost:5001](http://localhost:5001)

1. 客户端：Run the client-side Vue app in a different terminal window:

    ```sh
    $ cd client
    $ npm install
    $ npm run dev
   1
    ```

    访问 to [http://localhost:5173](http://localhost:5173)
