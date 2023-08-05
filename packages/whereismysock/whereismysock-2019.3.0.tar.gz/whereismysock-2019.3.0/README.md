A convenient way to work with information streaming from websockets, built
on top of the Python iterator protocol.

When subscribing to a stream of qualified data I am usually interested in either
the `latest` value i.e. the one I want when I am ready to do something
with it or `all` the values since I last checked.

`whereismysock` also has a `most` subscriber which is `all` with an upper bound
to the number of messages it keeps in memory (deleting the eldest first).

    >>> from whereismysock import latest
    >>> usdjpy = latest("ws://toplevel/USDJPY")
    >>> next(usdjpy)
    ...

    >>> from whereismysock import all
    >>> nk225 = all("ws://trades/NK225")
    >>> next(nk225)
    ...

I like it because it makes "synchronising" different source of information
super easy.

    >>> hhi = latest("ws://toplevel/HHI")
    >>> hsi = latest("ws://toplevel/HSI")
    >>> next(zip(hhi, hsi))
    ...
