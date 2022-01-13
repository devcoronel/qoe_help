let load = document.getElementById("loading");
let table = document.getElementById("div_dayly_table");
let statistics = document.getElementById("div_statistics")
let alert = document.getElementById("alert")
const myform = document.getElementById("form_sumary");


myform.addEventListener("submit", function (e) {
	e.preventDefault();
	table.innerHTML = ''
	statistics.innerHTML = ''
	load.innerHTML = `
		<div class="spinner-border text-primary" role="status">
		<span class="visually-hidden">Loading...</span>
		</div>
	`
	const formData = new FormData(this);
	myform.reset()

	fetch("/dayly" , {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {
			if(typeof(data.msg) === 'object') {
				alert.innerHTML = ''
				
				let elements = data.msg[0]
				
				let tablehtml = `
				<div class="accordion accordion-flush" id="accordionFlushExample">
                    <div class="accordion-item" style="background-color: F2F5FA;">
                      <h2 class="accordion-header" id="flush-headingTwo">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo" style="background-color: EDF0F5;">
                            <div>
                                <h4 class="fw-bold">Tabla Diaria `+ formData.get('dayly_date') +` - Región `+ formData.get('region') +`</h4>
                            </div>
                        </button>
                      </h2>
                      <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo" data-bs-parent="#accordionFlushExample">
                        <div class="accordion-body">
							<div style="display: flex ;justify-content: right;">
								<button id="daylybutton" class="btn btn-success" style="margin-bottom: 2rem;">Exportar</button>
							</div>
                            <div class="scrollmenu" style="border-radius:10px;">
							
                <table class="table table-hover" id="daylytable">
                <thead class="table-dark">
                <td onclick="sortTable(0, 'daylytable')" class="header"><strong>CMTS</strong></td>
                <td onclick="sortTable(1, 'daylytable')" class="header"><strong>Plano</strong></td>
				<td onclick="sortTable(2, 'daylytable')" class="header"><strong>QoE</strong></td>
				<td onclick="sortTable(3, 'daylytable')" class="header"><strong>CMs Afectados</strong></td>
				<td onclick="sortTable(4, 'daylytable')" class="header"><strong>CMs Estresados</strong></td>
				<td onclick="sortTable(5, 'daylytable')" class="header"><strong>Horas</strong></td>
				<td onclick="sortTable(6, 'daylytable')" class="header"><strong>Periodo</strong></td>
				<td onclick="sortTable(7, 'daylytable')" class="header"><strong>Cambio Modulación</strong></td>
				<td onclick="sortTable(8, 'daylytable')" class="header"><strong>Días</strong></td>
				<td onclick="sortTable(9, 'daylytable')" class="header"><strong>Prioridad</strong></td>`
				tablehtml += '</thead><tbody>'
				
				let cA = []
				let cB = []
				let cC = []
				let cD = []
				let cE = []

				let periodM = []
				let periodD = []
				let periodN = []
				let periodT = []
				let periodI = []
				let periodNo = []
				let periodMod = []

				let cA_greaterThan150 = []
				let cA_between50and150 = []
				let cA_between20and50 = []
				let cA_lessThan20 = []

				var cB_greaterThan150 = []
				let cB_between50and150 = []
				let cB_between20and50 = []
				let cB_lessThan20 = []

				let cC_greaterThan150 = []
				let cC_between50and150 = []
				let cC_between20and50 = []
				let cC_lessThan20 = []

				let cD_greaterThan150 = []
				let cD_between50and150 = []
				let cD_between20and50 = []
				let cD_lessThan20 = []
				
				for(let i in elements){

					tablehtml += `<tr>
					<td>`+ elements[i][0] +`</td>
					<td><a href="/detail/`+ elements[i][1] +`" target= "_blank">`+ elements[i][1] +`</a></td>
					<td>`+ elements[i][2] +`</td>
					<td>`+ elements[i][3] +`</td>
					<td>`+ elements[i][4] +`</td>
					<td>`+ elements[i][5] +`</td>
					<td>`+ elements[i][6] +`</td>
					<td>`+ elements[i][7] +`</td>
					<td>`+ elements[i][8] +`</td>`

					if (elements[i][2] < 70 && elements[i][2] >= 0) {
						cA.push(i)
						tablehtml += `<td>Con Afectación</td></tr>`
					} else if (elements[i][2] >= 70 && elements[i][2] < 80) {
						cC.push(i)
						tablehtml += `<td>Preventivo</td></tr>`
					} else if (elements[i][5] >= 3) {
						cB.push(i)
						tablehtml += `<td>Con Afectación</td></tr>`
					} else if (elements[i][7] >= 2 && elements[i][5] >= 0) {
						cD.push(i)
						tablehtml += `<td>Preventivo</td></tr>`
					} else {
						cE.push(i)
						tablehtml += `<td>Monitoreo</td></tr>`
					}

					if (elements[i][6] == 'MADRUGADA') {
						periodM.push(i)
					} else if (elements[i][6] == 'DIA') {
						periodD.push(i)
					} else if (elements[i][6] == 'NOCHE') {
						periodN.push(i)
					} else if (elements[i][6] == 'TODO EL DIA') {
						periodT.push(i)
					} else if (elements[i][6] == 'INTERMITENTE') {
						periodI.push(i)
					} else if (elements[i][6] == 'NO AFECTADO') {
						if (elements[i][7] >= 2 && elements[i][5] >= 0) {
							periodMod.push(i)
						} else {
							periodNo.push(i)
						}
					}
				}

				for (let j in cA) {

					if(elements[cA[j]][3] > 150){
						cA_greaterThan150.push(cA[j])
					} else if(elements[cA[j]][3] > 50 && elements[cA[j]][3] <= 150){
						cA_between50and150.push(cA[j])
					} else if(elements[cA[j]][3] > 20 && elements[cA[j]][3] <= 50){
						cA_between20and50.push(cA[j])
					} else if(elements[cA[j]][3] <= 20){
						cA_lessThan20.push(cA[j])
					}
				}

				for (let k in cB) {

					if(elements[cB[k]][3] > 150){
						cB_greaterThan150.push(cB[k])
					} else if(elements[cB[k]][3] > 50 && elements[cB[k]][3] <= 150){
						cB_between50and150.push(cB[k])
					} else if(elements[cB[k]][3] > 20 && elements[cB[k]][3] <= 50){
						cB_between20and50.push(cB[k])
					} else if(elements[cB[k]][3] <= 20){
						cB_lessThan20.push(cB[k])
					}

				}
				for (let l in cC) {

					if(elements[cC[l]][3] > 150){
						cC_greaterThan150.push(cC[l])
					} else if(elements[cC[l]][3] > 50 && elements[cC[l]][3] <= 150){
						cC_between50and150.push(cC[l])
					} else if(elements[cC[l]][3] > 20 && elements[cC[l]][3] <= 50){
						cC_between20and50.push(cC[l])
					} else if(elements[cC[l]][3] <= 20){
						cC_lessThan20.push(cC[l])
					}

				}
				for (let m in cD) {
					
					if(elements[cD[m]][3] > 150){
						cD_greaterThan150.push(cD[m])
					} else if(elements[cD[m]][3] > 50 && elements[cD[m]][3] <= 150){
						cD_between50and150.push(cD[m])
					} else if(elements[cD[m]][3] > 20 && elements[cD[m]][3] <= 50){
						cD_between20and50.push(cD[m])
					} else if(elements[cD[m]][3] <= 20){
						cD_lessThan20.push(cD[m])
					}

				}

				let claseList = [cA.length, cB.length, cC.length, cD.length]
				let periodList = [periodM.length, periodD.length, periodN.length, periodT.length, periodI.length, periodMod.length]
				let sumPeriodPlanes = periodM.length + periodD.length + periodN.length + periodT.length + periodI.length + periodMod.length

				// console.log("qoe < 70: "+cA.length)
				// console.log("horas >= 3: "+cB.length)
				// console.log("qoe entre 70 y 80: "+cC.length)
				// console.log("modulacion: "+cD.length)
				// console.log("no afectado: "+cE.length)


				tablehtml += `</tbody></table>
				</div>
                        </div>
                      </div>
                    </div>
				</div>`
				
				load.innerHTML = ''
				table.innerHTML = tablehtml

				let body_statistics = `
				<hr>
				<div class="row">
                    <div class="col-sm-10 col-md-9 col-9">
                        <h2 class="fw-bold"> <img src="../static/images/aboutme/i.png" width="35" class="pb-2">&nbspEstadística</h2>
                    </div>
                </div>
				`
				statistics.innerHTML = body_statistics
				statistics.innerHTML += `
				<div class="container">
				<div class="row container">
                    <div class="col-4 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
						<h4 style="padding:0.5rem;text-align:center">Total Planos por Tipo de Afectación</h4>
                        <canvas id="canvas1"></canvas>
                    </div>
                    <div class="col-7 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
						<h4 style="padding:0.5rem;text-align:center">Total Planos por Periodo de Afectación</h4>
                        <canvas id="canvas2" style="padding:1rem"></canvas>
						<h6 style="padding:0.5rem;text-align:center">Total Planos = `+ sumPeriodPlanes +`</h6>
                    </div>
				</div>
				</div>
				<div class="container">
				<div class="row container">
					<div class="col-12" style="background-color:#EBEDEF; border-radius: 1.5rem;">
						<h4 style="padding:0.5rem;text-align:center">Tipo de Afectación por cantidad de Clientes Afectados</h4>
						<div id="impactedByTypeTable"></div>
					</div>
				</div>
				</hr>
				</div>

				<div data-bs-backdrop="static" class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
				<div class="modal-dialog modal-dialog-scrollable">
				<div class="modal-dialog">
					<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="modalTitle">Modal title</h5>
						<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
					</div>
					<div class="modal-body" id="modalBody">
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-primary" data-bs-dismiss="modal">OK</button>
					</div>
					</div>
				</div>
				</div>
				</div>

				<div class="container">
				<div class="row container">
                    <div class="col-5 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
						<h4 style="padding:0.5rem;text-align:center">Planos Afectados con más de 150 Clientes</h4>
                        <canvas id="canvas3"></canvas>
                    </div>
                    <div class="col-5 m-2" style="background-color:#EBEDEF; border-radius: 1.5rem;">
						<h4 style="padding:0.5rem;text-align:center">Planos Afectados de 50 a 150 Clientes</h4>
                        <canvas id="canvas4" style="padding:1rem"></canvas>
                    </div>
				</div>
				</div>`


				let canvas1 = document.getElementById("canvas1").getContext("2d")
				var chart1 = new Chart(canvas1, {
					type: "pie",
					data: {
						labels: ["QoE < 70","Horas ≥ 3","70 ≤ QoE < 80","Cambios de Mod ≥ 2"],
						datasets:[
							{
								backgroundColor: [
									'rgba(231, 76, 60, 0.5)',
									'rgba(230, 126, 34, 0.5)',
									'rgba(241, 196, 15, 0.5)',
									'rgba(88, 214, 141, 0.5)'
								],
								data: claseList
							}
						]
					},
					options:{
						plugins:{
							legend: {
								position: 'bottom'
							},
							labels:{
								render: (context) => {
									const percentage = context.value / showData(chart1) *100
									return percentage.toFixed(0)+'%'
								},
								fontColor: '#fff',
								shadowColor: '#fff'
							},
						},
					},
				})
				function showData(chart){
					let totalsum = 0
					let i = 0
					for (i; i < chart.config.data.datasets[0].data.length; i++){
						if (chart.getDataVisibility(i) === true){
							totalsum += chart.config.data.datasets[0].data[i]
						}
					}
					return totalsum
				}

				

				let canvas2 = document.getElementById("canvas2").getContext("2d")
				var chart2 = new Chart(canvas2, {
					type: "bar",
					data: {
						labels: ["MADRUGADA", "DIA", "NOCHE", "TODO EL DÍA", "INTERMITENTE", "MODULACIÓN"],
						datasets:[
							{
								label:"Periodo",
								backgroundColor: [
									'rgba(241, 196, 15, 0.5)', // amarillo
									'rgba(52, 152, 219, 0.5)', // azul
									'rgba(52, 73, 94, 0.5)', // azul oscuro
									'rgba(231, 76, 60, 0.5)', //rojo
									'rgba(142, 68, 173, 0.5)', // morado
									'rgba(88, 214, 141, 0.5)' // verde
									// 'rgba(189, 195, 199, 0.5)' // gris
								],
								data: periodList
							}
						]
					},
					options: {
						indexAxis: 'y',
						plugins:{
							labels:{
								render: 'value'
							}
						},
						scales: {
							y: {
								beginAtZero: true
							}
						}
					}
				})				


				let impactedByTypeTable = document.getElementById("impactedByTypeTable")
				let impactedByTypeTableHTML = '<div class="scrollmenu" style="border-radius:10px;"><table class="table table-hover"><thead  class="table-dark">'
				impactedByTypeTableHTML += `
				<tr>
					<td></td>
					<td></td>
					<td>Prioridad 1</td>
					<td>Prioridad 2</td>
					<td>Prioridad 3</td>
					<td>Prioridad 4</td>
					<td>Total General</td>
				</tr>
				<tr>
					<td>Estado de plano</td>
					<td>Estado</td>
					<td>150 < CMs Afectados</td>
					<td>50 < CMs Afectados ≤ 150</td>
					<td>20 < CMs Afectados ≤ 50</td>
					<td>CMs Afectados ≤ 20</td>
					<td></td>
				</tr>
				</thead>
				<tbody>
				<tr>
					<td rowspan="2">Con Afectación</td>
					<td>QoE < 70</td>
					<td id="t22">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cA_greaterThan150.length +`
						</button>
					</td>
					<td id="t23">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cA_between50and150.length +`
						</button>
					</td>
					<td id="t24">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cA_between20and50.length +`
						</button>
					</td>
					<td id="t25">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cA_lessThan20.length +`
						</button>
					</td>
					<td>`+ (cA_greaterThan150.length + cA_between50and150.length + cA_between20and50.length + cA_lessThan20.length) +`</td>
				</tr>
				<tr>
					<td>Horas ≥ 3</td>
					<td id="t32">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cB_greaterThan150.length +`
						</button>
					</td>
					<td id="t33">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cB_between50and150.length +`
						</button>
					</td>
					<td id="t34">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cB_between20and50.length +`
						</button>
					</td>
					<td id="t35">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cB_lessThan20.length +`
						</button>
					</td>
					<td>`+ (cB_greaterThan150.length + cB_between50and150.length + cB_between20and50.length + cB_lessThan20.length) +`</td>
				</tr>
				<tr>
					<td>Total</td>
					<td></td>
					<td>`+ (cA_greaterThan150.length + cB_greaterThan150.length) +`</td>
					<td>`+ (cA_between50and150.length + cB_between50and150.length) +`</td>
					<td>`+ (cA_between20and50.length + cB_between20and50.length) +`</td>
					<td>`+ (cA_lessThan20.length + cB_lessThan20.length) +`</td>
					<td>`+ (cA_greaterThan150.length + cA_between50and150.length + cA_between20and50.length + cA_lessThan20.length + cB_greaterThan150.length + cB_between50and150.length + cB_between20and50.length + cB_lessThan20.length) +`</td>
				</tr>

				<tr>
					<td rowspan="2">Preventivo</td>
					<td>70 ≤ QoE < 80</td>
					<td id="t42">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cC_greaterThan150.length +`
						</button>
					</td>
					<td id="t43">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cC_between50and150.length +`
						</button>
					</td>
					<td id="t44">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cC_between20and50.length +`
						</button>
					</td>
					<td id="t45">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cC_lessThan20.length +`
						</button>
					</td>
					<td>`+ (cC_greaterThan150.length + cC_between50and150.length + cC_between20and50.length + cC_lessThan20.length) +`</td>
				</tr>
				<tr>
					<td>Cambios de Modul ≥ 2</td>
					<td id="t52">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cD_greaterThan150.length +`
						</button>
					</td>
					<td id="t53">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cD_between50and150.length +`
						</button>
					</td>
					<td id="t54">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cD_between20and50.length +`
						</button>
					</td>
					<td id="t55">
						<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
						`+ cD_lessThan20.length +`
						</button>
					</td>
					<td>`+ (cD_greaterThan150.length + cD_between50and150.length + cD_between20and50.length + cD_lessThan20.length) +`</td>
				</tr>
				<tr>
					<td>Total</td>
					<td></td>
					<td>`+ (cC_greaterThan150.length + cD_greaterThan150.length) +`</td>
					<td>`+ (cC_between50and150.length + cD_between50and150.length) +`</td>
					<td>`+ (cC_between20and50.length + cD_between20and50.length) +`</td>
					<td>`+ (cC_lessThan20.length + cD_lessThan20.length) +`</td>
					<td>`+ (cC_greaterThan150.length + cC_between50and150.length + cC_between20and50.length + cC_lessThan20.length + cD_greaterThan150.length + cD_between50and150.length + cD_between20and50.length + cD_lessThan20.length) +`</td>
				</tr>
				<tr>
					<td>Total General</td>
					<td></td>
					<td>`+ (cA_greaterThan150.length + cB_greaterThan150.length + cC_greaterThan150.length + cD_greaterThan150.length) +`</td>
					<td>`+ (cA_between50and150.length + cB_between50and150.length + cC_between50and150.length + cD_between50and150.length) +`</td>
					<td>`+ (cA_between20and50.length + cB_between20and50.length + cC_between20and50.length + cD_between20and50.length) +`</td>
					<td>`+ (cA_lessThan20.length + cB_lessThan20.length + cC_lessThan20.length + cD_lessThan20.length) +`</td>
					<td>`+ (cA_greaterThan150.length + cB_greaterThan150.length + cC_greaterThan150.length + cD_greaterThan150.length + cA_between50and150.length + cB_between50and150.length + cC_between50and150.length + cD_between50and150.length + cA_between20and50.length + cB_between20and50.length + cC_between20and50.length + cD_between20and50.length + cA_lessThan20.length + cB_lessThan20.length + cC_lessThan20.length + cD_lessThan20.length) +`</td>
					
				</tr>
				</div>
				`
				impactedByTypeTable.innerHTML = impactedByTypeTableHTML


				let modalTitle = document.getElementById("modalTitle")
				let modalBody = document.getElementById("modalBody")

				function createModalTable(indexList){
					let modalTable = `
					<table class="table table-hover">
					<thead>
						<tr>
							<td>Plano</td>
							<td>Días</td>
						</tr>
					</thead>
					<tbody>`
					for (let a in indexList) {
						modalTable += `
						<tr>
							<td>`+ elements[indexList[a]][1] +`</td>
							<td>`+ elements[indexList[a]][8] +`</td>
						</tr>
						`
					}
					modalTable += `</tbody></table>`
					modalBody.innerHTML = modalTable
				}
				
				let t22 = document.getElementById("t22")
				t22.addEventListener("click", function(){
					modalTitle.innerHTML = "QoE < 70 | 150 < CMs Afectados"
					if (cA_greaterThan150.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cA_greaterThan150)
					}
				})
				let t23 = document.getElementById("t23")
				t23.addEventListener("click", function(){
					modalTitle.innerHTML = "QoE < 70 | 50 < CMs Afectados ≤ 150"
					if (cA_between50and150.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cA_between50and150)
					}
				})
				let t24 = document.getElementById("t24")
				t24.addEventListener("click", function(){
					modalTitle.innerHTML = "QoE < 70 | 20 < CMs Afectados ≤ 50"
					if (cA_between20and50.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cA_between20and50)
					}
				})
				let t25 = document.getElementById("t25")
				t25.addEventListener("click", function(){
					modalTitle.innerHTML = "QoE < 70 | CMs Afectados ≤ 20"
					if (cA_lessThan20.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cA_lessThan20)
					}
				})


				let t32 = document.getElementById("t32")
				t32.addEventListener("click", function(){
					modalTitle.innerHTML = "Horas ≥ 3 | 150 < CMs Afectados"
					if (cB_greaterThan150.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cB_greaterThan150)
					}
				})
				let t33 = document.getElementById("t33")
				t33.addEventListener("click", function(){
					modalTitle.innerHTML = "Horas ≥ 3 | 50 < CMs Afectados ≤ 150"
					if (cB_between50and150.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cB_between50and150)
					}
				})
				let t34 = document.getElementById("t34")
				t34.addEventListener("click", function(){
					modalTitle.innerHTML = "Horas ≥ 3 | 20 < CMs Afectados ≤ 50"
					if (cB_between20and50.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cB_between20and50)
					}
				})
				let t35 = document.getElementById("t35")
				t35.addEventListener("click", function(){
					modalTitle.innerHTML = "Horas ≥ 3 | CMs Afectados ≤ 20"
					if (cB_lessThan20.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cB_lessThan20)
					}
				})


				let t42 = document.getElementById("t42")
				t42.addEventListener("click", function(){
					modalTitle.innerHTML = "70 ≤ QoE < 80 | 150 < CMs Afectados"
					if (cC_greaterThan150.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cC_greaterThan150)
					}
				})
				let t43 = document.getElementById("t43")
				t43.addEventListener("click", function(){
					modalTitle.innerHTML = "70 ≤ QoE < 80 | 50 < CMs Afectados ≤ 150"
					if (cC_between50and150.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cC_between50and150)
					}
				})
				let t44 = document.getElementById("t44")
				t44.addEventListener("click", function(){
					modalTitle.innerHTML = "70 ≤ QoE < 80 | 20 < CMs Afectados ≤ 50"
					if (cC_between20and50.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cC_between20and50)
					}
				})
				let t45 = document.getElementById("t45")
				t45.addEventListener("click", function(){
					modalTitle.innerHTML = "70 ≤ QoE < 80 | CMs Afectados ≤ 20"
					if (cC_lessThan20.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cC_lessThan20)
					}
				})


				let t52 = document.getElementById("t52")
				t52.addEventListener("click", function(){
					modalTitle.innerHTML = "Cambios Modul ≥ 2 | 150 < CMs Afectados"
					if (cD_greaterThan150.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cD_greaterThan150)
					}
				})
				let t53 = document.getElementById("t53")
				t53.addEventListener("click", function(){
					modalTitle.innerHTML = "Cambios Modul ≥ 2 | 50 < CMs Afectados ≤ 150"
					if (cD_between50and150.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cD_between50and150)
					}
				})
				let t54 = document.getElementById("t54")
				t54.addEventListener("click", function(){
					modalTitle.innerHTML = "Cambios Modul ≥ 2 | 20 < CMs Afectados ≤ 50"
					if (cD_between20and50.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cD_between20and50)
					}
				})
				let t55 = document.getElementById("t55")
				t55.addEventListener("click", function(){
					modalTitle.innerHTML = "Cambios Modul ≥ 2 | CMs Afectados ≤ 20"
					if (cD_lessThan20.length == 0) {
						modalBody.innerHTML = "No hay planos por mostrar"
					} else {
						createModalTable(cD_lessThan20)
					}
				})





				//Clase A: QoE < 70
				// Clase B: Horas ≥ 3
				// Clase C: 70 ≤ QoE < 80
				// Clase D: Cambios de Modulación ≥ 2
				// Clase E: No afectado en la fecha


				let allGreaterThan150 = ((cA_greaterThan150.concat(cB_greaterThan150)).concat(cC_greaterThan150)).concat(cD_greaterThan150)
				let greaterThan150Day = []
				let greaterThan150Night = []
				let greaterThan150AllDay = []
				let greaterThan150EarlyMorning = []
				let greaterThan150Intermittent = []
				let greaterThan150NotAffected = []

				for(let n in allGreaterThan150){
					if(elements[allGreaterThan150[n]][6] == 'DIA'){
						greaterThan150Day.push(allGreaterThan150[n])
					} else if(elements[allGreaterThan150[n]][6] == 'NOCHE'){
						greaterThan150Night.push(allGreaterThan150[n])
					} else if(elements[allGreaterThan150[n]][6] == 'TODO EL DIA'){
						greaterThan150AllDay.push(allGreaterThan150[n])
					} else if(elements[allGreaterThan150[n]][6] == 'MADRUGADA'){
						greaterThan150EarlyMorning.push(allGreaterThan150[n])
					} else if(elements[allGreaterThan150[n]][6] == 'INTERMITENTE'){
						greaterThan150Intermittent.push(allGreaterThan150[n])
					} else if(elements[allGreaterThan150[n]][6] == 'NO AFECTADO'){
						greaterThan150NotAffected.push(allGreaterThan150[n])
					}
				}

				let greaterThan150PeriodList = [greaterThan150EarlyMorning.length, greaterThan150Day.length, greaterThan150Night.length, greaterThan150AllDay.length, greaterThan150Intermittent.length, greaterThan150NotAffected.length]

				let canvas3 = document.getElementById("canvas3").getContext("2d")
				var chart3 = new Chart(canvas3, {
					type: "bar",
					data: {
						labels: ["MADRUGADA", "DIA", "NOCHE", "TODO EL DÍA", "INTERMITENTE", "NO AFECTADO"],
						datasets:[
							{
								label:"Periodo",
								backgroundColor: [
									'rgba(241, 196, 15, 0.5)', // amarillo
									'rgba(52, 152, 219, 0.5)', // azul
									'rgba(52, 73, 94, 0.5)', // azul oscuro
									'rgba(231, 76, 60, 0.5)', //rojo
									'rgba(142, 68, 173, 0.5)', // morado
									'rgba(88, 214, 141, 0.5)' // verde
									// 'rgba(189, 195, 199, 0.5)' // gris
								],
								data: greaterThan150PeriodList
							}
						]
					},
					options: {
						
						plugins:{
							labels:{
								render: 'value'
							}
						},
						scales: {
							y: {
								beginAtZero: true
							}
						}
					}
				})

				let all50and150 = ((cA_between50and150.concat(cB_between50and150)).concat(cC_between50and150)).concat(cD_between50and150)
				let between50and150Day = []
				let between50and150Night = []
				let between50and150AllDay = []
				let between50and150EarlyMorning = []
				let between50and150Intermittent = []
				let between50and150NotAffected = []

				for(let o in all50and150){
					if(elements[all50and150[o]][6] == 'DIA'){
						between50and150Day.push(all50and150[o])
					} else if(elements[all50and150[o]][6] == 'NOCHE'){
						between50and150Night.push(all50and150[o])
					} else if(elements[all50and150[o]][6] == 'TODO EL DIA'){
						between50and150AllDay.push(all50and150[o])
					} else if(elements[all50and150[o]][6] == 'MADRUGADA'){
						between50and150EarlyMorning.push(all50and150[o])
					} else if(elements[all50and150[o]][6] == 'INTERMITENTE'){
						between50and150Intermittent.push(all50and150[o])
					} else if(elements[all50and150[o]][6] == 'NO AFECTADO'){
						between50and150NotAffected.push(all50and150[o])
					}
				}

				let between50and150PeriodList = [between50and150EarlyMorning.length, between50and150Day.length, between50and150Night.length, between50and150AllDay.length, between50and150Intermittent.length, between50and150NotAffected.length]

				let canvas4 = document.getElementById("canvas4").getContext("2d")
				var chart4 = new Chart(canvas4, {
					type: "bar",
					data: {
						labels: ["MADRUGADA", "DIA", "NOCHE", "TODO EL DÍA", "INTERMITENTE", "NO AFECTADO"],
						datasets:[
							{
								label:"Periodo",
								backgroundColor: [
									'rgba(241, 196, 15, 0.5)', // amarillo
									'rgba(52, 152, 219, 0.5)', // azul
									'rgba(52, 73, 94, 0.5)', // azul oscuro
									'rgba(231, 76, 60, 0.5)', //rojo
									'rgba(142, 68, 173, 0.5)', // morado
									'rgba(88, 214, 141, 0.5)' // verde
									// 'rgba(189, 195, 199, 0.5)' // gris
								],
								data: between50and150PeriodList
							}
						]
					},
					options: {
						
						plugins:{
							labels:{
								render: 'value'
							}
						},
						scales: {
							y: {
								beginAtZero: true
							}
						}
					}
				})

				

				document.getElementById('daylybutton').addEventListener('click', function() {
					var table2excel = new Table2Excel();
					table2excel.export(document.querySelectorAll("#daylytable"), "Diario_"+ formData.get('dayly_date'));
				});
			}
			else{
				load.innerHTML = ''
				statistics.innerHTML = ''
				alert.innerHTML = `
				<div class="alert alert-danger alert-dismissible fade show" role="alert">
				<strong>`+ data.msg +`</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
			}
			
		})
		.catch(err => {
			console.log(err)
			load.innerHTML = ''
			statistics.innerHTML = ''
			alert.innerHTML = `
				<div class="alert alert-danger alert-dismissible fade show" role="alert">
				<strong>Ocurrió un error interno. Intente de nuevo</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
		})
	}	
);
