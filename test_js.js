var fs = new ActiveXObject("Scripting.FileSystemObject");
var text = fs.OpenTextFile("data.js", 1, false, -1).ReadAll(); // -1 for Unicode, but let's just try to read it
// If data.js is utf-8, FSO might mess up the characters, but syntax errors usually remain intact unless the multibyte characters form quotes.
// Better way to read UTF-8 in JScript:
var stream = new ActiveXObject("ADODB.Stream");
stream.Type = 2; // adTypeText
stream.Charset = "utf-8";
stream.Open();
stream.LoadFromFile("data.js");
var text = stream.ReadText();
stream.Close();

// Replace ES6 const with var
text = text.replace(/const\s+QUIZ_DATA/, "var QUIZ_DATA");
// Remove trailing commas to be ES5 compliant (JScript doesn't like trailing commas sometimes, though it might)
text = text.replace(/,\s*\]/g, ']');
text = text.replace(/,\s*\}/g, '}');

try {
    eval(text);
    WScript.Echo("Valid JS!");
} catch (e) {
    WScript.Echo("JS Error: " + e.message);
}
