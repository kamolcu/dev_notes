// Run this script in browser console
// Get downloadable link for pdf file
var links = document.getElementsByTagName('a');
for(var ii = 0; i< links.length; ii++){
    if(links[ii] && links[ii].href && links[ii].href.indexOf('.pdf') > 0){
        console.log(links[ii].href);
    }
}