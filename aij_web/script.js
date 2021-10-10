async function aij_func(id_search, csv_name, box_name) {
    let val = await eel.aij_system(id_search, csv_name, box_name)();
    document.getElementById('result').value = val;
}


let search = document.getElementById('search')
search.addEventListener('click', () => {
    if (input_form.input_id.value == "") {
        alert("キーワードを入力してください");
        return false;
    }else if(input_form.input_f.value == ""){
        alert("ファイル名を入力してください");
        return false;
    }else if(input_form.input_d.value == ""){
        alert("フォルダ名を入力してください");
        return false;
    }else {
        aij_func(id_search.value, csv_name.value, box_name.value);
        return true;
    }
})