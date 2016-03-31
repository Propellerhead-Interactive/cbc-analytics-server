window.lana = {
  server: "http://cbc.propellerheadlabs.io:8888"
};

/*
 * Lana.js
 * v0.1.0
 * MIT License
 * =====================================
 * Based on Ahoy.js
 * Simple, powerful JavaScript analytics
 * https://github.com/ankane/ahoy.js
 * v0.1.0
 * MIT License
 */

/*jslint browser: true, indent: 2, plusplus: true, vars: true */

(function (window) {
  "use strict";

  var lana = window.lana || window.Lana || {};
  var server = lana.server || "";
  var visitId, visitorId, track;
  var visitTtl = 4 * 60; // 4 hours
  var visitorTtl = 2 * 365 * 24 * 60; // 2 years
  var isReady = false;
  var queue = [];
  var canStringify = typeof(JSON) !== "undefined" && typeof(JSON.stringify) !== "undefined";
  var eventQueue = [];
  var page = lana.page || window.location;
  var category = lana.category || "none";
  var visitsUrl = lana.visitsUrl || server + "/lana/visits";
  var eventsUrl = lana.eventsUrl || server + "/lana/events";

  var cookies = {
    visit: "lana_visit",
    visitor: "lana_visitor",
    events: "lana_events",
    track: "lana_track",
    debug: "lana_debug"
  };

  // cookies

  // http://www.quirksmode.org/js/cookies.html
  function setCookie(name, value, ttl) {
    var expires = "";
    var cookieDomain = "";
    if (ttl) {
      var date = new Date();
      date.setTime(date.getTime() + (ttl * 60 * 1000));
      expires = "; expires=" + date.toGMTString();
    }
    if (lana.domain) {
      cookieDomain = "; domain=" + lana.domain;
    }
    document.cookie = name + "=" + escape(value) + expires + cookieDomain + "; path=/";
  }

  function getCookie(name) {
    var i, c;
    var nameEQ = name + "=";
    var ca = document.cookie.split(";");
    for (i = 0; i < ca.length; i++) {
      c = ca[i];
      while (c.charAt(0) === " ") {
        c = c.substring(1, c.length);
      }
      if (c.indexOf(nameEQ) === 0) {
        return unescape(c.substring(nameEQ.length, c.length));
      }
    }
    return null;
  }

  function destroyCookie(name) {
    setCookie(name, "", -1);
  }

  function doHttpRequest(method, url, data, contenttype, callback){

    var proper_url = url;
    if (method !== "GET"){
      proper_url = url;
    }else if(method === "GET" && !!data){
      proper_url += "?" + data;
    }

    var r = new XMLHttpRequest();
    r.open(method, proper_url, true);

    if (!!contenttype) {
      r.setRequestHeader("Content-Type", contenttype);
    }

    r.onload = function(e) {
      if (r.status >= 200 && r.status < 400){
        callback(r);
      }
    };

    r.onerror = function(e){
      console.log("Error:");
      console.log(e);
    };

    if (method === "POST") {
      r.send(data);
    } else {
      r.send();
    }
  }

  function log(message) {
    if (!!getCookie(cookies.debug)) {
      window.console.log(message);
    }
  }

  function setReady() {
    var callback;
    while (queue.length > 0) {
      callback = queue.shift();
      callback();
    }
    isReady = true;
  }

  function ready(callback) {
    if (!!isReady) {
      callback();
    } else {
      queue.push(callback);
    }
  }

  // http://stackoverflow.com/a/2117523/1177228
  function generateId() {
    //prefix with timestamp
    var d = (new Date()).getTime();
    //generate id with this pattern
    var id = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
        var r = Math.random()*16|0, v;
        if(c ==="x"){
          v = r;
        }else{
          v = (r&0x3|0x8);
        }
    return v.toString(16);
    });
    return d+"-"+id;
  }

  function saveEventQueue() {
    // TODO add stringify method for IE 7 and under
    if (!!canStringify) {
      setCookie(cookies.events, JSON.stringify(eventQueue), 1);
    }
  }

  function trackEvent(event) {
    ready( function () {
      // ensure JSON is defined
      if (!!canStringify) {

        //todo - add contenttype and datatype-json to function
        doHttpRequest("GET", eventsUrl, JSON.stringify(event), "application/json", function(){
          for (var i = 0; i < eventQueue.length; i++) {
            if (eventQueue[i].id === event.id) {
              eventQueue.splice(i, 1);
              break;
            }
          }
          saveEventQueue();
        });
      }
    });
  }

  //http://gomakethings.com/climbing-up-and-down-the-dom-tree-with-vanilla-javascript/
  //function getClosest(elem, selector){
  //  var firstChar = selector.charAt(0);
  //
  //  // Get closest match
  //  for ( ; elem && elem !== document; elem = elem.parentNode ) {
  //
  //      // If selector is a class
  //      if ( firstChar === "." ) {
  //          if ( elem.classList.contains( selector.substr(1) ) ) {
  //              return elem;
  //          }
  //      }
  //
  //      // If selector is an ID
  //      if ( firstChar === "#" ) {
  //          if ( elem.id === selector.substr(1) ) {
  //              return elem;
  //          }
  //      } 
  //
  //      // If selector is a data attribute
  //      if ( firstChar === "[" ) {
  //          if ( elem.hasAttribute( selector.substr(1, selector.length - 2) ) ) {
  //              return elem;
  //          }
  //      }
  //
  //      // If selector is a tag
  //      if ( elem.tagName.toLowerCase() === selector ) {
  //          return elem;
  //      }
  //
  //  }
  //
  //  return false;
  //}

  //function eventProperties(e) {
  //  var temp = getClosest(e, "[data-section]");
  //
  //  return {
  //    tag: e.tagName.toLowerCase(),
  //    id: e.id,
  //    "class": e.className,
  //    page: page.pathname,
  //    category: category,
  //    section: temp ? temp.getAttribute("data-section") : ""
  //  };
  //}

  //function addEvtHandlers(els, evt) {
  //  for (var el in els) {
  //    for (var i = 0; i < els[el].length; i++) {
  //      els[el][i].addEventListener(evt, function(event){
  //        var properties = event.properties;
  //        lana.track("$" + evt, properties);
  //      }, false);
  //    }
  //  }
  //}

  // main

  visitId = getCookie(cookies.visit);
  visitorId = getCookie(cookies.visitor);
  track = getCookie(cookies.track);

  if (!!visitId && !!visitorId && !track) {
    // TODO keep visit alive?
    log("Active visit");
    setReady();
  } else {
    if (!!track) {
      destroyCookie(cookies.track);
    }

    if (!visitId) {
      visitId = generateId();
      setCookie(cookies.visit, visitId, visitTtl);
    }

    // make sure cookies are enabled
    if (getCookie(cookies.visit)) {
      log("Visit started");

      if (!visitorId) {
        visitorId = generateId();
        setCookie(cookies.visitor, visitorId, visitorTtl);
      }

      var data = {
        visit_token: visitId,
        visitor_token: visitorId,
        platform: lana.platform || "Web",
        landing_page: page.href,
        screen_width: window.screen.width,
        screen_height: window.screen.height
      };

      // referrer
      if (document.referrer.length > 0) {
        data.referrer = document.referrer;
      }

      log(data);

      //todo - set responsetype as json
      //doHttpRequest("GET", visitsUrl, JSON.stringify(data), false, setReady);
    } else {
      log("Cookies disabled");
      setReady();
    }
  }

  lana.getVisitId = lana.getVisitToken = function () {
    return visitId;
  };

  lana.getVisitorId = lana.getVisitorToken = function () {
    return visitorId;
  };

  lana.reset = function () {
    destroyCookie(cookies.visit);
    destroyCookie(cookies.visitor);
    destroyCookie(cookies.events);
    destroyCookie(cookies.track);
    return true;
  };

  lana.debug = function (enabled) {
    if (enabled === false) {
      destroyCookie(cookies.debug);
    } else {
      setCookie(cookies.debug, "t", 365 * 24 * 60); // 1 year
    }
    return true;
  };

  lana.track = function (name, properties) {
    // generate unique id

    properties.url = encodeURIComponent(page.href);
    properties.title = document.title;

    var event = {
      visit: visitId,
      visitor: visitorId,
      id: generateId(),
      name: name,
      properties: properties,
      time: (new Date()).getTime() / 1000.0
    };
    log(event);

    eventQueue.push(event);
    saveEventQueue();

    // wait in case navigating to reduce duplicate events
    setTimeout( function () {
      trackEvent(event);
    }, 1000);
  };

  //lana.trackView = function () {
  //  var properties = {
  //    url: encodeURIComponent(page.href),
  //    title: document.title,
  //    page: page.pathname,
  //    category: category
  //  };
  //  lana.track("$view", properties);
  //};
  //
  //lana.trackClicks = function () {
  //  var els = {
  //    anchors: document.getElementsByTagName("a"),
  //    buttons: document.getElementsByTagName("button"),
  //    allinputs: document.getElementsByTagName("input"),
  //    inputs: []
  //  };
  //  for (var el in els) {
  //    if(el === "allinputs") {
  //      for (var i = 0; i < els[el].length; i++) {
  //        if(els[el][i].type === "submit"){
  //          els.inputs.push(els[el][i]);
  //        }
  //      }
  //
  //      els[el] = [];
  //    }
  //
  //    for (var i = 0; i < els[el].length; i++) {
  //      els[el][i].addEventListener("click", function(event){
  //        var target = event.target;
  //        var properties = eventProperties(target);
  //        properties.text = properties.tag === "input" ? target.value : target.innerHTML.replace(/[\s\r\n]+/g, " ").trim();
  //        properties.href = target.href;
  //        lana.track("$click", properties);
  //      }, false);
  //    }
  //  }
  //};
  //
  //lana.trackSubmits = function () { 
  //  var onsubmit_els = {
  //    forms: document.getElementsByTagName("form")
  //  };
  //
  //  addEvtHandlers(onsubmit_els, "submit");
  //};
  //
  //lana.trackChanges = function () {
  //  var onchange_els = {
  //    forms: document.getElementsByTagName("input"),
  //    textareas: document.getElementsByTagName("textarea"),
  //    selects: document.getElementsByTagName("select")
  //  };
  //
  //  addEvtHandlers(onchange_els, "change");
  //};
  //
  //lana.trackAll = function() {
  //  lana.trackView();
  //  lana.trackClicks();
  //  lana.trackSubmits();
  //  lana.trackChanges();
  //};

  lana.doHttpRequest = doHttpRequest;

  // push events from queue
  try {
    eventQueue = JSON.parse(getCookie(cookies.events) || "[]");
  } catch (e) {
    // do nothing
  }

  for (var i = 0; i < eventQueue.length; i++) {
    trackEvent(eventQueue[i]);
  }

  window.lana = lana;
}(window));