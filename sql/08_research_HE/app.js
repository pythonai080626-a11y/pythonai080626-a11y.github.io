/* Copy buttons for the SQL blocks */
document.querySelectorAll('.copy-btn').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var pre = document.getElementById(btn.dataset.target);
    if (!pre) return;
    var text = pre.innerText;

    function done() {
      btn.textContent = 'הועתק ✓';
      btn.classList.add('copied');
      setTimeout(function () { btn.textContent = 'העתקה'; btn.classList.remove('copied'); }, 1800);
    }
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (e) {}
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else { fallback(); }
  });
});
