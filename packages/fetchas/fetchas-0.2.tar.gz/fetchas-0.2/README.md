# fetchas

Fetch URLs as search engine robot ("fetch as")

Show content or headers of a given URL with the HTTP "User-Agent" header 
set to a search engine robot. Defaults to Googlebot.    

Online help:
```text
usage: fetchas [-h] [-r] [-I] [-a ROBOT_AGENT] url

Fetch URLs as search engine robot.

positional arguments:
  url

optional arguments:
  -h, --help            show this help message and exit
  -r, --follow-redirects
                        Follow redirects, if any occur
  -I, --headers         Show only response headers
  -a ROBOT_AGENT, --robot-agent ROBOT_AGENT
                        ROBOT_AGENT should be one of the following values
                        (default: 'googlebot'): default, desktop, googlebot,
                        mobile, googlebot-mobile, googlebot2, bingbot,
                        bingbot-mobile, browser, iphone, pixel
```

