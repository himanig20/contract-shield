import streamlit as st
import streamlit.components.v1 as components

st.title("Test Injection")

html_code = """
<script>
try {
    const parent = window.parent.document;
    const div = parent.createElement("div");
    div.innerHTML = "<h1 style='position:fixed; bottom:20px; right:20px; z-index:9999; color:red;'>INJECTED DOM</h1>";
    parent.body.appendChild(div);
} catch(e) {
    document.write("Error: " + e.message);
}
</script>
"""

components.html(html_code, height=0)
