(function(){
    "use strict";
    //get content ID
    var cid = document.location.pathname.match(/([0-9]{1}\.[0-9]+)$/);
    if (!cid){
        console.log("analReadJS: ignoring because not in Polopoly");
        return;
    }else{
        console.log("analReadJS: content id", cid);
    }
    function handleData(resp){
        try{
            var trackingData = { tagged:{}};
            //convert response to JSON
            var jsondata = JSON.parse(resp.responseText);
            
            if (jsondata.type !== "story"){
                console.log("analReadJS: ignoring because not an article");
                return;
            }
            //get people, location, company, organization, subject from JSON
            var dimensions = jsondata.categorization.dimensions;
            var val, i, j, tag_list_name;
            for (i=0; i<dimensions.length; i++){
                for (j=0; j<dimensions[i].entities.length; j++){
                    val = dimensions[i].entities[j].name.toLowerCase().replace(/\s/g, "-").replace(/\./g, "");
                    tag_list_name = dimensions[i].name.toLowerCase();
                    if (!trackingData.tagged[tag_list_name]){
                        trackingData.tagged[tag_list_name] = [];
                    }
                    trackingData.tagged[tag_list_name].push(val);
                    console.log("found attached tag: "+val);
                }
            }
            //get publication date from JSON
            if (!!jsondata.epoch){
                trackingData.publicationDate = jsondata.epoch.pubdate;
            }
            //get title
            if (!!jsondata.headline){
                trackingData.title = jsondata.headline;
            }
            //get url
            trackingData.url = document.location.href;
            //get categories from JSON
            if (!!jsondata.tracking){
                trackingData.category = jsondata.tracking;
            }
            console.log("analReadJS: detected load", trackingData);
            //lana.track("load", trackingData);

            /* configure readJS for this page */
            var readJSConfig = {};
            readJSConfig.el=".story-bodywrapper";
            var beta = document.location.pathname.match(/\/beta\//);
            if (!!beta){
                readJSConfig.el = ".story-wrap";
            }
            readJSConfig.cb = function(){
                console.log("analReadJS: detected read", trackingData);
                //lana.track("read", trackingData);
            };
            window.readJSConfig = readJSConfig;
            
            readJS.initialize(readJSConfig);

        }catch(e){
            console.log("analReadJS:ERROR");
            console.log(e);
        }
    }
    //method, url, data, contenttype, callback
    lana.doHttpRequest("GET", "/json/cmlink/"+cid[0], null, "application/json", handleData); //end of lana.doHttpRequest()
})();