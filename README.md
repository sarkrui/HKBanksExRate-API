This application displays currency exchange rates (RMB-HKD, and HKD-USD only) fetched from multiple banks (based Hong Kong) official websites/APIs in an HTML table at `localhost/`. It also provides a raw JSON output at `localhost/raw `.

### Functions

-  `getHSBCRate()`: Returns buying rates for USD and HKD from HSBC as a tuple `(BuyUSD, BuyHKD)`.
-  `getCMBWLRate()`: Returns buying rates for USD and HKD from CMBWL as a tuple `(BuyUSD, BuyHKD)`.
-  `getBOCHKRate()`: Returns buying rates for USD and HKD from BOCHK as a tuple `(BuyUSD, BuyHKD)`.
-  `getHKBEARate()`: Returns buying rates for USD and HKD from HKBEA as a tuple `(BuyUSD, BuyHKD)`.
-  `getICBCAISARate()`: Returns buying rates for USD and HKD from ICBC ASIA as a tuple `(BuyUSD, BuyHKD)`.

### Routes

-  `/`: Displays a Bootstrap-styled table with buying rates of USD and HKD from different banks. It also shows the last updated timestamp.
-  `/raw`: Returns a JSON object that contains the raw buying rates of USD and HKD from different banks and the last updated timestamp.

### Deployment with Gunicorn

1. Install Gunicorn

   ```bash
   pip install gunicorn
   ```

2. Run the following command to start the Gunicorn server:

   ```bash
   bashCopy code
   gunicorn --bind 0.0.0.0:8000 app:app -w 4
   ```

-  `--bind 0.0.0.0:8000`: This binds the application to all available network interfaces at port 8000.
-  `app:app`: Specifies that the Flask application is in a Python file named `app.py` and the Flask application object is named `app`.
-  `-w 4`: Launches 4 worker processes to handle incoming requests.

------

### License 

This project is licensed under the terms of the MIT License.

```
MIT License

Copyright (c) 2023 Sark

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

