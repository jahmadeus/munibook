/*jslint browser:true*/
/*global window, console, ajax*/



$(function () {
    "use strict";
    //$("form#route-comment-form").validate();
    // On vehicle comment form submit
    $("form#route-comment-form").submit(function (event) {
        // Retrieve the current route from the dropdown menu value
        var routeSelected = $("select#route").find("option:selected").val();
        $("<input />").attr("type", "hidden")
            .attr("name", "route")
            .attr("value", routeSelected)
            .appendTo("form#route-comment-form");
        // Remove all comments from comments ul (to be refreshed with updated list)
        $("ul#route-comments li").remove();
        // Serialize comment form data
        var data = $("form#route-comment-form").serializeArray();
        // AJAX call to post Route comment and get updated comments list
        ajax("/addroutecomment", data, function (result) {
            // Log the resulting JSON data from the ajax call
            console.log(result);
            // Unhide the route comments ul
            $("ul#route-comments").show();
            // If there are route comments to display
            if (result.length > 0) {
                // Add each comment to the DOM as an html list item
                result.forEach(function (comment) {
                    console.log(comment);
                    $("ul#route-comments").append("<li><p>"
                            + comment.text
                            + "<br><small>"
                            + comment.datePosted
                            + "</small></p><hr></li>");
                });
            } else {
                // If there are no comments to display, tell user
                $("ul#route-comments").append("<li><p><i>No Comments for Route</i></p></li>");
            }
        });
        // Prevent form from submitting and redirecting page
        event.preventDefault();
        return false;
    });

// On selection of route from dropdown menu
    $("select#route").change(function () {
    // Get the value of the dropdown box selection
        var optionSelected = $("select#route").find("option:selected");
        var valueSelected = optionSelected.val();

        // If not hidden, hide results area
        $("div#results-area").hide();
        // If not hidden, hide stop dropdown menu
        $("#stop-list").hide();
        // If messages already present, clear messages list
        $("ul#messages li").remove();
        var data = {"rt": valueSelected};
        ajax("/getdirections", data, function (result) {
            console.log(result);
            $("#direction option").remove();
            $("#stop option").remove();
            $("#direction")
                .append("<option value=\"\" disabled selected>Select Direction</option>");
            $("label#direction-list").show();
            result.forEach(function (direction) {
                $("#direction").append("<option value=\""
                        + direction.tag
                        + "\">" + direction.name
                        + "</option>");
            });
        });
    });

    $("select#direction").change(function () {
        var optionSelected = $("select#direction").find("option:selected");
        var valueSelected = optionSelected.val();
        $("div#results-area").hide();
        $("ul#messages li").remove();
        var data = {"dir": valueSelected};
        ajax("/getstops", data, function (result) {
            console.log(result);
            $("#stop option").remove();
            $("#stop").show();
            $("#stop").append("<option value=\"\" disabled selected>Select Stop</option>");
            $("label#stop-list").show();
            result.forEach(function (stop) {
                $("#stop").append("<option value=\""
                        + stop.tag + "\">"
                        + stop.name
                        + "</option>");
            });
        });
    });

    $("select#stop").change(function () {
        var optionSelected = $("select#stop").find("option:selected");
        var valueSelected = optionSelected.val();
        var routeSelected = $("select#route").find("option:selected");
        var routeTag = routeSelected.val();

        $("div#results-area").show();

        var top = $("div#results-area").position().top;
        $(window).scrollTop(top);
        $("ul#messages li").remove();
        $("ul#route-comments li").remove();

        var data = {"route": routeTag, "stop": valueSelected};
        ajax("/getpredictions", data, function (result) {
            console.log(result);
            $("div#predictions-box")
                .html("<h2>Predictions</h2><ul id=\"predictions\"></ul>");
            result.messages.forEach(function (message) {
                $("ul#messages").append("<li><p>" + message.text + "</p></li>");
            });
            if (result.predictions_data.length > 0) {
                result.predictions_data.forEach(function (p_direction) {
                    $("ul#predictions").append("<h5>" + p_direction.title + "</h5>");
                    p_direction.predictions.forEach(function (prediction) {
                        $("ul#predictions")
                            .append("  <li><p><a href=\"http://nuess.net/getvehicle?id="
                                    + prediction.vehicleId + "\">" + "Vehicle #"
                                    + prediction.vehicleId + "</a> - <b>"
                                    + prediction.minutes + " minutes</b></p></li>");
                    });
                });
            } else {
                $("div#predictions-box").append("<h5>No Predictions Available</h5>");
            }
        });
        var data_sec = {"route": routeTag};
        ajax("/getroutecomments", data_sec, function (result) {
            console.log(result);
            $("ul#route-comments").show();
            if (result.length > 0) {
                result.forEach(function (comment) {
                    $("ul#route-comments").append("<li><p>"
                            + comment.text
                            + "<br><small>"
                            + comment.datePosted
                            + "</small></p><hr></li>");
                });
            } else {
                $("ul#route-comments")
                    .append("<li><p><i>No Comments for Route</i></p></li>");
            }
        });
    });
});
