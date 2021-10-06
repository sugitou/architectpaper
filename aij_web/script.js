// rakutenAPI関数
async function rakuten_func(kw_search, csv_name, box_name, select_api) {
    let val = await eel.rakuten_system(kw_search, csv_name, box_name, select_api)();
    if (select_api == "market_search") {
        document.getElementById('item_name').value = ""
        for (let i = 0; i < val.length; i++) {
            let num = i + 1
            document.getElementById('item_name').value += "【" + num + "件目】" + val[i] + "\n";
        }
    }else if (select_api == "books_search") {
        document.getElementById('book_name').value = ""
        for (let i = 0; i < val.length; i++) {
            let num = i + 1
            document.getElementById('book_name').value += "【" + num + "件目】" + val[i] + "\n";
        }
    }else {
        document.getElementById('hotel_name').value = ""
        for (let i = 0; i < val.length; i++) {
            let num = i + 1
            document.getElementById('hotel_name').value += "【" + num + "件目】" + val[i] + "\n";
        }
    }
}

//初期表示はwrap02とwrap03を非表示
document.getElementById("wrap01").style.display ="block";
document.getElementById("wrap02").style.display ="none";
document.getElementById("wrap03").style.display ="none";
// 変数定義
const wrap01 = document.getElementById("wrap01");
const wrap02 = document.getElementById("wrap02");
const wrap03 = document.getElementById("wrap03");
// 切り替え関数
function vis_invis_01(){
    if(wrap01.style.display=="none"){
        wrap01.style.display ="block";
        wrap02.style.display ="none";
        wrap03.style.display ="none";
    }else{
        wrap01.style.display ="block";
        wrap02.style.display ="none";
        wrap03.style.display ="none";
    }
}
function vis_invis_02(){
    if(wrap02.style.display=="none"){
        wrap01.style.display ="none";
        wrap02.style.display ="block";
        wrap03.style.display ="none";
    }else{
        wrap01.style.display ="none";
        wrap02.style.display ="block";
        wrap03.style.display ="none";
    }
}
function vis_invis_03(){
    if(wrap03.style.display=="none"){
        wrap01.style.display ="none";
        wrap02.style.display ="none";
        wrap03.style.display ="block";
    }else{
        wrap01.style.display ="none";
        wrap02.style.display ="none";
        wrap03.style.display ="block";
    }
}

let market_search = document.getElementById('market_search')
market_search.addEventListener('click', () => {
    if (input_form_01.input_kw.value == "") {
        alert("キーワードを入力してください");
        return false;
    }else if(input_form_01.input_f.value == ""){
        alert("ファイル名を入力してください");
        return false;
    }else if(input_form_01.input_d.value == ""){
        alert("フォルダ名を入力してください");
        return false;
    }else {
        rakuten_func(kw_search_01.value, csv_name_01.value, box_name_01.value, "market_search");
        return true;
    }
})

let books_search = document.getElementById('books_search')
books_search.addEventListener('click', () => {
    if (input_form_02.input_kw.value == "") {
        alert("キーワードを入力してください");
        return false;
    }else if(input_form_02.input_f.value == ""){
        alert("ファイル名を入力してください");
        return false;
    }else if(input_form_02.input_d.value == ""){
        alert("フォルダ名を入力してください");
        return false;
    }else {
        rakuten_func(kw_search_02.value, csv_name_02.value, box_name_02.value, "books_search");
        return true;
    }
})

let travel_search = document.getElementById('travel_search')
travel_search.addEventListener('click', () => {
    if (input_form_03.input_kw.value == "") {
        alert("キーワードを入力してください");
        return false;
    }else if(input_form_03.input_f.value == ""){
        alert("ファイル名を入力してください");
        return false;
    }else if(input_form_03.input_d.value == ""){
        alert("フォルダ名を入力してください");
        return false;
    }else {
        rakuten_func(kw_search_03.value, csv_name_03.value, box_name_03.value, "travel_search");
        return true;
    }
})