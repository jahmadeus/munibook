/*jslint browser:true*/
/*global window, console*/


var keywords = ["role", "base", "input", "init", "legal", "true", "next", "does", "goal",
        "terminal", "distinct", "not"];

function getCookie(name) {
    "use strict";
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        cookies.some(function (cookie) {
            var trimmedCookie = jQuery.trim(cookie);
            if (trimmedCookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
            }
            return (trimmedCookie.substring(0, name.length + 1) === (name + "="));
        });
    }
    return cookieValue;
}

function ajax(url, data, callback) {
    "use strict";
    data.csrfmiddlewaretoken = getCookie("csrftoken");
    $.get(url, data, callback);
}
