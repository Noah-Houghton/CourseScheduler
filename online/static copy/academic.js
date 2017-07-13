/** academic.js
 * 
 * Noah Houghton, Raahul Acharya, and Luke Sajer
 * Professor David J. Malan
 * CS50
 * 
 * 
 * */
// run once DOM is loaded
$(function()
{
    academic();
    // script to search and display results for keyword "fun"
    function academic(){
        var parameters = {
            q: "",
            k: "academic"
        };
        
        $.getJSON(Flask.url_for("searching"), parameters)
        .done(function(data) {
            console.log(data);
            // build display of results of search
            var plural = "";
            if (data.length > 1)
            {
                plural = "s";
            }
            
            var div = "<h3>Found " + data.length + " result" + plural + " for \"Academic\". To search for more, click on \"Search\" above. </h3> <div class=\"panel-group\" id=\"accordion\">";
            for (var i = 0; i < data.length; i++)
            {
                div += "<div class=\"panel panel-default\"><div class=\"panel-heading\"> <h4 class=\"panel-title\"><a data-toggle=\"collapse\" data-parent=\"#accordion\" href=\"#collapse_" 
                + i + "\">" + data[i].title + "</a></h4></div><div id=\"collapse_" + i + "\" class=\"panel-collapse collapse\"><div class=\"panel-body\">" 
                + data[i].content + "</div></div></div>";
            }
            div +="</div>";
            var results = document.getElementById("results");
            results.innerHTML = div;
        })
        .fail(function(statusText) {
    
            // log error to browser's console
            console.log(statusText);
            console.log("failure");
            var div = "An error occurred. Please try again. If the error persists notify an admin.";
            document.getElementById("results").innerHTML = div;
        });
        
    }
});