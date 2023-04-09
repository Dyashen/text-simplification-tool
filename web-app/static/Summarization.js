const callPythonFunctionSummarize = async (text) => {
  try {
    const response = await fetch(
      `http://localhost:5000/summarize?text=${text}`
    );
    return (result = await response.json());
  } catch (error) {
    console.error(error);
  }
};

const callPythonFunctionAbstractiveSummarization = async (text) => {
  try {
    const response = await fetch(
      `http://localhost:5000/summarize?text=${text}`
    );
    return (result = await response.json());
  } catch (error) {
    console.error(error);
  }
};

//
async function abstractiveSummarization() {
  var selectedText = window.getSelection().toString();
  const response = await callPythonFunctionAbstractiveSummarization(
    selectedText
  );
  var dazzle = document.querySelector(".dazzle");
  var p = document.createElement("p");
  var p2 = document.createElement("p");
  var text = document.createTextNode(JSON.stringify(response.result));
  var prompt = document.createTextNode(JSON.stringify(response.prompt));
  p.appendChild(prompt);
  dazzle.appendChild(p);
  p2.appendChild(text);
  dazzle.appendChild(p2);
}
