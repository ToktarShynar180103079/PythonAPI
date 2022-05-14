function makeSearch(){
    const api_url = "http://127.0.0.1:8000/api/authors";
    var formEl = document.forms[0];
    var name = formEl.elements["name"].value;
    var surname = formEl.elements["surname"].value;
    let data = {
        name: name,
        lastname: surname
    }
    let fetchData = {
        method: 'POST',
        body: data,
    }
async function postdata(url, fetchData) {
    const response = await fetch(url, fetchData);
    var data = await response.json();
    console.log(data);
    if (response) {
        hideloader();
    }
    show(data);
}
// Calling that async function
postdata(api_url, fetchData);

// Function to hide the loader
function hideloader() {
    document.getElementById('loading').style.display = 'none';
}function show(data) {
    let tab =
        `<tr>
          <th style="width:30%">Name</th>
          <th style="width:30%">OrcidId</th>
          <th style="width:20%">Affiliation</th>
          <th style="width:20%">Country</th>
         </tr>`;

    // Loop to access all rows
    for (let r of data.list) {
        tab += `<tr> 
    <td>${r.name} </td>
    <td>${r.orcidId}</td>
    <td>${r.affiliation}</td> 
    <td>${r.country}</td>          
    </tr>`;
    }
    document.getElementById("employees").innerHTML = tab;
}
}

