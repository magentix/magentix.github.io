let codeElements = document.querySelectorAll('pre');
for (let i = 0; i < codeElements.length; i++) {
    if (!codeElements[i].classList.contains('nohighlight')) {
        highlight.el(codeElements[i]);
    }
}