"Name: openrej
"Author: Justin Lebar
"Version: 0.1
"Description: XXX

function! OpenRej()
  let l:rejects=system("find . -name '*.rej'")
  for reject in split(l:rejects, '\n', 1)
    if strlen(l:reject) != 0
      let l:regular=substitute(l:reject, ".rej", "", "g")
      execute ":e ".l:reject
      execute ":e ".l:regular
    endif
  endfor
endfunction

command! -nargs=0 OpenRej :call OpenRej()
