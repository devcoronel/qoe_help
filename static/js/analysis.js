let load = document.getElementById("loading");
let table = document.getElementById("my_table");
let alert = document.getElementById("alert")

const myform = document.getElementById("form_sumary");

myform.addEventListener("submit", function (e) {
	e.preventDefault();
	table.innerHTML = ''
	load.innerHTML = `
		<div class="spinner-border text-primary" role="status">
		<span class="visually-hidden">Loading...</span>
		</div>
	`
	const formData = new FormData(this);
	myform.reset()
	
	fetch('/analysis' , {
		method: 'POST',
		body: formData
	})	
		.then(response => response.json())
		.then(data => {
			if(typeof(data.msg[0]) === 'object') {
				alert.innerHTML = ''
                let elements = data.msg[0]
                let dates = data.msg[1]
                let id_table = data.msg[2]

                let tablehtml = `<table class="table table-hover" id="`+ id_table +`">
                <thead class="table-dark">
                <td class="header"><strong>REGION</strong></td>
                <td onclick="sortTable(1, '`+ id_table +`')" class="header"><strong>CMTS</strong></td>
                <td onclick="sortTable(2, '`+ id_table +`')" class="header"><strong>Plano</strong></td>`
                            
                for (let i in dates) {
                    let a = parseInt(i)+3
                    tablehtml += `<td onclick="sortTable(`+ a +`, '`+ id_table +`')" class="header"><strong>`+ dates[i] +`</strong></td>`
                }
                tablehtml += '</thead><tbody>'
                
                for(let i in elements){
                    tablehtml += `<td>`+ elements[i][0] +`</td>
                    <td>`+ elements[i][1] +`</td>
					<td><a href="/detail/`+ elements[i][2] +`" target= "_blank">`+ elements[i][2] +`</a></td>`
                    
                    for (j in elements[i]) {
                        if (!(j == 0 || j == 1 || j == 2)) {
                            tablehtml += '<td>'+ elements[i][j] +'</td>'
                        }
                    }
                    
                    tablehtml += '</tr>'
                        
                }
                tablehtml += '</tbody></table>'
				load.innerHTML = ''
                table.innerHTML = tablehtml

			}
			else{
				if(typeof(data.msg) === 'string') {
					load.innerHTML = ''
					alert.innerHTML = `
					<div class="alert alert-danger alert-dismissible fade show" role="alert">
					<strong>`+ data.msg +`</strong>
					<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
					</div>
					`
				} else{
					load.innerHTML = ''
					alert.innerHTML = `
					<div class="alert alert-danger alert-dismissible fade show" role="alert">
					<strong>`+ data.msg[0] +`</strong>
					<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
					</div>`
				}
			}
			
		})
		.catch(err => {
			load.innerHTML = ''
			alert.innerHTML = `
				<div class="alert alert-danger alert-dismissible fade show" role="alert">
				<strong>Ocurrió un error interno. Intente de nuevo</strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
				`
			
		})
	}	
);
