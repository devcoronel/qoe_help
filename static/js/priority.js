let div_generaltable = document.getElementById("div_generaltable")
let div_especifictable = document.getElementById("div_especifictable")

function build(data) {
    if(typeof(data.msg) === 'object') {
        let mydata = data.msg
        let general_values = mydata[0]
        let qoe_values = mydata[1]
        let hours_values = mydata[2]
        let period_values = mydata[3]
        let modulation_values = mydata[4]
        let dates = mydata[5]

        // TABLA GENERAL

        let general_table = `
            <table id="generaltable" class="table table-hover" data-excel-name="General_Priority">
            <thead class="table-dark">
                <tr>
                    <td onclick="sortTable(0,'generaltable')" class="header"><strong>CMTS</strong></td>
                    <td onclick="sortTable(1,'generaltable')" class="header"><strong>Plano</strong></td>
                    <td onclick="sortTable(2,'generaltable')" class="header"><strong>Dependencia</strong></td>
                    <td onclick="sortTable(3,'generaltable')" class="header"><strong>Impedimento</strong></td>
                    <td onclick="sortTable(4,'generaltable')" class="header"><strong>Revisión</strong></td>
                    <td onclick="sortTable(5,'generaltable')" class="header"><strong>Tipo</strong></td>
                    <td onclick="sortTable(6,'generaltable')" class="header"><strong>Días</strong></td>
                    <td onclick="sortTable(7,'generaltable')" class="header"><strong>Problema</strong></td>
                    <td onclick="sortTable(8,'generaltable')" class="header"><strong>Estado</strong></td>
                    <td onclick="sortTable(9,'generaltable')" class="header"><strong>Detalle</strong></td>
                </tr>
            </thead>
            <tbody>
        `
        for (let value in general_values) {
            general_table += `<tr>`
            general_table += `<td>`+ general_values[value][0] +`</td>`
            general_table += `<td><a href="/detail/`+ general_values[value][1] +`" target= "_blank">`+ general_values[value][1] +`</a></td>`
            for (let i in general_values[value]) {
                if (!(i == 0 || i == 1)) {
                    general_table += `<td>`+ general_values[value][i] +`</td>`
                }
            }
            general_table += `</tr>`
        }
        general_table += `</tbody></table>`
        div_generaltable.innerHTML = general_table

        // TABLA ESPECIFICA

        let especific_head = `
        <table id="especifictable" class="table table-hover" data-excel-name="Especific_Priority">
        <thead class="table-dark">
            <tr>
                <td onclick="sortTable(0, 'especifictable')" class="header"><strong>CMTS</strong></td>
                <td onclick="sortTable(1, 'especifictable')" class="header"><strong>Plano</strong></td>
                <td onclick="sortTable(2, 'especifictable')" class="header"><strong>Tipo</strong></td>
                <td onclick="sortTable(3, 'especifictable')" class="header"><strong>Días</strong></td>
                <td onclick="sortTable(4, 'especifictable')" class="header"><strong>Problema</strong></td>
                <td onclick="sortTable(5, 'especifictable')" class="header"><strong>Estado</strong></td>
        `
        for (let date in dates) {
            especific_head += `<td class="header"><strong>`+ dates[date] +`</strong></td>`
        }
        especific_head += `</tr></thead><tbody>`
        
        let select = document.getElementById("type")
        div_especifictable.innerHTML = especific_head
        let especific_body = ``

        if (select.value == 'qoe') {
            for (let e_value in qoe_values) {
                especific_body += `<tr>
                <td>`+ qoe_values[e_value][0] +`</td>
                <td><a href="/detail/`+ qoe_values[e_value][1] +`" target= "_blank">`+ qoe_values[e_value][1] +`</a></td>
                <td>` + qoe_values[e_value][2] + `</td>
                <td>` + qoe_values[e_value][3] + `</td>
                <td>` + qoe_values[e_value][4] + `</td>
                <td>` + qoe_values[e_value][5] + `</td>
                `
                
                for (let i in qoe_values[e_value]) {
                    if (i > 5) {
                        if (qoe_values[e_value][i] > 80) {
                            especific_body += `<td style="background-color: 70EC66;">`+ qoe_values[e_value][i] +`</td>`
                        } else if (qoe_values[e_value][i] >= 70) {
                            especific_body += `<td style="background-color: F3DE5B">`+ qoe_values[e_value][i] +`</td>`
                        } else if (qoe_values[e_value][i] >= 0){
                            especific_body += `<td style="background-color: FB7D4D">`+ qoe_values[e_value][i] +`</td>`
                        } else {
                            especific_body += `<td>`+ qoe_values[e_value][i] +`</td>`
                        }
                    }
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
                    <td onclick="sortTable(0, 'especifictable')" class="header"><strong>CMTS</strong></td>
                    <td onclick="sortTable(1, 'especifictable')" class="header"><strong>Plano</strong></td>
                    <td onclick="sortTable(2, 'especifictable')" class="header"><strong>Tipo</strong></td>
                    <td onclick="sortTable(3, 'especifictable')" class="header"><strong>Días</strong></td>
                    <td onclick="sortTable(4, 'especifictable')" class="header"><strong>Problema</strong></td>
                    <td onclick="sortTable(5, 'especifictable')" class="header"><strong>Estado</strong></td>
            `
            for (let date in dates) {
                especific_head += `<td class="header"><strong>`+ dates[date] +`</strong></td>`
            }
            especific_head += `</tr></thead><tbody>`
            

            especific_body = ''
            if (select.value == 'hours') {
                for (let e_value in hours_values) {
                    especific_body += `<tr>
                    <td>`+ hours_values[e_value][0] +`</td>
                    <td><a href="/detail/`+ hours_values[e_value][1] +`" target= "_blank">`+ hours_values[e_value][1] +`</a></td>
                    <td>` + hours_values[e_value][2] + `</td>
                    <td>` + hours_values[e_value][3] + `</td>
                    <td>` + hours_values[e_value][4] + `</td>
                    <td>` + hours_values[e_value][5] + `</td>
                    `
                    
                    for (let i in hours_values[e_value]) {
                        if (i > 5) {
                            if (hours_values[e_value][i] > 6) {
                                especific_body += `<td style="background-color: FB7D4D;">`+ hours_values[e_value][i] +`</td>`
                            } else if (hours_values[e_value][i] >= 3) {
                                especific_body += `<td style="background-color: F3DE5B">`+ hours_values[e_value][i] +`</td>`
                            } else if (hours_values[e_value][i] >= 0){
                                especific_body += `<td style="background-color: 70EC66">`+ hours_values[e_value][i] +`</td>`
                            } else {
                                especific_body += `<td>`+ hours_values[e_value][i] +`</td>`
                            }
                        }
                    }
                }
                especific_body += `</tbody></table>`
                div_especifictable.innerHTML = especific_head + especific_body

            } else if (select.value == 'period') {
                for (let e_value in period_values) {
                    especific_body += `<tr>
                    <td>`+ period_values[e_value][0] +`</td>
                    <td><a href="/detail/`+ period_values[e_value][1] +`" target= "_blank">`+ period_values[e_value][1] +`</a></td>
                    <td>` + period_values[e_value][2] + `</td>
                    <td>` + period_values[e_value][3] + `</td>
                    <td>` + period_values[e_value][4] + `</td>
                    <td>` + period_values[e_value][5] + `</td>
                    `
                    
                    for (let i in period_values[e_value]) {
                        if (i > 5) {
                            if (period_values[e_value][i] == 'DIA') {
                                especific_body += `<td style="background-color: 7BE0EA;">`+ period_values[e_value][i] +`</td>`
                            } else if (period_values[e_value][i] == 'NOCHE') {
                                especific_body += `<td style="background-color: 647EB9">`+ period_values[e_value][i] +`</td>`
                            } else if (period_values[e_value][i] == 'TODO EL DIA'){
                                especific_body += `<td style="background-color: FB7D4D">`+ period_values[e_value][i] +`</td>`
                            } else if (period_values[e_value][i] == 'MADRUGADA'){
                                especific_body += `<td style="background-color: F3DE5B">`+ period_values[e_value][i] +`</td>`
                            } else {
                                especific_body += `<td>`+ period_values[e_value][i] +`</td>`
                            }
                        }
                    }
                }
                especific_body += `</tbody></table>`
                div_especifictable.innerHTML = especific_head + especific_body

            } else if (select.value == 'modulation') {
                for (let e_value in modulation_values) {
                    especific_body += `<tr>
                    <td>`+ modulation_values[e_value][0] +`</td>
                    <td><a href="/detail/`+ modulation_values[e_value][1] +`" target= "_blank">`+ modulation_values[e_value][1] +`</a></td>
                    <td>` + modulation_values[e_value][2] + `</td>
                    <td>` + modulation_values[e_value][3] + `</td>
                    <td>` + modulation_values[e_value][4] + `</td>
                    <td>` + modulation_values[e_value][5] + `</td>
                    `
                    
                    for (let i in modulation_values[e_value]) {
                        if (i > 5) {
                            if (modulation_values[e_value][i] >= 4) {
                                especific_body += `<td style="background-color: FB7D4D;">`+ modulation_values[e_value][i] +`</td>`
                            } else if (modulation_values[e_value][i] >= 1) {
                                especific_body += `<td style="background-color: F3DE5B">`+ modulation_values[e_value][i] +`</td>`
                            } else {
                                especific_body += `<td style="background-color: 70EC66">`+ modulation_values[e_value][i] +`</td>`
                            }
                        }
                    }
                }
                especific_body += `</tbody></table>`
                div_especifictable.innerHTML = especific_head + especific_body

            } else if (select.value == 'qoe') {
                for (let e_value in qoe_values) {
                    especific_body += `<tr> 
                    <td>`+ qoe_values[e_value][0] +`</td>
                    <td><a href="/detail/`+ qoe_values[e_value][1] +`" target= "_blank">`+ qoe_values[e_value][1] +`</a></td>
                    <td>` + qoe_values[e_value][2] + `</td>
                    <td>` + qoe_values[e_value][3] + `</td>
                    <td>` + qoe_values[e_value][4] + `</td>
                    <td>` + qoe_values[e_value][5] + `</td>
                    `
                    
                    for (let i in qoe_values[e_value]) {
                        if (i > 5) {
                            if (qoe_values[e_value][i] > 80) {
                                especific_body += `<td style="background-color: 70EC66;">`+ qoe_values[e_value][i] +`</td>`
                            } else if (qoe_values[e_value][i] >= 70) {
                                especific_body += `<td style="background-color: F3DE5B">`+ qoe_values[e_value][i] +`</td>`
                            } else if (qoe_values[e_value][i] >= 0){
                                especific_body += `<td style="background-color: FB7D4D">`+ qoe_values[e_value][i] +`</td>`
                            } else {
                                especific_body += `<td>`+ qoe_values[e_value][i] +`</td>`
                            }
                        }
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