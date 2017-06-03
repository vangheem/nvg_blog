---
layout: post
title:  "Embedding Go and groupcache in Python"
date: 2017-06-03 07:16:00
categories: python open-source golang groupcache
description: Exploration on embedding the awesome Go groupcache library into Python
published: true
---


# Using Go in Python

`Go(golang)` is a very fast and efficient compiled programming language. Much like
how you can build Python C-extensions to speed up your python applications, Python
developers also have the option to build Go components that are embedded into their python.


# A Simple Demonstration

**Before you get started, make sure to install golang.**

We'll create a `Go` file named `gcode.go` that has a function in it that simply
prints a string. Then in Python, we'll call that function.

Put the following contents into `gocode.go`:

{% highlight go %}
package main

import (
  "fmt"
  "C"
)

//export say_hi
func say_hi(txt *C.char) {
  fmt.Printf(C.GoString(txt))
}


func main() {}

{% endhighlight %}

The important bit of the Go code is `//export say_hi`. This tells the Go compiler
to export the function to be able to be used in the `.so` file we'll build next.

Also, please notice the use of the Go `C` library to convert C types to Go types.

So, next we compile it into an `.so` file::

{% highlight bash %}
$ go build -buildmode=c-shared -o gcode.so gcode.go
{% endhighlight %}

The `-buildmode=c-shared` bit is important here as we need to create an
`.so`(shared object) file.

Finally, hook it up with python:

{% highlight python %}
import ctypes
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
lib = ctypes.cdll.LoadLibrary(os.path.join(dir_path, 'gcode.so'))

go_say_hi = lib.say_hi
go_say_hi.argtypes = [ctypes.c_char_p]

def say_hi(txt):
    return go_say_hi(ctypes.c_char_p(txt.encode('utf8')))

if __name__ == '__main__':
    say_hi('Hello!')
{% endhighlight %}


The Python wiring here relies on ctypes. After getting some of the cruft out of
arranging the function signatures, it's really pretty easy.

# Embedding groupcache into Python

[groupcache](https://github.com/golang/groupcache) is a great caching library
written in Go. It allows Go applications to implement a shared LRU cache and is
very fast.

`groupcache` has one caveat: It is a read-only cache. You can not modify values once they are in the cache. This means, the only way you can do invalidation is by issuing a new key for a cache value.

At [Onna](https://www.onna.com), we investigated the feasibility of using
groupcache in Python. It ended up being that we couldn't use it for our use-case;
however, since Onna likes to open source all that we can, we wanted to open
source the project in case anyone was interested in developing the implementation further.

Of course, our implementation was going to be a `guillotina` module. You can
find the package on the [guillotinaweb github organization](https://github.com/guillotinaweb/guillotina_groupcache).

## Install the dependencies

Go has it's own built-in packaging system::

{% highlight bash %}
$ go get github.com/golang/groupcache
{% endhighlight %}

## Integration

From there, it's using the same method as described above for exposing Go
functions to export to the `.so` and using `ctypes` in Python to setup the
function signatures.

{% highlight go %}
package main

import (
  "github.com/golang/groupcache"
  "net/http"
  "log"
  "errors"
)

import "C"

// temporary storage to be able to set data
var Store = map[string]string{}

var peers *groupcache.HTTPPool = nil
var cache *groupcache.Group = nil
var srv *http.Server = nil


//export cache_set
func cache_set(key *C.char, value *C.char) *C.char {
  // groupcache does not have a way to set a value in the cache(pass through cache)
  // so we fake it by setting value in global store and then getting the value immediately..
  // Ideally, this is switched out with a backend that retrieves the value
  // you want to cache
  var gkey = C.GoString(key)
  var gvalue = C.GoString(value)
  Store[gkey] = gvalue;
  var data = ""
  cache.Get(nil, gkey, groupcache.StringSink(&data))
  delete(Store, gkey)
  return C.CString(data)
}


//export cache_get
func cache_get(key *C.char) *C.char {
  var data = ""
  cache.Get(nil, C.GoString(key), groupcache.StringSink(&data))
  return C.CString(data)
}

//export setup
func setup(addr *C.char) {

  go func() {
    peers = groupcache.NewHTTPPool(C.GoString(addr))
    cache = groupcache.NewGroup("Cache", 64<<20, groupcache.GetterFunc(
      func(ctx groupcache.Context, key string, dest groupcache.Sink) error {
        v, ok := Store[key]
        if !ok {
          return errors.New("cache key not found")
        }
        dest.SetBytes([]byte(v))
        return nil
      }))

    srv := &http.Server{Addr: C.GoString(addr), Handler: http.HandlerFunc(peers.ServeHTTP)}

    if err := srv.ListenAndServe(); err != nil {
      log.Fatal("ListenAndServe: ", err)
    }
  }()
  // do it in a go routine so we don't block
  log.Print("Running cache server node\n")
}

//export initialized
func initialized() bool {
  return cache != nil
}

func main() {}
{% endhighlight %}


Finally, the Python wiring::

{% highlight python %}
import ctypes
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
lib = ctypes.cdll.LoadLibrary(os.path.join(dir_path, 'gcache.so'))


gget = lib.cache_get
gget.restype = ctypes.c_char_p
gget.argtypes = [ctypes.c_char_p]


def get(key):
    return gget(ctypes.c_char_p(key.encode('utf8')))


gset = lib.cache_set
gset.restype = ctypes.c_char_p
gset.argtypes = [ctypes.c_char_p, ctypes.c_char_p]


def set(key, value):
    if not isinstance(value, bytes):
        value = value.encode('utf-8')

    return gset(
        ctypes.c_char_p(key.encode('utf8')),
        ctypes.c_char_p(value))


gsetup = lib.setup
gsetup.argtypes = [ctypes.c_char_p]


def setup(addr):
    gsetup(ctypes.c_char_p(addr.encode('utf8')))
{% endhighlight %}


# Guillotina caching

The original goal of this was to provide a `guillotina` database shared cache
implementation that was really fast.

We had to abandon it for a
[redis implementation](https://github.com/guillotinaweb/guillotina_rediscache)
because dealing the the read-only aspect of the cache came with it's own
complexity and issues.


# Final thoughts

Once I understood the initial setup of how to integrate Go with Python,
it was really nice to work with. Go is a great language. I am going to consider
it instead of c-extensions when I need to optimize my Python code from now on.
