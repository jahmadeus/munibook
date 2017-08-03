/*jslint browser:true*/
/*global window, console, ajax*/
$(document).ready(function () {
    "use strict";

    // Get vehicleId from django views via hidden form value
    var vid = $("select#vehicleId").find("option:selected").val();
    var data = {"vehicleId": vid};
    // AJAX call to get all Vehicle comments
    ajax("/getvehiclecomments", data, function (result) {
        // Log the resulting JSON data from the ajax call
        console.log(result);
        // Unhide the vehicle comments ul
        $("ul#vehicle-comments").show();
        // If there are vehicle comments to display
        if (result.length > 0) {
            // Add each comment to the DOM as an html list item
            result.forEach(function (comment) {
                $("ul#vehicle-comments").append("<li><p>"
                        + comment.text
                        + "<br><small>"
                        + comment.datePosted
                        + "</small></p></li>");
            });
        } else {
            // If there are no comments to display, tell user
            $("ul#vehicle-comments")
                .append("<li><p><i>No Comments for Vehicle</i></p></li>");
        } // End of IF/Else
    }); // End of ajax() function

    // On vehicle comment form submit
    $("form#vehicle-comment-form").submit(function (event) {
        $("<input />").attr("type", "hidden")
            .attr("name", "vehicleId")
            .attr("value", vid)
            .appendTo("form#vehicle-comment-form");

        // Remove all comments from comments ul (to be refreshed with updated list)
        $("ul#vehicle-comments li").remove();

        // Serialize the vehicle comment form data
        var data_sec = $("form#vehicle-comment-form").serializeArray();

        // AJAX call to post Vehicle comment and get updated comments list
        ajax("/addvehiclecomment", data_sec, function (result) {
            // Log the resulting JSON data from the ajax call
            console.log(result);
            // Unhide the vehicle comments ul
            $("ul#vehicle-comments").show();
            // If there are vehicle comments to display
            if (result.length > 0) {
                // Add each comment to DOM as an html list item
                result.forEach(function (comment) {
                    $("ul#vehicle-comments").append("<li><p>"
                            + comment.text
                            + "<br><small>"
                            + comment.datePosted
                            + "</small></p></li>");
                });
            } else {
                // If there are no comments to display, tell user
                $("ul#vehicle-comments")
                    .append("<li><p><i>No Comments for Vehicle</i></p></li>");
            }
        });
        // Prevent form from submitting and redirecting page
        event.preventDefault();
        return false;
    });
});
