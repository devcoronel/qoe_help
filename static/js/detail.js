let load = document.getElementById("loading")
let table = document.getElementById("table")
let alert = document.getElementById("alert")
let status_node = document.getElementById("status")

const myform = document.getElementById("form_detail");

myform.addEventListener("submit", function (e) {
	e.preventDefault();
	load.innerHTML = `
		<div class="spinner-border text-primary" role="status">
		<span class="visually-hidden">Loading...</span>
		</div>`
        
    table.innerHTML = ''
    status_node.innerHTML = ''
    alert.innerHTML = ''
	const formData = new FormData(this);
    myform.reset()
    
	fetch("/detail" , {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {
			
            load.innerHTML= ""
            let mydata = data.msg

            if(typeof(mydata) === 'object'){
                let tablehtml = `
                <div class="col-xl-6 col-lg-6 col-md-6 col-sm-12 col-12">
                                    <div class="scrollmenu" style="border-radius:10px;">
                                        <table class="table table-hover" id="hourstable" data-excel-name="Horas_QoE_afectado" >
                                            <thead class="table-dark">
                                                <tr>
                                                    <td class="header"><strong>
                `+ mydata[0] +  `</strong></td> `

                for(let td in mydata[2]){
                    tablehtml +=  `<td class="header"><strong>`+ mydata[2][td] + `</strong></td>`
                }

                tablehtml += `</tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Horas</strong></td>`

                for(let i in mydata[1][0]){
                    tablehtml +=  `<td>`+ mydata[1][0][i] +`</td>`
                }
                tablehtml += `
                </tr>
                <tr>
                    <td><strong>QoE</strong></td>
                `
                for(let j in mydata[1][1]){
                    tablehtml +=  `<td>`+ mydata[1][1][j] +`</td>`
                }
                tablehtml += `
                </tr>
                <tr>
                    <td><strong>Periodo</strong></td>
                `
				for(let j in mydata[1][2]){
                    tablehtml +=  `<td>`+ mydata[1][2][j] +`</td>`
                }
                tablehtml += `
                </tr>
                <tr>
                    <td><strong>Cambios Modulación</strong></td>
                `
				for(let j in mydata[1][3]){
                    tablehtml +=  `<td>`+ mydata[1][3][j] +`</td>`
                }
                tablehtml += `
                </tr>
                <tr>
                    <td><strong>CMs Afectados</strong></td>
                `
				for(let j in mydata[1][4]){
                    tablehtml +=  `<td>`+ mydata[1][4][j] +`</td>`
                }
                tablehtml += `
                </tr>
                <tr>
                    <td><strong>CMs Estresados</strong></td>
                `
				for(let j in mydata[1][5]){
                    tablehtml +=  `<td>`+ mydata[1][5][j] +`</td>`
                }
                tablehtml += `
                </tr>
                <tr>
                    <td><strong>N° Muestras</strong></td>
                `
				for(let j in mydata[1][6]){
                    tablehtml +=  `<td>`+ mydata[1][6][j] +`</td>`
                }
                tablehtml += `
                </tr>
                                </tbody>
                            </table>
                        </div>
                </div>
                `
                table.innerHTML = tablehtml

                let table_status =
                `<div class="col-12">
                <div class="scrollmenu" style="border-radius:10px;">
                <table class="table table-hover">
                <thead class="table-dark">
                    <tr>
                        <td class="header"><strong>REGION</strong></td>
                        <td class="header"><strong>CMTS</strong></td>
                        <td class="header"><strong>Plano</strong></td>
                        <td class="header"><strong>Dependencia</strong></td>
                        <td class="header"><strong>Impedimento</strong></td>
                        <td class="header"><strong>Revisión</strong></td>
                        <td class="header"><strong>Tipo</strong></td>
                        <td class="header"><strong>Días</strong></td>
                        <td class="header"><strong>Problema</strong></td>
                        <td class="header"><strong>Estado</strong></td>
                        <td class="header"><strong>Detalle</strong></td>
                    </tr>
                </thead>
                <tbody>
                <tr>
                    <td>`+ mydata[3][0][0] +`</td>
                    <td>`+ mydata[3][0][1] +`</td>
                    <td>`+ mydata[3][0][2] +`</td>
                    <td>`+ mydata[3][0][3] +`</td>
                    <td>`+ mydata[3][0][4] +`</td>
                    <td>`+ mydata[3][0][5] +`</td>
                    <td>`+ mydata[3][0][6] +`</td>
                    <td>`+ mydata[3][0][7] +`</td>
                    <td>`+ mydata[3][0][8] +`</td>
                    <td>`+ mydata[3][0][9] +`</td>
                    <td>`+ mydata[3][0][10] +`</td>
                </tr></tbody></table></div></div>`

                status_node.innerHTML = table_status

            } else {
                alert.innerHTML = `
				<div class="alert alert-danger alert-dismissible fade show" role="alert">
				<strong>`+ mydata +`</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>`
            }

            
			
		})
		.catch(err => {
            load.innerHTML= ""
            alert.innerHTML = `
				<div class="alert alert-danger alert-dismissible fade show" role="alert">
				<strong>Ocurrió un error interno. Intente de nuevo</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
			
		})
	}	
);