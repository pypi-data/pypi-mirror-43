(function(){'use strict';var timeParsePatterns=[{re:/^\d{1,2}$/i,handler:function(bits){if(bits[0].length===1){return'0'+bits[0]+':00';}else{return bits[0]+':00';}}},{re:/^\d{2}[:.]\d{2}$/i,handler:function(bits){return bits[0].replace('.',':');}},{re:/^\d[:.]\d{2}$/i,handler:function(bits){return'0'+bits[0].replace('.',':');}},{re:/^(\d+)\s*([ap])(?:.?m.?)?$/i,handler:function(bits){var hour=parseInt(bits[1]);if(hour===12){hour=0;}
if(bits[2].toLowerCase()==='p'){if(hour===12){hour=0;}
return(hour+12)+':00';}else{if(hour<10){return'0'+hour+':00';}else{return hour+':00';}}}},{re:/^(\d+)[.:](\d{2})\s*([ap]).?m.?$/i,handler:function(bits){var hour=parseInt(bits[1]);var mins=parseInt(bits[2]);if(mins<10){mins='0'+mins;}
if(hour===12){hour=0;}
if(bits[3].toLowerCase()==='p'){if(hour===12){hour=0;}
return(hour+12)+':'+mins;}else{if(hour<10){return'0'+hour+':'+mins;}else{return hour+':'+mins;}}}},{re:/^no/i,handler:function(bits){return'12:00';}},{re:/^mid/i,handler:function(bits){return'00:00';}}];function parseTimeString(s){for(var i=0;i<timeParsePatterns.length;i++){var re=timeParsePatterns[i].re;var handler=timeParsePatterns[i].handler;var bits=re.exec(s);if(bits){return handler(bits);}}
return s;}
window.parseTimeString=parseTimeString;})();