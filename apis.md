submit/expense/
    POST, returns a json
    input: title, amount, date (optional), user(token)
    output: status: ok

submit/income/
    POST, returns a json
    input: title, amount, date (optional), user(token)
    output: status: ok

/accounts/login/
    POST, returns a json
    input: username, password
    output: status:ok & token

/accounts/register/
    step1: POST
        input: username, email, password
        output: status:ok
    step2: #click on link with the code in the email
        GET
        input: email, code
        output: status: ok (shows the token)

/q/generalstat/
    POST, returns a json
    input: fromdate (optional), todate(optional), token
    output: json from some general stats related to this user

q/expenses/
    POST, returns a json
    input: token, num (optional, default is 10)
    output: last num expenses

q/incomes/
    POST, returns a json
    input: token, num (optional, default is 10)
    output: last num incomes