let myurl = window.location.href;
let mysplit = myurl.split("/");
let myroute = mysplit[mysplit.length - 1]

function sortTable(n, name_table) {
    let table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById(name_table);
    switching = true;
    dir = "asc";

    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            if (myroute == 'analysis'){
                
                if (name_table == 'PERIOD') {
                    if (dir == "desc") {
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == "asc") {
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                } else {
                    if (n == 0){
                        if (dir == "desc") {
                            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                                shouldSwitch = true;
                                break;
                                }
                            } else if (dir == "asc") {
                                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                    shouldSwitch = true;
                                    break;
                                    }
                                }
                    } else {
                        if (dir == "desc") {
                            if (parseFloat(x.innerHTML.toLowerCase()) > parseFloat(y.innerHTML.toLowerCase())) {
                                shouldSwitch = true;
                                break;
                                }
                            } else if (dir == "asc") {
                                if (parseFloat(x.innerHTML.toLowerCase()) < parseFloat(y.innerHTML.toLowerCase())) {
                                    shouldSwitch = true;
                                    break;
                                    }
                                }
                        
                    }
                }

            } else if (myroute == 'modulation') {
                if (n == 0){
                    if (dir == "desc") {
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                            }
                        } else if (dir == "asc") {
                            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                shouldSwitch = true;
                                break;
                                }
                            }
                } else {
                    if (dir == "desc") {
                        if (parseFloat(x.innerHTML.toLowerCase()) > parseFloat(y.innerHTML.toLowerCase())) {
                            shouldSwitch = true;
                            break;
                            }
                        } else if (dir == "asc") {
                            if (parseFloat(x.innerHTML.toLowerCase()) < parseFloat(y.innerHTML.toLowerCase())) {
                                shouldSwitch = true;
                                break;
                                }
                            }
                    
                }
            } else if (myroute == 'priority'){

                if (name_table == 'generaltable') {
                    if (n !== 5){
                        if (dir == "desc") {
                            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                                shouldSwitch = true;
                                break;
                            }
                        } else if (dir == "asc") {
                            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                shouldSwitch = true;
                                break;
                            }
                        }
        
                    } else {
                        if (dir == "desc") {
                            if (parseFloat(x.innerHTML.toLowerCase()) > parseFloat(y.innerHTML.toLowerCase())) {
                                shouldSwitch = true;
                                break;
                            }
                        } else if (dir == "asc") {
                            if (parseFloat(x.innerHTML.toLowerCase()) < parseFloat(y.innerHTML.toLowerCase())) {
                                shouldSwitch = true;
                                break;
                            }
                        }
                        
                    }
                } else if (name_table == 'especifictable') {
                    if (n !== 2){
                        if (dir == "desc") {
                            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                                shouldSwitch = true;
                                break;
                            }
                        } else if (dir == "asc") {
                            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                shouldSwitch = true;
                                break;
                            }
                        }
        
                    } else {
                        if (dir == "desc") {
                            if (parseFloat(x.innerHTML.toLowerCase()) > parseFloat(y.innerHTML.toLowerCase())) {
                                shouldSwitch = true;
                                break;
                            }
                        } else if (dir == "asc") {
                            if (parseFloat(x.innerHTML.toLowerCase()) < parseFloat(y.innerHTML.toLowerCase())) {
                                shouldSwitch = true;
                                break;
                            }
                        }
                        
                    }
                }

            } else if (myroute == 'dayly'){
                if (n == 0 || n == 3){
                    if (dir == "desc") {
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == "asc") {
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    }
    
                } else {
                    if (dir == "desc") {
                        if (parseFloat(x.innerHTML.toLowerCase()) > parseFloat(y.innerHTML.toLowerCase())) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == "asc") {
                        if (parseFloat(x.innerHTML.toLowerCase()) < parseFloat(y.innerHTML.toLowerCase())) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                    
                }
            }
                
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++;
            } else {
                if (switchcount == 0 && dir == "asc") {
                    dir = "desc";
                    switching = true;
                    }
                }
        }
    }
