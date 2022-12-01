//sorts alphabetically
function sortList() {
  var list, i, switching, b, shouldSwitch;
  //targets unordered list of application names in index.html
  list = document.getElementById("id01");
  switching = true;

  //switch list items if the next one is smaller than the previous one
  while (switching) {
    switching = false;
    b = list.getElementsByTagName("LI");
    for (i = 0; i < (b.length - 1); i++) {
      shouldSwitch = false;
      if (b[i].innerHTML.toLowerCase() > b[i + 1].innerHTML.toLowerCase()) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      b[i].parentNode.insertBefore(b[i + 1], b[i]);
      switching = true;
    }
  }
}