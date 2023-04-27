window.onload = async function () {
    var url = `http://localhost:5000/get-settings-user`;
    const response = await fetch(url, { method: 'POST' });
    var result = await response.json();
    document.body.style.fontSize = result.fontSize;
    document.body.style.fontFamily = result.fontSettings;
    document.body.style.backgroundColor = result.favcolor;
  }