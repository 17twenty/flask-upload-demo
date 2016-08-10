# Flask-jQuery Upload Demo #
We needed to support uploading a file using a form as well as via an endpoint.
To make sure that works I built this demonstrator that does both, it uses this
rather [nice jQuery plugin](https://github.com/blueimp/jQuery-File-Upload)

## Getting Started ##
It's Python so assuming you have a venv you can do this:
```
$ pip install -U -r requirements.txt
$ python server.py
 * Running on http://0.0.0.0:5001/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 105-027-218
```
Hit that link and you can play around with the simple setup and serve/upload files from your /tmp directory using
both jQuery and regular forms. jQuery uploads are automatic and get added as 'Auto Upload' to the list on the main
page.

## Usage ##
You can either use the main page to upload or use the excellent [httpie](https://github.com/jkbrzt/httpie) and you can do
things like this to hit the ```upload``` endpoint:
```
$ http --form POST localhost:5001/upload file@/home/nglynn/Pictures/welcome.gif
HTTP/1.0 200 OK
Content-Length: 71
Content-Type: application/json
Date: Wed, 10 Aug 2016 01:36:22 GMT
Server: Werkzeug/0.11.8 Python/3.4.3

{
    "message": "success",
    "result": "/v/welcome.gif",
    "status": "success"
}

```
of course it only checks file names but that's enough for now:
```
$ http --form POST localhost:5001/upload file@/home/nglynn/readme.md
HTTP/1.0 500 INTERNAL SERVER ERROR
Content-Length: 60
Content-Type: application/json
Date: Wed, 10 Aug 2016 01:40:12 GMT
Server: Werkzeug/0.11.8 Python/3.4.3

{
    "error_code": "None",
    "message": "Nope",
    "status": "error"
}
```

It will give you a 413 error if you upload a file larger than 16MB.

## Further Development ##
Hopefully it's fairly short and sweet. Uses /static for files, /templates for HTML and uses the best
bits of Flask as well as our ```json_response``` object to keep things standard.
I developed in Python3 and you will want to setup a venv and use the requirements.txt to set up the dependencies.
```
$ pip install -U -r requirements.txt
$ python server.py
```

## Contributors ##
It's a fairly simple, unstyled app. Feel free to build it out and let me know and I'll add you to
the resource list.
 * [nglynn@freelancer.com](mailto:nglynn@freelancer.com)