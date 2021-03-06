(function (root, factory) {
    root.highlight = factory();
} (this, function () {
    var regex = [
        ['com', /(\/\/ |#).*?(?=\n|$)/],
        ['com', /\/\*[\s\S]*?\*\//],
        ['com', /<!--[\s\S]*?-->/],
        ['str', /(['"`])(\\\1|[\s\S])*?\1/],
        ['num', /[+-]?([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?/],
        ['pct', /[\\.,:;+\-*\/=<>()[\]{}|?!&@~]/],
        ['spc', /\s+/],
        ['nam', /[A-Za-zÀ-ÖØ-öø-ÿ$]+/],
        ['unk', /./]
    ];

    var tokenize = function (text) {
        var tokens = [];

        while (text) {
            for (var i = 0; i < regex.length; i += 1) {
                var str = regex[i][1].exec(text);
                if (!str || str.index !== 0) {
                    continue;
                }
                text = text.slice(str[0].length);
                tokens.push([regex[i][0], str[0]]);
                break;
            }
        }

        return tokens;
    };

    var process = function (element) {
        var tokens = tokenize(element.textContent);
        element.innerHTML = '';
        tokens.forEach(function (token) {
            if (token[0] === 'spc') {
                element.insertAdjacentHTML('beforeend', token[1])
            } else {
                var tokEl = document.createElement('span');
                tokEl.className = 'll-' + token[0];
                tokEl.textContent = token[1];
                element.appendChild(tokEl);
            }
        });
    };

    var highlight = function (element) {};
    highlight.tokenize = process;

    return highlight;
}));

let exclude = ['language-gemtext'];

let codeElements = document.querySelectorAll('pre > code');
for (let i = 0; i < codeElements.length; i++) {
    if (exclude.indexOf(codeElements[i].className) === -1) {
        highlight.tokenize(codeElements[i]);
    }
}