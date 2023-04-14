const callPythonFunctionExtractiveSummarize = async (text) => {
  try {
    const response = await fetch(`http://localhost:5000/extract-text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text, key: 'sc' })
    });
    return (result = await response.json());
  } catch (error) {
    console.error(error);
  }
};

async function extractiveSummarization() {
  //
  var selectedText = window.getSelection().toString();
  if (selectedText === "") {
    selectedText = document.body.innerText;
  }

  // dazzle ->  p-> prompt; p2 -> text
  var dazzle = document.querySelector(".dazzle");
  var p = document.createElement("p");
  var p2 = document.createElement("p");

  //
  var prompt = document.createTextNode("Kernzinnen ophalen...");
  var text = document.createTextNode("...");

  //
  p.appendChild(prompt);
  dazzle.appendChild(p);
  p2.appendChild(text);
  dazzle.appendChild(p2);

  //
  const response = await callPythonFunctionExtractiveSummarize(selectedText);

  console.log(response);

  prompt.nodeValue = "Kernzinnen uit geselecteerde tekst...";
  text.nodeValue = JSON.stringify(response.result);
}
