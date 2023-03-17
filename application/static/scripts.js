// search bar function
function searcher() {
    var filter = document.getElementById('sidebar-search').value.toUpperCase();
    var items = document.getElementById("sidebar-articles").getElementsByTagName('a');
    for (var i = 0; i < items.length; i++) {
        var txtValue = items[i].textContent || items[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            items[i].style.display = "";
        } else {
            items[i].style.display = "none";
        }
    }
}

// inner article links must open in new tab
if (document.getElementsByClassName('article').length > 0) {
    var links = document.getElementsByClassName('article')[0].getElementsByTagName('a');
    if (links.length > 0) {
        for (var i = 0; i < links.length; i++) {
            if (links[i].getAttribute("href")[0] != '#') {
                links[i].target = "_blank";
            }
        }
    }
}

// removes TOC if no subheadings present, add horizontal rule if TOC exists.
if (document.getElementsByClassName('toc').length > 0) {
    if (document.getElementsByClassName('toc')[0].getElementsByTagName('li').length == 0) {
        document.getElementsByClassName('toc')[0].style.display = "none";
    } else {
        document.getElementsByClassName('toc')[0].after(document.createElement("hr"));
    }
}

// tab = 4 spaces in textareas
if (document.getElementsByTagName('textarea').length > 0) {
    document.getElementsByTagName('textarea')[0].addEventListener('keydown', function(e) {
        if (e.key == 'Tab') {
            e.preventDefault();
            var start = this.selectionStart;
            var end = this.selectionEnd;
            // set textarea value to: text before caret + tab + text after caret
            this.value = this.value.substring(0, start) + "    " + this.value.substring(end);
            // put caret at correct position again
            this.selectionStart = this.selectionEnd = start + 4;
        }
    });
}

// KaTex Configuration
(function () {
    'use strict';
    
    var katexMath = (function () {
        var maths = document.querySelectorAll('.arithmatex'),
            tex;
    
        for (var i = 0; i < maths.length; i++) {
            tex = maths[i].textContent || maths[i].innerText;
            if (tex.startsWith('\\(') && tex.endsWith('\\)')) {
                katex.render(tex.slice(2, -2), maths[i], {'displayMode': false});
            } else if (tex.startsWith('\\[') && tex.endsWith('\\]')) {
                katex.render(tex.slice(2, -2), maths[i], {'displayMode': true});
            }
        }
    });
    
    (function () {
        var onReady = function onReady(fn) {
            if (document.addEventListener) {
                document.addEventListener("DOMContentLoaded", fn);
            } else {
                document.attachEvent("onreadystatechange", function () {
                    if (document.readyState === "interactive") {
                        fn();
                    }
                });
            }
        };
    
        onReady(function () {
            if (typeof katex !== "undefined") {
                katexMath();
            }
        });
    })();
    
}());
    
