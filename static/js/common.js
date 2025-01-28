var headers = {"Content-Type": "application/json"};

function gebi(eleid){
    return document.getElementById(eleid);
}

function gebcn(class_name){
    return document.getElementsByClassName(class_name);
}

function fetch_data(url, method, headers, data){
    var promise = new Promise(function(resolve, reject){
        var http = new XMLHttpRequest;
        http.open(method, url, true);
        for (var header in headers){
            http.setRequestHeader(header, headers[header]);
        }
        try{
            if (method === "GET"){
                http.send();
            }else{
                http.send(data);
            }
        }catch(error){
            reject({"message": error.name+error.message});
        }
        http.onreadystatechange = function(){
            if (http.readyState === 4){
                if (http.status === 0){
                    reject({"message": "网络错误"})
                }else{
                    resolve({"response_text": http.responseText, "status_code": http.status});
                }
            }
        }
        http.onerror = function(){
            reject({"message": "网络错误"});
        }
    });
    return promise;
}

function fetch_api(endpoint, payload){
    return new Promise(function(resolve, reject){
        fetch_data(endpoint, "POST", headers, JSON.stringify(payload)).then(function(val){
            try{
                var rsp = JSON.parse(val.response_text);
            }catch(err){
                resolve({"retcode": -1, "msg": err, "data": null});
            }
            resolve({"retcode": rsp.success?0:-2, "msg": rsp.message, "data": rsp.data});
        }, function(val){
            resolve({"retcode": -3, "msg": val.message, "data": null})
        });
    });
}

function is_in(chr, str){
    for (var t in str){
        if (chr === str[t]){
            return true;
        }
    }
    return false;
}
function include(ele, list){
    for (var e = 0;e < list.length;e++){
        if (ele === list[e]){
            return true;
        }
    }
    return false;
}
function ts2str(e) {
    e = new Date(1e3 * e);
    return e.getFullYear() + "-" + ("0" + (e.getMonth() + 1)).slice(-2) + "-" + ("0" + e.getDate()).slice(-2) + " " + ("0" + e.getHours()).slice(-2) + ":" + ("0" + e.getMinutes()).slice(-2) + ":" + ("0" + e.getSeconds()).slice(-2)
}
function rsc(e) {
    return e ? e.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;") : e;
}
function get_url_args(){
    var url = window.location.href;
    var ret = {};
    if (url.includes("?")){
        var args = url.split("?").slice(1).join("?").split("&");
        for (var index in args){
            var arg = args[index];
            if (arg.includes("=")){
                var kv = arg.split("=");
                ret[kv[0]] = kv.slice(1).join("=");
            }else{
                ret[arg] = null;
            }
        }
    }
    return ret;
}
function check_logged_in(){
    if (localStorage.getItem("access-token") === null){
        localStorage.login_redirect = window.location.href;
        window.location = "/login";
        return true;
    }
    return false;
}
function get_element_abs_pos2(e) {
    for (var t = e.offsetTop, n = e.offsetLeft; e = e.offsetParent; )
        t += e.offsetTop,
        n += e.offsetLeft;
    return {
        left: n,
        top: t
    }
}
function icon_with_text(icon_name, text){
    return `<img src="/static/image/icon/${icon_name}.svg" alt="" width="16px" class="middle"><span class="middle">${text}</span>`;
}
function set_btn_html(ele, html){
    if (html){
        if (!ele.getAttribute("old_html")){
            ele.setAttribute("old_html", ele.innerHTML);
        }
        ele.innerHTML = html;
        ele.disabled = true;
    }else{
        if (ele.getAttribute("old_html")){
            ele.innerHTML = ele.getAttribute("old_html");
            ele.removeAttribute("old_html");
        }
        ele.disabled = false;
    }
}
String.prototype.replaceAll = function(e, t) {
    return this.split(e).join(t);
}

function b642link(b64, type){
    var file_bytes = atob(b64);
    var file_bytes_array = new Uint8Array(file_bytes.length);
    for (var i=0; i < file_bytes.length; i++){
        file_bytes_array[i] = file_bytes.charCodeAt(i);
    }
    var file_blob = new Blob([file_bytes_array], {"type": type});
    var file_url = URL.createObjectURL(file_blob);
    return file_url;
}

function input_file2b64(file){
    return new Promise(function(resolve, reject){
        var file_reader = new FileReader();
        file_reader.readAsDataURL(file);
        file_reader.onload = function(){
            resolve(this.result.split(",")[1]);
        }
    });
}

// 已弃用
// function update_highlight(parent){
//    if (parent){
//         var hl_ele = parent.querySelectorAll(".marked-highlight");
//     }else{
//         var hl_ele = gebcn("marked-highlight");
//     }
//     for (var i=0; i<hl_ele.length; i++){
//         var ele = hl_ele[i];
//         hljs.highlightElement(ele);
//     }
// }

function insert_into_textarea(text, textarea){
    var start_pos = textarea.selectionStart;
    var end_pos = textarea.selectionEnd;
    var old_text = textarea.value;
    var new_text = old_text.substring(0, start_pos) + text + old_text.substring(end_pos, old_text.length);
    textarea.value = new_text;
    textarea.selectionStart = start_pos + text.length;
    textarea.selectionEnd = start_pos + text.length;
}

function is_in_array(e, t) {
    for (var n = 0; n < e.length; n++)
        if (e[n] === t)
            return true;
    return false
}

function add_markdown_tips(){
    var markdown_tips = "\n提示:\n1. 支持Markdown语法、LaTeX语法\n2. 可直接粘贴图片到输入框，会自动上传\n3. 更多用法请见论坛置顶帖子";
    var textareas = gebcn("marked-textarea");
    for (var i=0;i<textareas.length;i++){
        var textarea = textareas[i];
        if (textarea.getAttribute("placeholder") && !textarea.getAttribute("markdown-tips-set")){
            textarea.setAttribute("placeholder", textarea.getAttribute("placeholder")+markdown_tips);
            textarea.setAttribute("markdown-tips-set", "true");
        }
    }
}

add_markdown_tips();
