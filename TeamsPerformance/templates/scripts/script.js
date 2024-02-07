function valueChanges() {
    let options = document.getElementById('leagues');
    console.log(options.value)
}
    

document.getElementById('leagues').addEventListener('change',valueChanges);
