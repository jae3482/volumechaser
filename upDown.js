var tds = document.getElementsByTagName('td');

for (var i = 0; i < tds.length; i++) {
    if(tds.item(i).innerHTML[0] === "+") {
        tds.item(i).style.color = 'red';
    } else if(tds.item(i).innerHTML[0] === "-") {
        tds.item(i).style.color = 'blue';
    }
}

