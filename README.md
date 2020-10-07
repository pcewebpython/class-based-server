# CLASS BASED SERVER

A class-based HTTP socket server.

Once you're done, you should be able to start the web server inside the homework directory using `python -u http_server.py` and then point your web browser at locations like:
  * http://localhost:10000/sample.txt
  * http://localhost:10000/a_web_page.html
  * http://localhost:10000/images/sample_1.png

and see the corresponding file located under homework/webroot. Take a moment to look into the homework/webroot and see these files. 

Inside this repository you'll find the http_server.py file. I've added enough stub code for the missing functions to let the server run. And there are more tests for you to make pass!

You do NOT need to execute the `make_time.py` Python file. When a web user visits `http://localhost:1000/make_time.py` you only need to _serve up_ the contents of that file. But if you'd like to take on a challenge, then you _can_ choose to execute the file and serve up the result of performing that execution.


## Hints

* Because your server will be transmitting files as bytes, you might want to try searching for "reading a file as bytes in Python".
* Your `get_content` method is going to be looking at the incoming path and checking whether the path represents a directory, a file, or none of the above. There are relevant methods in the [os.path](https://docs.python.org/3/library/os.path.html) module.
* In some cases, you'll have to get a list of files inside of a directory and then turn that list into a bytestring. There's a method inside of [the os module](https://docs.python.org/3/library/os.html) that can help you address the first part of that problem. You'll then have to turn that list into a string and then a byte-string using techniques you've learned in this class and previous classes.
* Your `get_mimetype` method will receive a path and return an appropriate mimetype. The [mimetypes.guess_type](https://docs.python.org/3.7/library/mimetypes.html) method might be useful. Try playing around with this method at the REPL and manipulating its return value until it matches what you want. For example:
  ```python
  >>> import mimetypes
  >>> result = mimetypes.guess_type("foo/bar.png")
  >>> print(result)
      # ...
  ```
* Finally, your `get_content` method will be receiving `path` arguments such as "/a_sample_page.html". Suppose that you are running your server with the command `python http_server.py` from inside the `class-based-server` directory. Then if you have expressions like `os.path.isfile(path)` in your `response_path` method, these will be looking for a file named "a_sample_page.html" inside of your `class-based-server` directory. That file **doesn't exist**: the "a_sample_page.html" exists inside of the `webroot` directory. So as you're writing your `response_path` method, you're going to have to somehow modify the `path` variable to make python look for files _inside_ of the `webroot` directory.

## Use Your Tests

As you work your way through the steps outlined above, look at your tests. Write code that makes them pass.

There are integration tests that you can run with `python tests.py` and unit tests that you can run with `python unit-tests.py`. The unit tests test everything except for the server method.

You may find it helpful to work through the homework using either or both sets of tests. If you're not sure how to proceed, it may be easier to begin by running the unit tests and trying to make them pass one at a time.

## Going Further

To take this one step further, make the directory listings into clickable links: if you visit `http://localhost:10000/` then the list of files should be clickable links that take you to that file. And similarly if you visit `http://localhost:10000/images/` then the list of images should be clickable links.

If you want to accomplish this, you'll need to:
  * change the mime type for your directory listings from `text/plain` to `text/html`
  * know how to make an HTML link: a link in HTML looks like `<a href="/images/sample_1.png">arbitrary link text</a>`
