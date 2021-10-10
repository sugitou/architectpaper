async function jgl_func(csv_name, box_name) {
    let val = await eel.jgl_system(csv_name, box_name)();
    document.getElementById('result').value = val;
}


let search = document.getElementById('search')
search.addEventListener('click', () => {
    if(input_form.input_f.value == ""){
        alert("ファイル名を入力してください");
        return false;
    }else if(input_form.input_d.value == ""){
        alert("フォルダ名を入力してください");
        return false;
    }else {
        jgl_func(csv_name.value, box_name.value);
        return true;
    }
})