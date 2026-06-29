var stream = new ActiveXObject("ADODB.Stream");
stream.Type = 2; // adTypeText
stream.Charset = "utf-8";
stream.Open();
stream.LoadFromFile("data.js");
var text = stream.ReadText();
stream.Close();

text = text.replace(/const\s+/g, "var ");
text = text.replace(/,\s*\]/g, ']');
text = text.replace(/,\s*\}/g, '}');

try {
    eval(text);
    WScript.Echo("Valid JS!");
} catch (e) {
    WScript.Echo("JS Error: " + e.message + " at character (not line)");
    // Try to find the error position manually using eval in chunks? No, JS Error object might have line/col.
    var err = "";
    for (var k in e) { err += k + ": " + e[k] + ", "; }
    WScript.Echo("Details: " + err);
}
