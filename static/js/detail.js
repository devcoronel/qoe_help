let load = document.getElementById("loading")
let table = document.getElementById("table")

const myform = document.getElementById("form_detail");

myform.addEventListener("submit", function (e) {
	e.preventDefault();
	load.innerHTML = `
		<div class="spinner-border text-primary" role="status">
		<span class="visually-hidden">Loading...</span>
		</div>
	`
    table.innerHTML = ''
	const formData = new FormData(this);

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
                                    <div class="scrollmenu">
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
                                </tbody>
                            </table>
                        </div>
                </div>
                `
                table.innerHTML = tablehtml
            } else {
                table.innerHTML = '<strong>'+ mydata +'</strong>'
            }
			
		})
		.catch(err => {
			console.log("There was an error")
			
		})
	}	
);