# Metalic
Metalic is a open source library to create reactive web applications in Sanic. It works by listening to item modifications in a dictionary within each Metalic instance. When the dictionary is modified, each connection will be re-drawn (this is where the Jinja2 render it is based off is re-ran). Metalic also allows you to put functions in this dictionary which can be invoked with arguments.

## How do I use this?
Before we get started, you will need a Jinja2-based template that will be the HTML for the web page. Got that? Great, we can continue!

Firstly, we are going to need some stuff to do. This example will add 1 every time a button is pressed. Lets make the function to add one first. The function will take one required argument (the Metalic instance, I will call it `this` for this tutorial). The remainder of the arguments are optional so that they can be added from in the JS. For example, if you wanted to insert a number to add from in the JS, you might have a `number` argument. It is also important to remember that functions are the only way in which you can manipulate the dictionary on the client side in this library. Lets make this function (we will call the number we are adding to `number` in the dictionary later):
```python
def add_one_to_number(this):
    this['number'] += 1
```
Great, now we can initialise the Metalic library! The library takes the Sanic application as a required argument, but after that can either take key word arguments or a dictionary. In this tutorial we will use key word arguments.

It is important to note how you want to initialise it. You can share Metalic instances between multiple users if there are no functions which having shared data will affect. If there are, you will need to make one Metalic instance per user. In this situation, we are going to initialise one per user since we are modifying a integer. Therefore, we are going to initialise it in the route:
```python
from metalic import Metalic

@app.route("/")
async def button_plus_one(*_):
    metalic_instance = Metalic(app, add_one_to_number=add_one_to_number, number=0)
```
To create the renderer HTML for the process, we can simply await the render function of this now with a path to the Jinja2 template:
```python
    return await metalic_instance.render("./button_frontend.html")
``` 
From here, we can handle the front end like a regular Jinja2 template. This means to get the number we can simply type `{{ number }}` in the template. The dictionary is also viewable at the `Metalic` global. This also allows you to call functions which are inside of the dictionary from here. For example, to add one to the number, you would call `Metalic.add_one_to_number()` in JS.

## Caveats
- Due to how WebSockets work in JS, no results are returned by functions. If you want the result, you can run the function, make the function put the result in the dictionary and wait for the page to be redrawn. When this is done, you can simply get the result out of the dictionary.
- Metalic cannot watch objects in the dictionary. If you call a function on a object in the dictionary, you will need to call `update` on the Metalic object.
- All items (except functions) are JSON encoded so they can be sent to the browser. Make sure that all items you send (except functions) can be encoded!
- This library requires the protocol in Sanic to be set as `WebSocketProtocol`. This is simple to do:
```python
from sanic import Sanic
from sanic.websocket import WebSocketProtocol

app = Sanic(__name__)

app.run(protocol=WebSocketProtocol)
```

## Examples
Examples of this library can be found in the `examples` folder.
