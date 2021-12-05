let div_generaltable = document.getElementById("div_generaltable")
let div_especifictable = document.getElementById("div_especifictable")

function build(data) {
    if(typeof(data.msg) === 'object') {

        let mydata = data.msg
        let general_values = mydata[0]
        let especific_values = mydata[1]
        let qoe_values = mydata[2]
        let hours_values = mydata[3]
        let period_values = mydata[4]
        let dates = mydata[5]

        let general_table = `
            <table id="generaltable" class="table table-hover" data-excel-name="General_Priority">
            <thead class="table-dark">
                <tr>
                    <td onclick="sortTable(0,'generaltable')" class="header"><strong>Plano</strong></td>
                    <td onclick="sortTable(1,'generaltable')" class="header"><strong>Dependencia</strong></td>
                    <td onclick="sortTable(2,'generaltable')" class="header"><strong>Impedimento</strong></td>
                    <td onclick="sortTable(3,'generaltable')" class="header"><strong>Revisión</strong></td>
                    <td onclick="sortTable(4,'generaltable')" class="header"><strong>Tipo</strong></td>
                    <td onclick="sortTable(5,'generaltable')" class="header"><strong>Días</strong></td>
                    <td onclick="sortTable(6,'generaltable')" class="header"><strong>Problema</strong></td>
                    <td onclick="sortTable(7,'generaltable')" class="header"><strong>Estado</strong></td>
                </tr>
            </thead>
            <tbody>
        `
        for (let value in general_values) {
            general_table += `<tr>`
            general_table += `<td><a href="/detail/`+ general_values[value][0] +`" target= "_blank">`+ general_values[value][0] +`</a></td>`
            for (let i in general_values[value]) {
                if (i != 0) {
                    general_table += `<td>`+ general_values[value][i] +`</td>`
                }
            }
            general_table += `</tr>`
        }
        general_table += `</tbody></table>`
        div_generaltable.innerHTML = general_table

        let especific_head = `
        <table id="especifictable" class="table table-hover" data-excel-name="Especific_Priority">
        <thead class="table-dark">
            <tr>
                <td onclick="sortTable(0, 'especifictable')" class="header"><strong>Plano</strong></td>
                <td onclick="sortTable(1, 'especifictable')" class="header"><strong>Tipo</strong></td>
                <td onclick="sortTable(2, 'especifictable')" class="header"><strong>Días</strong></td>
                <td onclick="sortTable(3, 'especifictable')" class="header"><strong>Problema</strong></td>
                <td onclick="sortTable(4, 'especifictable')" class="header"><strong>Estado</strong></td>
        `
        for (let date in dates) {
            especific_head += `<td class="header"><strong>`+ dates[date] +`</strong></td>`
        }
        especific_head += `</tr></thead><tbody>`
        
        let select = document.getElementById("type")
        
        let especific_body = ``

        if (select.value == 'qoe') {
            for (let e_value in especific_values) {
                especific_body += `<tr>
                <td><a href="/detail/`+ especific_values[e_value][0] +`" target= "_blank">`+ especific_values[e_value][0] +`</a></td>`
                
                for (let j in especific_values[e_value]) {
                    if (j != 0){
                        especific_body += `<td>`+ especific_values[e_value][j] +`</td>`
                    }
                }
                for (let k in qoe_values[e_value]){
                    especific_body += `<td>`+ qoe_values[e_value][k] +`</td>`
                }
            }
            especific_body += `</tbody></table>`
            div_especifictable.innerHTML = especific_head + especific_body
        }

        select.addEventListener("change", function () {
            div_especifictable.innerHTML = ''
            especific_head = `
            <table id="especifictable" class="table table-hover" data-excel-name="Especific_Priority">
            <thead class="table-dark">
                <tr>
                    <td onclick="sortTable(0, 'especifictable')" class="header"><strong>Plano</strong></td>
                    <td onclick="sortTable(1, 'especifictable')" class="header"><strong>Tipo</strong></td>
                    <td onclick="sortTable(2, 'especifictable')" class="header"><strong>Días</strong></td>
                    <td onclick="sortTable(3, 'especifictable')" class="header"><strong>Problema</strong></td>
                    <td onclick="sortTable(4, 'especifictable')" class="header"><strong>Estado</strong></td>
            `
            for (let date in dates) {
                especific_head += `<td class="header"><strong>`+ dates[date] +`</strong></td>`
            }
            especific_head += `</tr></thead><tbody>`

            especific_body = ''
            if (select.value == 'hours') {
                for (let e_value in especific_values) {
                    especific_body += `<tr>
                    <td><a href="/detail/`+ especific_values[e_value][0] +`" target= "_blank">`+ especific_values[e_value][0] +`</a></td>`
                    
                    for (let j in especific_values[e_value]) {
                        if (j != 0){
                            especific_body += `<td>`+ especific_values[e_value][j] +`</td>`
                        }
                    }
                    for (let k in hours_values[e_value]){
                        especific_body += `<td>`+ hours_values[e_value][k] +`</td>`
                    }
                }
                especific_body += `</tbody></table>`
                div_especifictable.innerHTML = especific_head + especific_body

            } else if (select.value == 'period') {
                for (let e_value in especific_values) {
                    especific_body += `<tr>
                    <td><a href="/detail/`+ especific_values[e_value][0] +`" target= "_blank">`+ especific_values[e_value][0] +`</a></td>`
                    
                    for (let j in especific_values[e_value]) {
                        if (j != 0){
                            especific_body += `<td>`+ especific_values[e_value][j] +`</td>`
                        }
                    }
                    for (let k in period_values[e_value]){
                        especific_body += `<td>`+ period_values[e_value][k] +`</td>`
                    }
                }
                especific_body += `</tbody></table>`
                div_especifictable.innerHTML = especific_head + especific_body
            } else if (select.value == 'qoe') {
                for (let e_value in especific_values) {
                    especific_body += `<tr>
                    <td><a href="/detail/`+ especific_values[e_value][0] +`" target= "_blank">`+ especific_values[e_value][0] +`</a></td>`
                    
                    for (let j in especific_values[e_value]) {
                        if (j != 0){
                            especific_body += `<td>`+ especific_values[e_value][j] +`</td>`
                        }
                    }
                    for (let k in qoe_values[e_value]){
                        especific_body += `<td>`+ qoe_values[e_value][k] +`</td>`
                    }
                }
                especific_body += `</tbody></table>`
                div_especifictable.innerHTML = especific_head + especific_body
            }
        })
    } else {

        div_generaltable.innerHTML = data.msg
        div_especifictable.innerHTML = data.msg
    }
}