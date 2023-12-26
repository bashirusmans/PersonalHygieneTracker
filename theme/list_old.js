
var checkbox = document.getElementById("mySwitch");
if(checkbox){
    checkbox.addEventListener("change", function() {
        if (checkbox.checked) {
            window.location.href = "dark.html"; 
        }
        else{
            window.location.href = "light.html";
        }
    });
}

var form = document.getElementById("new");
if(form){
    form.addEventListener("submit", function(e) {
        e.preventDefault()
        createTask(document.getElementById("input-field").value)
        document.getElementById("input-field").value = ""
    })
}

function createTask(task){
    
    var num = tasks.push(task)
    var numNode = document.createTextNode("Task "+num)
    var maindiv = document.getElementById("tasks");
    var div2 = document.createElement("div");
    var div3 = document.createElement("div");
    var div4 = document.createElement("div");
    var div5 = document.createElement("div");
    var div6 = document.createElement("div");
    var div7 = document.createElement("div");
    var div8 = document.createElement("div");
    div2.classList.add("card", "m-5");
    div3.classList.add("card-body");
    div4.classList.add("p-1");
    div5.classList.add("ms-auto", "p-2");
    div6.classList.add("d-flex");
    div7.classList.add("p-1");
    div8.classList.add("p-1");
    div2.style.width = '320px';
    var title = document.createElement("h5");
    title.classList.add('card-title');
    var text = document.createElement("b");
    text.classList.add("card-text" ,"fs-4");
    var btn1 = document.createElement("a");
    var btn2 = document.createElement("a");
    if(maindiv.dataset.mode == "dark"){
        div2.classList.add("dark");
        btn1.classList.add("btn","btn-outline-danger");
        btn2.classList.add("btn","btn-outline-danger");
    }
    else{
        div2.classList.add("light");
        btn1.classList.add("btn","btn-outline-light");
        btn2.classList.add("btn","btn-outline-light");
    }
    div4.appendChild(numNode);
    var node1 = document.createTextNode(task)
    text.appendChild(node1);
    btn1.appendChild(document.createTextNode("Delete Task"));
    btn1.addEventListener("click",function(){
            deleteTask(div2);
        }
    )
    var node2 = document.createTextNode("Mark as Done")
    btn2.appendChild(node2);
    btn2.addEventListener("click",function(){
            markDone(btn2, node2, node1, task);
        }
    )
    div2.appendChild(div3);
    div3.appendChild(title);
    title.appendChild(div4);
    title.appendChild(div5);
    div5.appendChild(text);
    div3.appendChild(div6);
    div6.appendChild(div7);
    div6.appendChild(div8);
    div7.appendChild(btn1);
    div8.appendChild(btn2);
    maindiv.appendChild(div2);
    console.log(tasks);
}

function deleteTask(div){
    div.remove()
    console.log(tasks)
}

function markDone(btn, node, text, task){
    node.nodeValue = "Unmark as Done";
    text.nodeValue = task + " (Completed) ";
    btn.addEventListener("click",function(){
            markUndone(btn, node, text, task);
        }
    )
}

function markUndone(btn, node, text, task){
    node.nodeValue = "Mark as Done";
    text.nodeValue = task;
    btn.addEventListener("click",function(){
            markDone(btn, node, text, task);
        }
    )
}

var tasks = []

