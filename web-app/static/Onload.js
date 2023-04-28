window.onload = async function () {
    /* --- */
    var url = `http://localhost:5000/get-settings-user`;
    const response = await fetch(url, { method: 'POST' });
    var result = await response.json();
    document.body.style.fontSize = result.fontSize;
    document.body.style.fontFamily = result.fontSettings;
    document.body.style.backgroundColor = result.favcolor;

    /* --- */
    var url = 'http://localhost:5000/get-session-keys';
    const session_keys_response = await fetch(url, { method: 'POST' });
    result = await session_keys_response.json();
    console.log(result);
  }