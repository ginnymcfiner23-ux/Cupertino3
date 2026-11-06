// Progressive enhancement: live text filter for tables and search boxes.
(function(){
  function norm(s){return (s||'').toString().toLowerCase();}
  function applyFilter(input){
    var q=norm(input.value);
    var scope=input.closest('section')||document;
    var tables=scope.querySelectorAll('table');
    tables.forEach(function(t){
      t.querySelectorAll('tbody tr').forEach(function(tr){
        tr.style.display = !q || norm(tr.textContent).indexOf(q)>-1 ? '' : 'none';
      });
    });
  }
  document.querySelectorAll('.filterbar input[type=search]').forEach(function(inp){
    inp.addEventListener('input', function(){applyFilter(inp);});
  });
})();
