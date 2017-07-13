
// run once DOM is loaded
$(function()
{
        document.getElementById("searchSubmit").addEventListener("click", function(){
            search(document.getElementById("q"));
        });

        document.getElementById("submitContent").addEventListener("click", function(){
            linkify();
        });

    
    // script to turn links into anchors
    // uses Linkify http://soapbox.github.io/linkifyjs/docs/
    function linkify(){
        var options = {/* … */};
        linkifyElement(document.getElementById('submitContent'), options, document);
    }
    
    // script to search and display results live
    function search(query){
        // get places matching query (asynchronously)
        var parameters = {
            q: query
        };
        console.log("Flask");
        $.getJSON(Flask.url_for("search"), parameters)
        .done(function(data, textStatus, jqXHR) {
            console.log(data);
            // build display of results of search
            var div = "Found {{ data|length }} result{% if data|length > 1 %}s{% endif %} for search \"{{ session.search }}\" with keywords \"{{ session.keywords }}\".{% endif %} </h3> <div class=\"panel-group\" id=\"accordion\">";
            for (var i = 0; i < data.length; i++)
            {
                div += "<div class=\"panel panel-default\"><div class=\"panel-heading\"> <h4 class=\"panel-title\"><a data-toggle=\"collapse\" data-parent=\"#accordion\" href=\"#collapse{{" + i + "}}\")>" + data[i].title + "}}</a></h4></div><div id=\"collapse{{ " + i + "}}\" class=\"panel-collapse collapse\"><div class=\"panel-body\">{{" + data[i].content + "}}</div></div></div>";
            }
            document.getElementById("results").innerHTML=div;
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
    
            // log error to browser's console
            console.log(errorThrown.toString());
            var div = "An error occurred. Please try again. If the error persists notify an admin.";
            document.getElementById("results").innerHTML=div;
        });
}

// script to generate previews for links
    function preview(){
        
    }

});